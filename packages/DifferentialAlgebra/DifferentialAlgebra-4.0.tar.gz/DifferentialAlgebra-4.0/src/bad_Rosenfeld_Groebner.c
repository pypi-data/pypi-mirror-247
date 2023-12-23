#include "bad_selection_strategy.h"
#include "bad_reduction.h"
#include "bad_regularize.h"
#include "bad_quadruple.h"
#include "bad_Rosenfeld_Groebner.h"
#include "bad_global.h"
#include "bad_base_field.h"
#include "bad_stats.h"

#define BAD_RG_DEBUG
#undef BAD_RG_DEBUG

/*
 * blad_indent: -l120
 */

/*
 * texinfo: bad_Rosenfeld_Groebner
 * Apply a version of the @dfn{Rosenfeld-Gr@"{o}bner} algorithm.
 * Assign to @var{tabC} a set of differential regular chains.
 * These differential regular chains define differential ideals whose
 * intersection is equal to the radical of the differential ideal
 * @math{[P]:S^\infty}. 
 * 
 * The function @code{bad_fast_primality_test_regchain} is applied
 * over each component of @var{tabC}.
 * 
 * The intersection may involve redundant components.
 * The function @code{bad_remove_redundant_components_intersectof_regchain}
 * is not called.
 * 
 * If zero, the parameter @var{S} is considered as the empty set.
 * 
 * If different from zero, @var{K0} contains a description
 * of a base field. In this case,
 * every nonzero polynomial @var{p} lying in the base field is
 * considered as non zero by @dfn{Rosenfeld-Gr@"{o}bner}: the 
 * case @math{p = 0} is not considered in the tree of splittings.
 * If the @var{K} parameter involves a non trivial regular differential
 * chain then the elements of this chain are incorporated to each
 * regular differential chain produced by @dfn{Rosenfeld-Gr@"{o}bner}.
 * The exception @code{BAD_ERRIBF} may be raised if the properties
 * of the regular chain of @var{K} are not compatible with those
 * of @var{tabC}.
 * 
 * If @var{K0} is the zero pointer then 
 * only nonzero polynomials depending on independent variables
 * are considered as base field elements.
 * 
 * If the @var{C} parameter is the zero pointer then the whole splitting
 * tree is computed and returned. This parameter can however be used
 * to control the splitting tree.
 */

BAD_DLL void
bad_Rosenfeld_Groebner (
    bad_intersectof_regchain tabC,
    bap_tableof_polynom_mpz P,
    bap_tableof_polynom_mpz S,
    bad_base_field K0,
    bad_splitting_control C)
{
/*
 * Initializations are just there to avoid stupid warnings
 */
  bad_base_field K;
  bad_selection_strategy strategy;
  bad_splitting_tree tree;
  bad_splitting_control control;
  ba0_int_p numberof_input_equations = 0;
  bool use_dimlb = false, reject;

  struct bad_tableof_quadruple tabG;
  bad_quadruple G;

  enum bad_typeof_reduction type_red = bad_full_reduction;

  struct bap_tableof_polynom_mpz ineqs;
  struct bap_tableof_product_mpz factored_ineqs;

  struct bap_product_mpz prod;

  struct bap_tableof_polynom_mpz tabP;

  bap_polynom_mpz p = (bap_polynom_mpz) 0;
  bap_polynom_mpz q = (bap_polynom_mpz) 0;

  bav_variable v;
  ba0_int_p c, i, g, k, counter;
  struct ba0_mark M;
/*
 * Initializes stats
 */
  bad_init_stats ();
  bad_global.stats.begin = time (0);
/*
 * Automatic properties will thus be inherited by the resulting regular chains.
 */
  tabC->inter.size = 0;
  bad_set_automatic_properties_attchain (&tabC->attrib);

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * Management of the node numbering of quadruples
 */
  tree = bad_new_splitting_tree ();
#if defined (BAD_RG_DEBUG)
  bad_activate_splitting_tree (tree);
#endif

/*
 * From now on, use control.
 */
  if (C == (bad_splitting_control) 0)
    control = bad_new_splitting_control ();
  else
    control = C;
/*
 * Base field management. If autoreduced, it is more efficient to
 * set K0->assume_reduced before calling bad_Rosenfeld_Groebner.
 */
  if (K0 == (bad_base_field) 0)
    K = bad_new_base_field ();
  else
    {
      if (!bad_is_a_compatible_base_field (K0, &tabC->attrib))
        BA0_RAISE_EXCEPTION (BAD_ERRIBF);
      if (bad_has_property_attchain (&tabC->attrib, bad_autoreduced_property))
        {
          if (K0->assume_reduced)
            K = K0;
          else
            {
              K = bad_new_base_field ();
              bad_set_base_field (K, K0);
              K->assume_reduced = true;
            }
        }
      else
        K = K0;
    }

  if (bad_defines_a_differential_ideal_attchain (&tabC->attrib))
    type_red = bad_full_reduction;
  else
    type_red = bad_algebraic_reduction;
/*
 * The bad_first_quadruple function stores P and S in the components P and S 
 * of quadruples and stores them in tabG. 
 *
 * The base field defining equations are removed from P.
 */
  ba0_init_table ((ba0_table) & tabG);
  bad_first_quadruple (&tabG, &tabC->attrib, P, S, type_red, K, tree);
/*
 * tabP is used by the Euclidean algorithm.
 */
  ba0_init_table ((ba0_table) & tabP);
  ba0_realloc2_table ((ba0_table) & tabP, 1, (ba0_new_function *) & bap_new_polynom_mpz);
  tabP.size = 1;
/*
 * ineqs and factored_ineqs are used when some simplification
 * (factorization) of some inequation is discovered.
 */
  ba0_init_table ((ba0_table) & ineqs);
  ba0_init_table ((ba0_table) & factored_ineqs);
/*
 * p and prod are local variables.
 * counter is only used for debugging.
 */
  p = bap_new_polynom_mpz ();
  bap_init_product_mpz (&prod);
  counter = 0;
  strategy = bad_new_selection_strategy ();
/*
 * MAIN LOOP
 *
 * It stops if there is not any quadruple to process anymore or
 * if the splitting control variable tells us to do so.
 */
  while (tabG.size > 0 && (!control->first_leaf_only || tabC->inter.size == 0))
    {
      counter++;
      if (bad_is_active_splitting_tree (tree))
        {
          ba0_printf ("------------------------------------------------\n");
          ba0_printf ("Round %d, |tabG| = %d\n", counter, tabG.size);
        }

/*
 * G is the top element of the stack
 */
      G = tabG.tab[tabG.size - 1];
      if (bad_is_active_splitting_tree (tree))
        {
          ba0_int_p father = bad_node_quadruple (G);
          ba0_printf ("Handling quadruple %d\n", father);
        }
      if (bad_first_case_quadruple (G))
        {
/*
 * The dimension lower bound. 
 * numberof_input_equations does not count the base field defining equations.
 *
 * It will apply to all quadruples generated from this one until another
 * first quadruple shows up.
 */
          use_dimlb = bad_apply_dimension_lower_bound_splitting_control (control, G->P, &tabC->attrib);
          numberof_input_equations = ba0_length_list ((ba0_list) G->P);
        }
/*
 * The dimension lower bound can be applied to reject quadruples
 */
      reject = false;
      if (use_dimlb)
        {
          reject = bad_codimension_regchain (&G->A, K) > numberof_input_equations;
        }

      if (reject)
        {
          if (bad_is_active_splitting_tree (tree))
            {
              ba0_int_p father = bad_node_quadruple (G);
              ba0_printf ("Rejecting quadruple %d (dimension argument)\n", father);
            }
          tabG.size -= 1;
        }
      else if (bad_is_a_listof_rejected_critical_pair (G->D) && G->P == (bap_listof_polynom_mpz) 0)
        {
          c = tabC->inter.size;
/*
 * The purely algebraic treatment.
 * G is pulled out of the stack.
 * The reg_characteristic algorithm transforms it as finitely many regchains
 *     which are stacked over tabC.
 */
          if (bad_is_active_splitting_tree (tree))
            {
              ba0_int_p father = bad_node_quadruple (G);
              ba0_printf ("Calling reg_characteristic on quadruple %d\n", father);
            }
          tabG.size -= 1;
          ba0_pull_stack ();
          bad_reg_characteristic_quadruple (tabC, G, (bad_regchain) 0, K);
          if (bad_is_active_splitting_tree (tree))
            {
              ba0_printf ("|tabC| = %d\n", tabC->inter.size);
            }
          ba0_push_another_stack ();

          ba0_int_p father = bad_node_quadruple (G);
          for (i = c; i < tabC->inter.size; i++)
            {
              ba0_int_p child = bad_next_node_splitting_tree (tree);
              bad_set_number_regchain (tabC->inter.tab[i], child);
              bad_append_edge_splitting_tree (tree, tree, father,
                  tabC->inter.tab[i]->number, bad_reg_characteristic_edge);
            }
        }
      else
        {
          bad_critical_pair pair;

          bad_pick_and_remove_quadruple (p, G, &pair, strategy);
          if (bad_is_active_splitting_tree (tree))
            {
              ba0_int_p father = bad_node_quadruple (G);
              ba0_printf ("New equation from quadruple %d: %Az\n", father, p);
            }
/*
 * If the reduction to zero test is deterministic, we may as well
 * skip it since we are going to reduce p anyway.
 *
 * If it is probabilistic, it is better to perform it before
 * the reduction.
 */
          if (bad_initialized_global.reduction.redzero_strategy == bad_probabilistic_redzero_strategy)
            {
              if (bad_is_a_reduced_to_zero_polynom_by_regchain (p, &G->A, type_red))
                {
                  if (bad_is_active_splitting_tree (tree))
                    {
                      ba0_printf ("New equation is reduced to zero\n");
                    }
                  bad_set_as_child_quadruple (G, G, bad_redzero_edge, tree);
                  bad_global.stats.reductions_to_zero += 1;
                  continue;
                }
            }
#if defined (BA0_HEAVY_DEBUG)
          struct bap_product_mpz H_p;
          bap_init_product_mpz (&H_p);
          bad_reduce_polynom_by_regchain (&prod, &H_p, p, &G->A, type_red, bad_all_derivatives_to_reduce);
#else
          bad_reduce_polynom_by_regchain (&prod, (bap_product_mpz) 0, p, &G->A,
              type_red, bad_all_derivatives_to_reduce);
#endif
/*
 * If the picked polynomial reduces to zero, pick the next one.
 */
          if (bap_is_zero_product_mpz (&prod))
            {
              if (bad_is_active_splitting_tree (tree))
                {
                  ba0_printf ("New equation is reduced to zero\n");
                }
              bad_set_as_child_quadruple (G, G, bad_redzero_edge, tree);
              bad_global.stats.reductions_to_zero += 1;
              continue;
            }
/*
 * The picked polynomial, which is now a product gets simplified.
 * The simplification preprocess may exhibit factorizations of
 * inequations, which are propagated in tabG.
 */
          bad_preprocess_equation_quadruple (&prod, &ineqs, &factored_ineqs, G, K);
          bad_report_simplification_of_inequations_quadruple (&tabG, &ineqs, &factored_ineqs);

          if (bad_is_active_splitting_tree (tree))
            {
              ba0_printf ("new equation after reduction: %Pz\n", &prod);
            }
          if (prod.size == 0)
            {
              if (bad_is_active_splitting_tree (tree))
                {
                  ba0_int_p father = bad_node_quadruple (G);
                  ba0_printf ("Rejecting inconsistent quadruple %d\n", father);
                }
              tabG.size -= 1;
              continue;
            }
/*
 * Assume prod is f1 ... fn = 0
 * The following function performs the following :
 * 	for i = 1 to n-1 do
 * 	    H := G, "fi = 0"
 * 	    G := G, "fi != 0"
 * 	done
 * So that, afterwards, G involves f1 <> 0, ..., f{n-1} <> 0 and we 
 * only have to deal with the case fn = 0. 
 */
          prod.size -= 1;
          bad_split_on_factors_of_equations_quadruple (&tabG, &prod, (bap_product_mpz) 0, bad_factor_edge, tree);
          if (bad_is_active_splitting_tree (tree))
            {
              ba0_int_p father = bad_node_quadruple (G);
              ba0_printf ("Current quadruple is now Quadruple %d\n", father);
            }
          BA0_SWAP (struct bap_polynom_mpz,
              *p,
              prod.tab[prod.size].factor);
/*
 * The following function splits on the initial and separant of p.
 * This function calls bad_preprocess_equation_quadruple and may simplify
 * the inequations of many quadruples.
 */
          bad_split_on_initial_and_separant_quadruple (&tabG, p, K, tree);
          if (bad_is_active_splitting_tree (tree))
            {
              ba0_int_p father = bad_node_quadruple (G);
              ba0_printf ("Current quadruple is now Quadruple %d\n", father);
            }
          v = bap_leader_polynom_mpz (p);
          if (!bad_is_leader_of_regchain (v, &G->A, &k))
            {
              g = tabG.size - 1;
/*
 * The complete function transforms G as finitely many quadruples which 
 * overwrite G at the top of the stack.
 */
              bad_complete_quadruple (&tabG, p, (bad_regchain) 0, K, strategy, tree);
              if (bad_is_active_splitting_tree (tree))
                {
                  if (tabG.size - 1 < g)
                    {
                      ba0_int_p father = bad_node_quadruple (G);
                      ba0_printf ("quadruple %d removed by bad_complete_quadruple\n", father);
                    }
                }
            }
          else
            {
              tabP.size = 1;
              g = tabG.size - 1;
/*
 * The Euclid function transforms G as finitely many quadruples G1, ..., Gn
 * which overwrite G at the top of the stack. It computes also the 
 * corresponding gcds g1, ..., gn of G->A.decision_system.tab [k] 
 * and p which overwrite the top element of the tabV stack.
 *
 * complete (Gi, gi) is performed afterwards for i = 1 ... n.
 */
              q = G->A.decision_system.tab[k];
              if (bad_is_active_splitting_tree (tree))
                {
                  ba0_int_p father = bad_node_quadruple (G);
                  ba0_printf ("\ngcd (%Az, %Az) mod quadruple %d\n", q, p, father);
                }
              bad_gcd_mod_quadruple (&tabP, &tabG, q, p, v, K, tree);
              if (bad_is_active_splitting_tree (tree))
                {
                  for (i = 0; i < tabP.size; i++)
                    {
                      ba0_int_p node = bad_node_quadruple (tabG.tab[i + g]);
                      ba0_printf ("gcd = %Az mod quadruple %d\n", tabP.tab[i], node);
                    }
                }
              for (i = tabP.size - 1; i >= 0; i--)
                {
                  ba0_move_to_tail_table ((ba0_table) & tabG, (ba0_table) & tabG, i + g);
                  bad_complete_quadruple (&tabG, tabP.tab[i], (bad_regchain) 0, K, strategy, tree);
                }
            }
        }
    }
  ba0_pull_stack ();
  if (bad_is_active_splitting_tree (tree))
    {
      bad_dot_splitting_tree (tree);
    }
/*
 * All explicit regchains get the prime attribute
 */
  bad_fast_primality_test_intersectof_regchain (tabC);
  ba0_restore (&M);
  bad_global.stats.end = time (0);
}

/*
 * texinfo: bad_split_on_initial_and_separant_quadruple
 * Append to @var{tabG} the quadruples generated
 * by the possible vanishing of
 * the initial and the separant of @var{p}.
 */

BAD_DLL void
bad_split_on_initial_and_separant_quadruple (
    bad_tableof_quadruple tabG,
    bap_polynom_mpz p,
    bad_base_field K,
    bad_splitting_tree tree)
{
  bad_quadruple G;
  struct bap_tableof_product_mpz factored_ineqs;
  struct bap_tableof_polynom_mpz ineqs;
  struct bap_product_mpz prod_init, prod_reductum, prod_sep, prod_sepuctum;
  struct bap_polynom_mpz init, reductum, sep, sepuctum;
  struct ba0_mark M;
  ba0_int_p g;

  g = tabG->size - 1;
  G = tabG->tab[g];

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * To manage exhibited factorizations of inequations
 */
  ba0_init_table ((ba0_table) & ineqs);
  ba0_init_table ((ba0_table) & factored_ineqs);
/*
 * First the initial
 */
  bap_init_readonly_polynom_mpz (&init);
  bap_init_readonly_polynom_mpz (&reductum);
  bap_initial_and_reductum_polynom_mpz (&init, &reductum, p);

  bap_init_product_mpz (&prod_init);
  bap_init_product_mpz (&prod_reductum);
/*
 * Discard obviously useless splittings
 */
  if (!bad_member_nonzero_polynom_base_field (&init, K) && !bad_member_nonzero_polynom_base_field (&reductum, K))
    {
      baz_factor_easy_polynom_mpz (&prod_init, &init, G->S);
      bad_preprocess_equation_quadruple (&prod_init, &ineqs, &factored_ineqs, G, K);
      if (ineqs.size > 0)
        {
          ba0_pull_stack ();
          bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
          ba0_push_another_stack ();
        }
      if (prod_init.size > 0)
        {
/*
 * The initial is never identically zero but the reductum can be identically zero.
 */
          baz_factor_easy_polynom_mpz (&prod_reductum, &reductum, G->S);
          bad_preprocess_equation_quadruple (&prod_reductum, &ineqs, &factored_ineqs, G, K);
          if (ineqs.size > 0)
            {
              ba0_pull_stack ();
              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
              ba0_push_another_stack ();
            }
          if (prod_reductum.size > 0 || bap_is_zero_product_mpz (&prod_reductum))
            {
              ba0_pull_stack ();
              bad_split_on_factors_of_equations_quadruple (tabG, &prod_init, &prod_reductum, bad_inisep_edge, tree);
              ba0_push_another_stack ();
            }
        }
    }
/*
 * Then the separant, if needed.
 */
  if (bap_leading_degree_polynom_mpz (p) > 1 && bad_has_property_attchain (&G->A.attrib, bad_squarefree_property))
    {
      bap_init_polynom_mpz (&sep);
      bap_init_polynom_mpz (&sepuctum);
      bap_separant_and_sepuctum_polynom_mpz (&sep, &sepuctum, p);

      bap_init_product_mpz (&prod_sep);
      bap_init_product_mpz (&prod_sepuctum);
/*
 * Discard obviously useless splittings. 
 * Observe that the separant involves the leading derivative of p.
 */
      if (!bad_member_nonzero_polynom_base_field (&sepuctum, K))
        {
          baz_factor_easy_polynom_mpz (&prod_sep, &sep, G->S);
          bad_preprocess_equation_quadruple (&prod_sep, &ineqs, &factored_ineqs, G, K);
          if (ineqs.size > 0)
            {
              ba0_pull_stack ();
              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
              ba0_push_another_stack ();
            }
          if (prod_sep.size > 0)
            {
              baz_factor_easy_polynom_mpz (&prod_sepuctum, &sepuctum, G->S);
              bad_preprocess_equation_quadruple (&prod_sepuctum, &ineqs, &factored_ineqs, G, K);
              if (ineqs.size > 0)
                {
                  ba0_pull_stack ();
                  bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
                  ba0_push_another_stack ();
                }
              if (prod_sepuctum.size > 0 || bap_is_zero_product_mpz (&prod_sepuctum))
                {
                  ba0_pull_stack ();
                  bad_split_on_factors_of_equations_quadruple (tabG, &prod_sep, &prod_sepuctum, bad_inisep_edge, tree);
                  ba0_push_another_stack ();
                }
            }
        }
    }

  ba0_pull_stack ();
  ba0_restore (&M);
}

/*
 * texinfo: bad_first_quadruple
 * Initialize the first quadruple with P and S.
 * The process may lead to splittings (there may be many different
 * first quadruples).
 * All generated quadruples have edges of type @code{bad_first_edge}.
 * The base field equations, if any, are inserted in the regchains.
 */

BAD_DLL void
bad_first_quadruple (
    bad_tableof_quadruple tabG,
    bad_attchain attrib,
    bap_tableof_polynom_mpz P,
    bap_tableof_polynom_mpz S,
    enum bad_typeof_reduction type_red,
    bad_base_field K,
    bad_splitting_tree tree)
{
  bad_quadruple G;
  struct bap_tableof_polynom_mpz ineqs;
  struct bap_tableof_product_mpz factored_ineqs;
  struct bap_product_mpz prod;
  struct ba0_mark M;
  ba0_int_p i, j, k;
  bool base_field;

  if (tabG->size != 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_realloc2_table ((ba0_table) tabG, 1, (ba0_new_function *) bad_new_quadruple);
  G = tabG->tab[0];
  bad_set_node_type_splitting_edge (&G->edge, -1, 0, bad_first_edge);
  tabG->size = 1;
/*
 * The relations of K are directly stored in G->A.
 * Overwrite the attributes of K->relations.attrib with attrib.
 */
  base_field = K != (bad_base_field) 0;
  if (base_field)
    bad_set_regchain (&G->A, &K->relations);

  bad_set_attchain (&G->A.attrib, attrib);

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_init_table ((ba0_table) & ineqs);
  ba0_init_table ((ba0_table) & factored_ineqs);
  bap_init_product_mpz (&prod);
/*
 * First process the inequations.
 * No splitting occurs since "p*q != 0" is just "p != 0", "q != 0".
 * However, the quadruple G may be proved inconsistent and discarded.
 */
  if (S)
    {
      for (i = 0; i < S->size && tabG->size > 0; i++)
        {
/*
 * An inequation might be reduced to zero by a base field equation
 * factor_easy does not expect zero polynomials.
 */
          if (base_field)
            bad_reduce_polynom_by_regchain (&prod, (bap_product_mpz) 0,
                S->tab[i], &G->A, type_red, bad_all_derivatives_to_reduce);
          else if (bap_is_numeric_polynom_mpz (S->tab[i]))
            bap_set_product_polynom_mpz (&prod, S->tab[i], 1);
          else
            baz_factor_easy_polynom_mpz (&prod, S->tab[i], G->S);
/*
 * In the case "0 != 0", remove the quadruple G from the stack.
 */
          if (bap_is_zero_product_mpz (&prod))
            tabG->size -= 1;
          else
            {
              bad_preprocess_equation_quadruple (&prod, &ineqs, &factored_ineqs, G, K);
              ba0_pull_stack ();
              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
              for (j = 0; j < prod.size; j++)
                G->S = bad_insert_in_listof_polynom_mpz (&prod.tab[j].factor, G->S);
              ba0_push_another_stack ();
            }
        }
    }
/*
 * Then process the equations.
 * Splittings can occur, since "p*q = 0" is "p = 0" or "q = 0" (two cases).
 * Fix some new equation P->tab [i].
 */
  for (i = 0; i < P->size; i++)
    {
/*
 * Loop invariant: quadruples in tabG->tab [k+1 .. tabG->size-1]
 *                 have already received the new equation P->tab[i]
 */
      for (k = tabG->size - 1; k >= 0; k--)
        {
/*
 * The kth quadruple is moved at the tail of tabG
 * This simplifies the management of splittings
 */
          ba0_move_to_tail_table ((ba0_table) tabG, (ba0_table) tabG, k);
          G = tabG->tab[tabG->size - 1];
          if (base_field)
            bad_reduce_polynom_by_regchain (&prod, (bap_product_mpz) 0,
                P->tab[i], &G->A, type_red, bad_all_derivatives_to_reduce);
          else if (bap_is_numeric_polynom_mpz (P->tab[i]))
            bap_set_product_polynom_mpz (&prod, P->tab[i], 1);
          else
            baz_factor_easy_polynom_mpz (&prod, P->tab[i], G->S);

          if (bap_is_numeric_product_mpz (&prod))
            {
/*
 * The quadruple is discarded
 */
              if (!bap_is_zero_product_mpz (&prod))
                tabG->size -= 1;
            }
          else
            {
              bad_preprocess_equation_quadruple (&prod, &ineqs, &factored_ineqs, G, K);

              ba0_pull_stack ();
              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
              if (prod.size == 0)
                {
/*
 * The quadruple is discarded
 */
                  tabG->size -= 1;
                }
              else
                {
/*
 * Apply bad_split_on_factors_of_equations_quadruple for all but the last factor.
 * Store the last equation in G->P manually.
 */
                  prod.size -= 1;
                  bad_split_on_factors_of_equations_quadruple (tabG, &prod, (bap_product_mpz) 0, bad_first_edge, tree);
                  G->P = bad_insert_in_listof_polynom_mpz (&prod.tab[prod.size].factor, G->P);
                }
              ba0_push_another_stack ();
            }
        }
    }
  ba0_pull_stack ();
/*
 * All quadruples must be first_edge quadruples.
 */
  for (i = 0; i < tabG->size; i++)
    if (!bad_first_case_quadruple (tabG->tab[i]))
      BA0_RAISE_EXCEPTION (BA0_ERRALG);
  ba0_restore (&M);
}

/*
 * texinfo: bad_gcd_mod_quadruple
 * Compute the gcds of @var{A} and @var{B}, viewed as
 * polynomials in @var{v} with coefficients taken
 * modulo the ideal defined by the last quadruple
 * of @var{tabG}. 
 * The polynomial @var{A} has positive degree in @var{v}.
 * The polynomial @var{B} has degree less than @var{A} 
 * in @var{v} (possibly zero).
 */

BAD_DLL void
bad_gcd_mod_quadruple (
    bap_tableof_polynom_mpz tabP,
    bad_tableof_quadruple tabG,
    bap_polynom_mpz A,
    bap_polynom_mpz B,
    bav_variable v,
    bad_base_field K,
    bad_splitting_tree tree)
{
  bad_quadruple G, H, I, J;
  struct bap_product_mpz prod, prod_init, prod_reductum;
  struct bap_polynom_mpz R, init, reductum;
  struct bap_tableof_product_mpz factored_ineqs;
  struct bap_tableof_polynom_mpz ineqs;
  bap_polynom_mpz poly;
  struct ba0_mark M;
  ba0_int_p i, j, k, l, g, h, p, q, delta;
  bool init_may_vanish;

/*
 * g = the index of G in tabG.
 * p = the index in tabP corresponding to G.
 * delta is used for debugging.
 */
  g = tabG->size - 1;
  p = tabP->size - 1;
  delta = g - p;
  G = tabG->tab[g];
/*
 * If B is zero, the gcd is A.
 * if B does not depend on v, then it is stored in P and thus
 * implicitly becomes equal to zero, whence the gcd is A.
 */
  if (bap_is_zero_polynom_mpz (B))
    {
      bap_set_polynom_mpz (tabP->tab[p], A);
    }
  else if (!bap_depend_polynom_mpz (B, v))
    {
      G->P = bad_insert_in_listof_polynom_mpz (B, G->P);
      bap_set_polynom_mpz (tabP->tab[p], A);
    }
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      bap_init_polynom_mpz (&R);
      bap_init_product_mpz (&prod);
      ba0_init_table ((ba0_table) & ineqs);
      ba0_init_table ((ba0_table) & factored_ineqs);
      bap_init_readonly_polynom_mpz (&init);
      bap_init_readonly_polynom_mpz (&reductum);
      bap_init_product_mpz (&prod_init);
      bap_init_product_mpz (&prod_reductum);
/*
 * R = remainder (A, B, v)
 */
      baz_gcd_prem_polynom_mpz (&R, (bap_product_mpz) 0, A, B, v);
/*
 * Get rid of the two special cases: R = 0 and R cannot vanish.
 */
      if (bap_is_zero_polynom_mpz (&R))
        {
          ba0_pull_stack ();
          bad_gcd_mod_quadruple (tabP, tabG, B, &R, v, K, tree);
          ba0_push_another_stack ();
/*
	 else if ((*bad_nonzero) (&R))
 */
        }
      else if (bad_member_nonzero_polynom_base_field (&R, K))
        {
          tabP->size -= 1;
          tabG->size -= 1;
        }
      else
        {
/*
 * R can vanish. Preprocess it.
 */
          baz_factor_easy_polynom_mpz (&prod, &R, G->S);
          bad_preprocess_equation_quadruple (&prod, &ineqs, &factored_ineqs, G, K);
          if (ineqs.size > 0)
            {
              ba0_pull_stack ();
              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
              ba0_push_another_stack ();
            }
          if (prod.size == 0)
            {
/*
 * This case may happen if prod only involve factors which occur in G->S
 */
              tabP->size -= 1;
              tabG->size -= 1;
            }
          else
            {
              for (i = 0; i < prod.size; i++)
                {
/*
 * For each factor of R (index is i)
 */
                  poly = &prod.tab[i].factor;

                  ba0_pull_stack ();
/*
 * H = G
 * G = G + "ith factor of R != 0"
 * except for the last factor, in which case H = G.
 *
 * h = the index of H in tabG
 * q = the index in tabP corresponding to H
 */
                  if (i < prod.size - 1)
                    {
                      ba0_realloc2_table ((ba0_table) tabG, tabG->size + 1, (ba0_new_function *) & bad_new_quadruple);
                      ba0_realloc2_table ((ba0_table) tabP, tabP->size + 1, (ba0_new_function *) & bap_new_polynom_mpz);
                      tabG->size += 1;
                      tabP->size += 1;
                      h = tabG->size - 1;
                      q = tabP->size - 1;
                      H = tabG->tab[h];
                      bad_set_as_child_quadruple (H, G, bad_euclid_edge, tree);
                      bad_insert_in_S_quadruple (G, G, poly, bad_euclid_edge, tree);
/*
                      G->S = bad_insert_in_listof_polynom_mpz (poly, G->S);
                      bad_promote_as_child_quadruple (G, bad_euclid_edge, tree);
*/
                    }
                  else
                    {
                      ba0_move_to_tail_table ((ba0_table) tabG, (ba0_table) tabG, g);
                      ba0_move_to_tail_table ((ba0_table) tabP, (ba0_table) tabP, p);
                      g = tabG->size - 1;
                      p = tabP->size - 1;
                      h = tabG->size - 1;
                      q = tabP->size - 1;
                      H = G;
                    }
                  ba0_push_another_stack ();
                  if (!bap_depend_polynom_mpz (poly, v))
                    {
/*
 * If the ith factor of R does not depend on v, suppose it equal to
 * zero and take B for gcd.
 */
                      ba0_pull_stack ();
                      bad_gcd_mod_quadruple (tabP, tabG, B, poly, v, K, tree);
                      ba0_push_another_stack ();
                    }
                  else
                    {
/*
 * Take the initial and reductum of the ith factor of R
 * The ith factor of prod should not involve trivial factors so
 * that the reductum should not be zero.
 */
                      bap_initial_and_reductum2_polynom_mpz (&init, &reductum, poly, v);
                      if (bap_is_zero_polynom_mpz (&reductum))
                        BA0_RAISE_EXCEPTION (BA0_ERRALG);
/*
                        init_may_vanish = ! (*bad_nonzero) (&init);
                        if (init_may_vanish && ! (*bad_nonzero) (&reductum))
 */
                      init_may_vanish = !bad_member_nonzero_polynom_base_field (&init, K);
                      if (init_may_vanish && !bad_member_nonzero_polynom_base_field (&reductum, K))
                        {
/*
 * If both the initial and the reductum can vanish, generate splittings.
 */
                          baz_factor_easy_polynom_mpz (&prod_init, &init, H->S);
                          bad_preprocess_equation_quadruple (&prod_init, &ineqs, &factored_ineqs, H, K);
                          if (ineqs.size > 0)
                            {
                              ba0_pull_stack ();
                              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
                              ba0_push_another_stack ();
                            }
                          if (prod_init.size > 0)
                            {
                              baz_factor_easy_polynom_mpz (&prod_reductum, &reductum, H->S);
                              bad_preprocess_equation_quadruple (&prod_reductum, &ineqs, &factored_ineqs, H, K);
                              if (ineqs.size > 0)
                                {
                                  ba0_pull_stack ();
                                  bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
                                  ba0_push_another_stack ();
                                }
                              if (prod_reductum.size > 0)
                                {
                                  ba0_pull_stack ();
/*
 * If, really, both initial and reductum can vanish, split.
 * Observe the (bap_product_mpz)0, which means that the reductum
 * is temporarily assumed identically zero.
 */
                                  bad_split_on_factors_of_equations_quadruple
                                      (tabG, &prod_init, (bap_product_mpz) 0, bad_euclid_edge, tree);
/*
 * H was moved on the top of tabG so that h is no more the index of H !
 */
                                  if (H != tabG->tab[tabG->size - 1])
                                    BA0_RAISE_EXCEPTION (BA0_ERRALG);
                                  ba0_realloc2_table ((ba0_table) tabP,
                                      tabP->size + tabG->size - h - 1, (ba0_new_function *) & bap_new_polynom_mpz);
                                  tabP->size += tabG->size - h - 1;
/*
 * For each new quadruple generated by the splittings, 
 *     for each factor of the reductum, recursive call:
 *          Euclid (B, the factor of the reductum) over the quadruple
 */
                                  for (j = tabG->size - 2, k = tabP->size - 2; j >= h; j--, k--)
                                    {
                                      for (l = 0; l < prod_reductum.size; l++)
                                        {
/*
 * I = the new quadruple
 * J = I 
 * I = I + "the lth factor of the reductum != 0"
 * except for the last factor, in which case I = J
 */
                                          if (l < prod_reductum.size - 1)
                                            {
                                              ba0_realloc2_table ((ba0_table)
                                                  tabG, tabG->size + 1, (ba0_new_function *) & bad_new_quadruple);
                                              ba0_realloc2_table ((ba0_table)
                                                  tabP, tabP->size + 1, (ba0_new_function *) & bap_new_polynom_mpz);
                                              tabG->size += 1;
                                              tabP->size += 1;
                                              I = tabG->tab[j];
                                              J = tabG->tab[tabG->size - 1];
                                              bad_set_as_child_quadruple (J, I, bad_euclid_edge, tree);
                                              bad_insert_in_S_quadruple (I, I,
                                                  &prod_reductum.tab[l].factor, bad_euclid_edge, tree);
/*
                                              I->S = bad_insert_in_listof_polynom_mpz (&prod_reductum.tab[l].factor, I->S);
                                              bad_promote_as_child_quadruple (I, bad_euclid_edge, tree);
*/
                                            }
                                          else
                                            {
                                              ba0_move_to_tail_table ((ba0_table) tabG, (ba0_table) tabG, j);
                                              ba0_move_to_tail_table ((ba0_table) tabP, (ba0_table) tabP, k);
                                            }
                                          bad_gcd_mod_quadruple (tabP, tabG, B,
                                              &prod_reductum.tab[l].factor, v, K, tree);
                                        }
                                    }
                                  ba0_push_another_stack ();
                                }
                            }
                        }
                      else if (init_may_vanish)
                        {
/*
 * The reductum cannot vanish but the initial, isolated, could.
 * To make sure that the gcd is correct, force it not to vanish.
 */
                          baz_factor_easy_polynom_mpz (&prod_init, &init, H->S);
                          bad_preprocess_equation_quadruple (&prod_init, &ineqs, &factored_ineqs, H, K);
                          if (ineqs.size > 0)
                            {
                              ba0_pull_stack ();
                              bad_report_simplification_of_inequations_quadruple (tabG, &ineqs, &factored_ineqs);
                              ba0_push_another_stack ();
                            }
                          ba0_pull_stack ();
                          for (j = 0; j < prod_init.size; j++)
                            H->S = bad_insert_in_listof_polynom_mpz (&prod_init.tab[j].factor, H->S);
                          ba0_push_another_stack ();
                        }
                      if (H != tabG->tab[h])
                        BA0_RAISE_EXCEPTION (BA0_ERRALG);
/*
 * Over H, the initial of the ith factor of R cannot vanish.
 * Recursive call:
 *    Euclid (B, ith factor of R) over H
 */
                      ba0_pull_stack ();
                      ba0_move_to_tail_table ((ba0_table) tabG, (ba0_table) tabG, h);
                      ba0_move_to_tail_table ((ba0_table) tabP, (ba0_table) tabP, q);
                      bad_gcd_mod_quadruple (tabP, tabG, B, poly, v, K, tree);
                      ba0_push_another_stack ();
                    }
                }
            }
        }
      ba0_pull_stack ();
      ba0_restore (&M);
    }
  if (delta != tabG->size - tabP->size)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
}
