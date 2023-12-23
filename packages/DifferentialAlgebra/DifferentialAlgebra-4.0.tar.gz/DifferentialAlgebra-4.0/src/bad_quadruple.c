#include "bad_quench_regchain.h"
#include "bad_reduction.h"
#include "bad_regularize.h"
#include "bad_quadruple.h"
#include "bad_global.h"
#include "bad_stats.h"

/*
 * texinfo: bad_init_quadruple
 * Initialize @var{G}.
 */

BAD_DLL void
bad_init_quadruple (
    bad_quadruple G)
{
  bad_init_regchain (&G->A);
  G->D = (bad_listof_critical_pair) 0;
  G->P = G->S = (bap_listof_polynom_mpz) 0;
  bad_init_splitting_edge (&G->edge);
}

/*
 * texinfo: bad_new_quadruple
 * Allocate a new quadruple, initialize it and return it.
 */

BAD_DLL bad_quadruple
bad_new_quadruple (
    void)
{
  bad_quadruple G;

  G = (bad_quadruple) ba0_alloc (sizeof (struct bad_quadruple));
  bad_init_quadruple (G);
  return G;
}

/*
 * texinfo: bad_set_quadruple
 * Assign @var{Q} to @var{P}.
 */

BAD_DLL void
bad_set_quadruple (
    struct bad_quadruple *P,
    struct bad_quadruple *Q)
{
  bad_set_regchain (&P->A, &Q->A);
  P->D = (bad_listof_critical_pair) ba0_copy ("%l[%critic]", Q->D);
  P->P = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->P);
  P->S = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->S);
  bad_set_splitting_edge (&P->edge, &Q->edge);
}

/* 
 * texinfo: bad_set_as_child_quadruple
 * Assign @var{Q} to @var{P} but not the @code{edge} field.
 * A new node number is assigned to @var{P} from @var{tree}.
 * The edge of @var{P} is built using this node number, the one of @var{Q}
 * and @var{type}. This edge is also appended to @var{tree}.
 */

BAD_DLL void
bad_set_as_child_quadruple (
    struct bad_quadruple *P,
    struct bad_quadruple *Q,
    enum bad_typeof_splitting_edge type,
    struct bad_splitting_tree *tree)
{
  ba0_int_p father, child;

  if (P != Q)
    {
      bad_set_regchain (&P->A, &Q->A);
      P->D = (bad_listof_critical_pair) ba0_copy ("%l[%critic]", Q->D);
      P->P = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->P);
      P->S = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->S);
    }
  father = bad_node_quadruple (Q);
  child = bad_next_node_splitting_tree (tree);
  bad_set_node_type_splitting_edge (&P->edge, father, child, type);
  bad_append_edge_splitting_tree (tree, tree, father, child, type);

  if (bad_is_active_splitting_tree (tree))
    {
      ba0_printf ("- - - - - - - - - - - - - - - - - - - - - - - - \n");
      ba0_printf ("set_as_child generates:\n%quadruple\n", P);
    }
}

/*
 * texinfo: bad_insert_in_S_quadruple
 * Assign @var{Q} to @var{P} but not the @code{edge} field.
 * Insert @var{poly} in the field @code{S} of @var{P}.
 * A new node number is assigned to @var{P} from @var{tree}.
 * The edge of @var{P} is built using this node number, the one of @var{Q}
 * and @var{type}. This edge is also appended to @var{tree}.
 */

BAD_DLL void
bad_insert_in_S_quadruple (
    struct bad_quadruple *P,
    struct bad_quadruple *Q,
    struct bap_polynom_mpz *poly,
    enum bad_typeof_splitting_edge type,
    struct bad_splitting_tree *tree)
{
  ba0_int_p father, child;

  if (P != Q)
    {
      bad_set_regchain (&P->A, &Q->A);
      P->D = (bad_listof_critical_pair) ba0_copy ("%l[%critic]", Q->D);
      P->P = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->P);
      P->S = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->S);
    }
  P->S = bad_insert_in_listof_polynom_mpz (poly, P->S);
  father = bad_node_quadruple (Q);
  child = bad_next_node_splitting_tree (tree);
  bad_set_node_type_splitting_edge (&P->edge, father, child, type);
  bad_append_edge_splitting_tree (tree, tree, father, child, type);

  if (bad_is_active_splitting_tree (tree))
    {
      ba0_printf ("- - - - - - - - - - - - - - - - - - - - - - - - \n");
      ba0_printf ("insert_in_S generates:\n%quadruple\n", P);
    }
}

/*
 * texinfo: bad_insert_in_P_quadruple
 * Assign @var{Q} to @var{P} but not the @code{edge} field.
 * Insert @var{poly} in the field @code{P} of @var{P}.
 * A new node number is assigned to @var{P} from @var{tree}.
 * The edge of @var{P} is built using this node number, the one of @var{Q}
 * and @var{type}. This edge is also appended to @var{tree}.
 */

BAD_DLL void
bad_insert_in_P_quadruple (
    struct bad_quadruple *P,
    struct bad_quadruple *Q,
    struct bap_polynom_mpz *poly,
    enum bad_typeof_splitting_edge type,
    struct bad_splitting_tree *tree)
{
  ba0_int_p father, child;

  if (P != Q)
    {
      bad_set_regchain (&P->A, &Q->A);
      P->D = (bad_listof_critical_pair) ba0_copy ("%l[%critic]", Q->D);
      P->P = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->P);
      P->S = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->S);
    }
  P->P = bad_insert_in_listof_polynom_mpz (poly, P->P);
  father = bad_node_quadruple (Q);
  child = bad_next_node_splitting_tree (tree);
  bad_set_node_type_splitting_edge (&P->edge, father, child, type);
  bad_append_edge_splitting_tree (tree, tree, father, child, type);

  if (bad_is_active_splitting_tree (tree))
    {
      ba0_printf ("- - - - - - - - - - - - - - - - - - - - - - - - \n");
      ba0_printf ("insert_in_P generates:\n%quadruple\n", P);
    }
}

/*
 * Variant of @code{bad_set_as_child_quadruple}.
 * The regchain A is handled in a special way.
 */

static void
bad_set_as_child2_quadruple (
    struct bad_quadruple *P,
    struct bad_quadruple *Q,
    struct bad_regchain *A,
    enum bad_typeof_splitting_edge type,
    struct bad_splitting_tree *tree)
{
  ba0_int_p father, child;

  if (P != Q)
    {
      bad_set_regchain (&P->A, A);
//      P->A = *A;
      P->D = (bad_listof_critical_pair) ba0_copy ("%l[%critic]", Q->D);
      P->P = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->P);
      P->S = (bap_listof_polynom_mpz) ba0_copy ("%l[%Az]", Q->S);
    }
  else
    bad_set_regchain (&P->A, A);
//    P->A = *A;
  father = bad_node_quadruple (Q);
  child = bad_next_node_splitting_tree (tree);
  bad_set_node_type_splitting_edge (&P->edge, father, child, type);
  bad_append_edge_splitting_tree (tree, tree, father, child, type);

  if (bad_is_active_splitting_tree (tree))
    {
      ba0_printf ("- - - - - - - - - - - - - - - - - - - - - - - - \n");
      ba0_printf ("set_as_child2 generates:\n%quadruple\n", P);
    }
}

/*
 * texinfo: bad_scanf_quadruple
 * The parsing function for quadruples.
 * It is called by @code{ba0_scanf/%quadruple}.
 * The expected format is @code{quadruple (regular chain, D = list of critical pairs, P = list of polynomials, S = list of polynomials, edge = splitting edge)}.
 */

BAD_DLL void *
bad_scanf_quadruple (
    void *A)
{
  bad_quadruple G;

  if (A == (void *) 0)
    G = bad_new_quadruple ();
  else
    G = (bad_quadruple) A;

  ba0_scanf
      ("quadruple (%regchain, D = %l[%critic], P = %l[%Az], S = %l[%Az], edge = %splitting_edge)",
      &G->A, &G->D, &G->P, &G->S, &G->edge);

  return G;
}

/*
 * texinfo: bad_printf_quadruple
 * The printing function for quadruples.
 * It is called by @code{ba0_printf/%quadruple}.
 */

BAD_DLL void
bad_printf_quadruple (
    void *A)
{
  bad_quadruple G = (bad_quadruple) A;

  ba0_printf
      ("quadruple %d (%regchain,\nD = %l[\n%critic],\nP = %l[%Az],\nS = %l[%Az],\nedge = %splitting_edge)",
      bad_node_quadruple (G), &G->A, G->D, G->P, G->S, &G->edge);
}

/*
 * Readonly static data
 */

static char _struct_quadruple[] = "struct bad_quadruple";

BAD_DLL ba0_int_p
bad_garbage1_quadruple (
    void *A,
    enum ba0_garbage_code code)
{
  bad_quadruple G = (bad_quadruple) A;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (G, sizeof (struct bad_quadruple), _struct_quadruple);

  n += bad_garbage1_regchain (&G->A, ba0_embedded);
  n += ba0_garbage1 ("%l[%critic]", G->D, ba0_isolated);
  n += ba0_garbage1 ("%l[%Az]", G->P, ba0_isolated);
  n += ba0_garbage1 ("%l[%Az]", G->S, ba0_isolated);
  n += bad_garbage1_splitting_edge (&G->edge, ba0_embedded);

  return n;
}

BAD_DLL void *
bad_garbage2_quadruple (
    void *A,
    enum ba0_garbage_code code)
{
  bad_quadruple G;

  if (code == ba0_isolated)
    G = (bad_quadruple) ba0_new_addr_gc_info (A, _struct_quadruple);
  else
    G = (bad_quadruple) A;

  bad_garbage2_regchain (&G->A, ba0_embedded);
  G->D = ba0_garbage2 ("%l[%critic]", G->D, ba0_isolated);
  G->P = ba0_garbage2 ("%l[%Az]", G->P, ba0_isolated);
  G->S = ba0_garbage2 ("%l[%Az]", G->S, ba0_isolated);
  bad_garbage2_splitting_edge (&G->edge, ba0_embedded);

  return G;
}

BAD_DLL void *
bad_copy_quadruple (
    void *A)
{
  bad_quadruple G;

  G = bad_new_quadruple ();
  bad_set_quadruple (G, (bad_quadruple) A);
  return G;
}

/*
 * texinfo: bad_node_quadruple
 * Return the node number of @var{G}.
 */

BAD_DLL ba0_int_p
bad_node_quadruple (
    bad_quadruple G)
{
  return G->edge.dst;
}

/*
 * texinfo: bad_first_case_quadruple
 * Return @code{true} if @var{G} corresponds to a first case quadruple, i.e.
 * a quadruple produced from raw lists of equations and inequations.
 */

BAD_DLL bool
bad_first_case_quadruple (
    bad_quadruple G)
{
  return G->edge.type == bad_first_edge;
}

/*
 * texinfo: bad_insert_in_listof_polynom_mpz
 * Insert a copy of @var{p} in @var{L}. In place function.
 * The list @var{L} is assumed to be the component @var{P} or @var{S} of
 * some quadruple. If @var{p} is already present in @var{L}, it is
 * not duplicated.  The systematic use of this function keeps lists sorted.
 */

BAD_DLL bap_listof_polynom_mpz
bad_insert_in_listof_polynom_mpz (
    bap_polynom_mpz p,
    bap_listof_polynom_mpz L)
{
  bap_listof_polynom_mpz R, cour, prec, cons;
  ba0_int_p nbmon_p, nbmon_c;
  bool forget, found;

  nbmon_p = bap_nbmon_polynom_mpz (p);

  found = false;
  forget = false;

  prec = (bap_listof_polynom_mpz) 0;
  cour = L;
  while (cour != (bap_listof_polynom_mpz) 0 && !found && !forget)
    {
      nbmon_c = bap_nbmon_polynom_mpz (cour->value);
      if (nbmon_p < nbmon_c)
        found = true;
      else if (nbmon_p == nbmon_c)
        {
          if (bap_lt_rank_polynom_mpz (p, cour->value))
            found = true;
          else if (bap_equal_polynom_mpz (p, cour->value))
            forget = true;
        }
      if (!found && !forget)
        {
          prec = cour;
          cour = cour->next;
        }
    }
/*
 * forget = true means that p is already present. Just forget it.
 * Otherwise, a new cons should be inserted in front of cour.
 */
  if (!forget)
    {
      cons = (bap_listof_polynom_mpz) ba0_alloc
          (sizeof (struct bap_listof_polynom_mpz));
      cons->next = cour;
      cons->value = (bap_polynom_mpz) bap_copy_polynom_mpz (p);
/*
 * Insertion at the beginning of the list ?
 */
      if (prec == (bap_listof_polynom_mpz) 0)
        R = cons;
      else
        {
          prec->next = cons;
          R = L;
        }
    }
  else
    R = L;
  return R;
}

/*
 * texinfo: bad_delete_from_listof_polynom_mpz
 * Remove @var{p} from the list @var{L}.
 * The argument @var{deletion} is set to @code{true} if @var{p} was present
 * in @var{L}, else it is set to @code{false}. It may be the zero pointer.
 */

BAD_DLL bap_listof_polynom_mpz
bad_delete_from_listof_polynom_mpz (
    bap_polynom_mpz p,
    bap_listof_polynom_mpz L,
    bool *deletion)
{
  bap_listof_polynom_mpz prec, cour, R;
  bool found;

  found = false;

  prec = (bap_listof_polynom_mpz) 0;
  cour = L;
  while (cour != (bap_listof_polynom_mpz) 0 && !found)
    {
      found = bap_equal_polynom_mpz (p, cour->value);
      if (!found)
        {
          prec = cour;
          cour = cour->next;
        }
    }
/*
 * found = p is equal to cour->value
 */
  if (!found)
    {
      if (deletion)
        *deletion = false;
      R = L;
    }
  else
    {
      if (deletion)
        *deletion = true;
/*
 * Deletion of the first element ?
 */
      if (prec == (bap_listof_polynom_mpz) 0)
        R = L->next;
      else
        {
          prec->next = cour->next;
          R = L;
        }
    }
  return R;
}

/*
 * texinfo: bad_preprocess_equation_quadruple
 * Simplify @var{A} using the inequations of @var{G}, mostly
 * by means of gcd computations. This simplification process may exhibit a
 * factorization of some inequation of @var{G}. Any such factorization is
 * recorded as an entry in @var{ineqs} and @var{factored_ineqs}. 
 * Factors which cannot vanish are discarded: the nonzero elements of the
 * base field @var{K}).
 */

BAD_DLL void
bad_preprocess_equation_quadruple (
    bap_product_mpz A,
    bap_tableof_polynom_mpz ineqs,
    bap_tableof_product_mpz factored_ineqs,
    bad_quadruple G,
    bad_base_field K)
{
  struct bap_product_mpz prod, prod_gcd;
  struct bap_tableof_polynom_mpz polys;
  bap_listof_polynom_mpz S;
  struct bap_polynom_mpz gcd, cof;
  struct ba0_mark M;
  ba0_int_p i, length;
  bool removed, already_stored;

  ba0_reset_table ((ba0_table) ineqs);
  ba0_reset_table ((ba0_table) factored_ineqs);

  if (bap_is_numeric_product_mpz (A))
    {
      if (!bap_is_zero_product_mpz (A))
        ba0_mpz_set_si (A->num_factor, 1);
      return;
    }

  length = ba0_length_list ((ba0_list) G->S);
  ba0_realloc_table ((ba0_table) ineqs, length);
  ba0_realloc2_table ((ba0_table) factored_ineqs, length,
      (ba0_new_function *) & bap_new_product_mpz);

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_product_mpz (&prod);
  bap_set_product_mpz (&prod, A);

  ba0_mpz_set_si (prod.num_factor, 1);

  ba0_init_table ((ba0_table) & polys);
  ba0_realloc_table ((ba0_table) & polys, 2);

  bap_init_product_mpz (&prod_gcd);
  bap_init_polynom_mpz (&gcd);
  bap_init_polynom_mpz (&cof);

  i = 0;
  while (i < prod.size)
    {
/*
 * removed = the ith component of the product is removed (it corresponds
 *           to a polynomial which cannot vanish).
 */
      if (bad_member_nonzero_polynom_base_field (&prod.tab[i].factor, K))
        {
          if (i != prod.size - 1)
            BA0_SWAP (struct bap_polynom_mpz,
                prod.tab[i].factor,
                prod.tab[prod.size - 1].factor);
          prod.size -= 1;
          removed = true;
        }
      else
        {
          removed = false;
          S = G->S;
          already_stored = false;
          while (!removed && S != (bap_listof_polynom_mpz) 0)
            {
              polys.tab[0] = &prod.tab[i].factor;
              polys.tab[1] = S->value;
              polys.size = 2;
              baz_gcd_tableof_polynom_mpz (&prod_gcd, &polys, false);
              if (!bap_is_numeric_product_mpz (&prod_gcd))
                {
/*
 * Non-trivial gcd between the ith component and the current inequation.
 * Factor the gcd out. May lead to a component that should be removed.
 */
                  bap_expand_product_mpz (&gcd, &prod_gcd);
                  bap_exquo_polynom_mpz
                      (&prod.tab[i].factor, &prod.tab[i].factor, &gcd);
                  removed = bad_member_nonzero_polynom_base_field
                      (&prod.tab[i].factor, K);
                  if (!already_stored &&
                      (prod_gcd.size > 1 ||
                          !bap_equal_polynom_mpz (S->value, &gcd)))
                    {
/*
 * The non-trivial gcd is also a non-trivial factor of the current inequation.
 * Simplifies the inequations.
 */
                      bap_exquo_polynom_mpz (&cof, S->value, &gcd);

                      ba0_pull_stack ();

                      ineqs->tab[ineqs->size] = S->value;
                      bap_mul_product_polynom_mpz
                          (factored_ineqs->tab[factored_ineqs->size],
                          &prod_gcd, &cof, 1);

                      ineqs->size += 1;
                      factored_ineqs->size += 1;

                      ba0_push_another_stack ();
                      already_stored = true;
                    }
                }
              else
                {
                  S = S->next;
                  already_stored = false;
                }
            }
        }
      if (!removed)
        {
          prod.tab[i].exponent = 1;
          i += 1;
        }
    }

  ba0_pull_stack ();
  bap_set_product_mpz (A, &prod);
  ba0_restore (&M);
}

/*
 * texinfo: bad_report_simplification_of_inequations_quadruple
 * Replace in the field @code{S} of each quadruple of @var{tabG}
 * any occurence of any polynomial of @var{ineqs} by its factors,
 * given in @var{factored_ineqs}. These factors are supposed to
 * be processed by @code{bad_preprocess_equation_quadruple}.
 */

BAD_DLL void
bad_report_simplification_of_inequations_quadruple (
    bad_tableof_quadruple tabG,
    bap_tableof_polynom_mpz ineqs,
    bap_tableof_product_mpz factored_ineqs)
{
  bad_quadruple G;
  bap_product_mpz prod;
  bap_polynom_mpz p;
  ba0_int_p i, j, k;
  bool found;

  if (ineqs->size != factored_ineqs->size)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  for (k = 0; k < ineqs->size; k++)
    {
      p = ineqs->tab[k];
      prod = factored_ineqs->tab[k];
      for (i = 0; i < tabG->size; i++)
        {
          G = tabG->tab[i];
          G->S = bad_delete_from_listof_polynom_mpz (p, G->S, &found);
          if (found)
            {
              for (j = 0; j < prod->size; j++)
                G->S = bad_insert_in_listof_polynom_mpz
                    (&prod->tab[j].factor, G->S);
            }
        }
    }
}

/*
 * texinfo: bad_split_on_factors_of_equations_quadruple
 * Generate in @var{tabG} the quadruples obtained from the top quadruple
 * @var{G} of @var{tabG}, covering the cases where the two products 
 * @var{prod1} and @var{prod2} both vanish.
 * In each generated quadruple, at least one factor of @var{prod1} and
 * one factor of @var{prod2} are inserted in the field @code{P} of @var{G}.
 * Generated cases are disjoint.
 * Eeventually, @var{G} is modified and covers the case where prod1
 * does not vanish.
 *
 * The most generic cases are stacked above the less generic ones, so that
 * @var{G} itself eventually appears on the top of @var{tabG}. 
 *
 * The products @var{prod1} and @var{prod2} are assumed to be preprocessed
 * equations (see @code{bad_preprocess_equation_quadruple}) so that no new quadruple
 * leads to an obviously inconsistent system. 
 * The product @var{prod1} may be a nonzero constant. 
 * The product @var{prod2} may be either the zero product or a product 
 * involving at least one factor.
 */

BAD_DLL void
bad_split_on_factors_of_equations_quadruple (
    bad_tableof_quadruple tabG,
    bap_product_mpz prod1,
    bap_product_mpz prod2,
    enum bad_typeof_splitting_edge type,
    bad_splitting_tree tree)
{
  bad_quadruple G, H, I;
  bap_polynom_mpz p, q;
  ba0_int_p g, h, i, j;

  if (bap_is_zero_product_mpz (prod1) ||
      (prod2 && prod2->size == 0 && !bap_is_zero_product_mpz (prod2)))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  g = tabG->size - 1;
  G = tabG->tab[g];
/*
 * G is on the top of tabG
 */
  ba0_realloc2_table
      ((ba0_table) tabG,
      tabG->size + prod1->size * (1 + (prod2 ? prod2->size : 0)),
      (ba0_new_function *) & bad_new_quadruple);

  for (i = 0; i < prod1->size; i++)
    {
/*
 * H = G + "p = 0",
 * G = G + "p != 0"
 */
      p = &prod1->tab[i].factor;
      h = tabG->size;
      H = tabG->tab[h];
      bad_insert_in_P_quadruple (H, G, p, type, tree);
/*
      bad_set_as_child_quadruple (H, G, bad_inisep_edge, tree);
      H->P = bad_insert_in_listof_polynom_mpz (p, H->P);
*/
      bad_insert_in_S_quadruple (G, G, p, type, tree);
/*
      bad_promote_as_child_quadruple (G, bad_inisep_edge, tree);
      G->S = bad_insert_in_listof_polynom_mpz (p, G->S);
*/
      tabG->size += 1;
/*
 * H is on the top of tabG
 */
      if (prod2 && prod2->size > 0)
        {
/*
 * The last factor is handled separately in order not to generate
 * the case where all the factors of prod2 are inequations.
 */
          for (j = 0; j < prod2->size - 1; j++)
            {
/*
 * I = H + "q = 0",
 * H = H + "q != 0"
 */
              q = &prod2->tab[j].factor;
              I = tabG->tab[tabG->size];
              bad_insert_in_P_quadruple (I, H, q, type, tree);
/*
              bad_set_as_child_quadruple (I, H, type, tree);
              I->P = bad_insert_in_listof_polynom_mpz (q, I->P);
*/
              bad_insert_in_S_quadruple (H, H, q, type, tree);
/*
              bad_promote_as_child_quadruple (H, type, tree);
              H->S = bad_insert_in_listof_polynom_mpz (q, H->S);
*/
              tabG->size += 1;
            }
          q = &prod2->tab[prod2->size - 1].factor;
          bad_insert_in_P_quadruple (H, H, q, type, tree);
/*
          H->P = bad_insert_in_listof_polynom_mpz (q, H->P);
*/
          ba0_move_to_tail_table ((ba0_table) tabG, (ba0_table) tabG, h);
        }
/*
 * H is again at the end of tabG
 */
    }
/*
 * G is again at the end of tabG
 */
  ba0_move_to_tail_table ((ba0_table) tabG, (ba0_table) tabG, g);
}

/*
 * texinfo: bad_simplify_and_store_in_P_quadruple
 * Store in the @code{P} field of @var{G} the polynomial @var{p}
 * after some simplification (see @code{bad_preprocess_equation_quadruple}).
 * Return @code{false} if @var{p} is proved to be nonzero so that
 * @var{G} becomes inconsistent else return @code{false}.
 */

BAD_DLL bool
bad_simplify_and_store_in_P_quadruple (
    bad_quadruple G,
    bap_polynom_mpz p,
    bad_base_field K)
{
  struct bap_tableof_polynom_mpz ineqs;
  struct bap_tableof_product_mpz factored_ineqs;
  struct bap_product_mpz prod;
  bap_polynom_mpz q;
  struct ba0_mark M;

  if (bap_is_zero_polynom_mpz (p))
    return true;

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_init_table ((ba0_table) & ineqs);
  ba0_init_table ((ba0_table) & factored_ineqs);
  bap_init_product_mpz (&prod);
  bap_set_product_polynom_mpz (&prod, p, 1);
  bad_preprocess_equation_quadruple (&prod, &ineqs, &factored_ineqs, G, K);

  ba0_pull_stack ();

  q = bap_new_polynom_mpz ();
  bap_expand_product_mpz (q, &prod);

  ba0_restore (&M);
/*
 * Nonzero factors of prod are removed by bad_simplify_relation_mod_quadruple
 * Might be useful for some bad_nonzero functions and when all factors
 * of prod are nonzero.
 *
 */
  if (bad_member_nonzero_polynom_base_field (q, K))
    return false;
  else
    {
      G->P = bad_insert_in_listof_polynom_mpz (p, G->P);
      return true;
    }
}

/*
 * texinfo: bad_simplify_and_store_in_S_quadruple
 * Store in the @code{S} field of @var{G} the polynomial @var{p}
 * after some simplification (see @code{bad_preprocess_equation_quadruple}).
 * Return @code{false} if @var{p} is proved to be zero so that
 * @var{G} becomes inconsistent else return @code{false}.
 */

BAD_DLL bool
bad_simplify_and_store_in_S_quadruple (
    bad_quadruple G,
    bap_polynom_mpz p,
    bad_base_field K)
{
  struct bap_tableof_polynom_mpz ineqs;
  struct bap_tableof_product_mpz factored_ineqs;
  struct bap_product_mpz prod;
  ba0_int_p i;
  bool consistent;
  struct ba0_mark M;

  if (bap_is_zero_polynom_mpz (p))
    return false;

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_init_table ((ba0_table) & ineqs);
  ba0_init_table ((ba0_table) & factored_ineqs);
  bap_init_product_mpz (&prod);
  bap_set_product_polynom_mpz (&prod, p, 1);
  bad_preprocess_equation_quadruple (&prod, &ineqs, &factored_ineqs, G, K);

  consistent = true;
  for (i = 0; i < prod.size && consistent; i++)
    {
      if (!bad_member_nonzero_polynom_base_field (&prod.tab[i].factor, K))
        {
          ba0_pull_stack ();
          G->S = bad_insert_in_listof_polynom_mpz (&prod.tab[i].factor, G->S);
          ba0_push_another_stack ();
        }
      else if (bap_is_zero_polynom_mpz (p))
        consistent = false;
    }

  ba0_pull_stack ();
  ba0_restore (&M);

  return consistent;
}

/***********************************************************************
 * PICK AND REMOVE FROM QUADRUPLE
 **********************************************************************/

/*
 * Picks a polynomial from G->P and stores it in p.
 */

static void
bad_pick_from_P_quadruple (
    bap_polynom_mpz p,
    bad_quadruple G,
    bad_critical_pair *pair)
{
  if (G->P == (bap_listof_polynom_mpz) 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  bap_set_polynom_mpz (p, G->P->value);
  G->P = G->P->next;
  if (pair)
    *pair = (bad_critical_pair) 0;
}

/*
 * Picks a pair from G->D. The picked pair is stored in *pair.
 * The Delta-polynomial is stored in p.
 */

static void
bad_pick_from_D_quadruple (
    bap_polynom_mpz p,
    bad_quadruple G,
    bad_critical_pair *pair)
{
  struct bav_tableof_variable nulles;
  struct ba0_mark M;

  if (G->D == (bad_listof_critical_pair) 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_table ((ba0_table) & nulles);
  bad_reduced_to_zero_derivatives_by_regchain
      (&nulles, &G->A, bad_full_reduction);
  ba0_pull_stack ();
  bad_delta_polynom_critical_pair (p, G->D->value, &nulles);
  ba0_restore (&M);
  if (pair)
    *pair = G->D->value;
  G->D = G->D->next;
}

/*
 * Picks elements of P first
 */

static void
bad_pick_and_remove_quadruple_P_first (
    bap_polynom_mpz p,
    bad_quadruple G,
    bad_critical_pair *pair)
{
  if (G->P != (bap_listof_polynom_mpz) 0)
    bad_pick_from_P_quadruple (p, G, pair);
  else
    bad_pick_from_D_quadruple (p, G, pair);
}

/*
 * Between a polynomial p and a critical pair {f, g}, picks
 * the one of lower "leader" (the leader of {f, g} being the 
 * lcd of the leaders of f and g).
 */

static void
bad_pick_and_remove_quadruple_lower_leader_first (
    bap_polynom_mpz p,
    bad_quadruple G,
    bad_critical_pair *pair)
{
  bav_variable u, v;

  if (G->P == (bap_listof_polynom_mpz) 0)
    bad_pick_from_D_quadruple (p, G, pair);
  else if (G->D == (bad_listof_critical_pair) 0)
    bad_pick_from_P_quadruple (p, G, pair);
  else
    {
      u = bap_leader_polynom_mpz (G->P->value);
      v = bav_lcd_variable
          (bap_leader_polynom_mpz (&G->D->value->p),
          bap_leader_polynom_mpz (&G->D->value->q));
      if (bav_R_variable_number (u) < bav_R_variable_number (v))
        bad_pick_from_P_quadruple (p, G, pair);
      else
        bad_pick_from_D_quadruple (p, G, pair);
    }
}

/*
 * texinfo: bad_pick_and_remove_quadruple
 * It is assumed that one of the components @var{P} or @var{D} of the quadruple 
 * is non empty. Assign to @var{p} the first element of @var{P} or the 
 * @math{\Delta}-polynomial defined by the first critical pair of @var{D}.
 * The choice is defined by @var{strategy}.
 * The picked element is removed from the list.
 * If @var{p} is picked from @var{P} then zero is assigned
 * to @var{pair} else the picked pair is assigned to @var{pair}.
 * The pointer @var{pair} is allowed to be zero.
 */

BAD_DLL void
bad_pick_and_remove_quadruple (
    bap_polynom_mpz p,
    bad_quadruple G,
    bad_critical_pair *pair,
    bad_selection_strategy S)
{
  switch (S->strategy)
    {
    case bad_equation_first_selection_strategy:
      bad_pick_and_remove_quadruple_P_first (p, G, pair);
      break;
    case bad_lower_leader_first_selection_strategy:
      bad_pick_and_remove_quadruple_lower_leader_first (p, G, pair);
      break;
    }
}

/*
 * texinfo: bad_reg_characteristic_quadruple
 * Denote @math{I} the unit ideal if @var{ideal} i zero and the ideal
 * defined by @var{ideal} otherwise.
 * It is assumed that 
 *      @math{G = \langle A,\, \emptyset,\, \emptyset,\, S \rangle}, that 
 *      @math{A = 0,\ S \neq 0} is a regular differential system and that
 *      @math{[A] : S^\infty \subset I}.
 * This function stores in @var{tabC} a list of regular differential chains
 *      @math{A_1, \ldots, A_t} such that
 * @math{[A] : S^\infty \subset [A_1] :{H_{A_1}}^\infty 
 *                  \cap \cdots \cap [A_t] : {H_{A_t}}^\infty \subset I}.
 * In the case @math{I} is prime the function only returns one
 * regular chain. If moreover @math{I} is a minimal prime of
 * @math{[C] : {H_C}^\infty} then the returned regular chain is a 
 * characteristic set of @math{I}. 
 * Polynomials are supposed to have coefficients in @var{K}.
 */

BAD_DLL void
bad_reg_characteristic_quadruple (
    bad_intersectof_regchain tabC,
    bad_quadruple G,
    bad_regchain ideal,
    bad_base_field K)
{
  ba0_realloc2_table ((ba0_table) & tabC->inter, tabC->inter.size + 1,
      (ba0_new_function *) & bad_new_regchain);
  tabC->inter.size++;
  bad_set_regchain (tabC->inter.tab[tabC->inter.size - 1], &G->A);
  bad_reg_characteristic_regchain (tabC, G->S, ideal, K);
}

/***************************************************************************
 COMPLETE
 ***************************************************************************/

static void bad_insert_in_regchain (
    bad_regchain,
    bap_polynom_mpz,
    ba0_int_p *,
    ba0_int_p *);
static void bad_update_D (
    bad_quadruple,
    ba0_int_p,
    bap_polynom_mpz,
    bad_selection_strategy);
static bool bad_partially_reduce_S (
    bad_quadruple,
    bad_base_field);

/*
 * texinfo: bad_complete_quadruple
 * Denote @math{G = \langle A,\, D,\, P,\, S \rangle} the last element 
 * of @var{tabG}.
 * 
 * The purely algebraic context.
 * 
 * The function stores @math{r} in @math{A}.
 * If @math{A} involves an element having the same leader as @math{r} 
 *      then this element is just discarded.
 * 
 * The differential context.
 * 
 * It is assumed that @math{r} is partially reduced w.r.t. @math{A}.
 * The function stores @math{r} in @math{A}.
 * If @math{A} involves an element having the same leader as @math{r} 
 *      then this element is just discarded (in particular, no critical 
 *      pair is generated between this possible element and @math{r}).
 * Some critical pairs are generated and stored in @math{D}.
 * This list is sorted according to @var{strategy}.
 * The elements of @math{S} are reduced partially w.r.t. @math{A}.
 * 
 * Both contexts.
 * 
 * The quenching operation, applied on @math{A} may split @math{A} in finitely
 * many different regular chains. In this case, the quadruple @math{G} is
 * split into the same number of quadruples.
 * The resulting quadruples are stored in @var{tabG}, at indices greater
 * than or equal to that of @math{G} (the functions reuses the input 
 * quadruple @math{G}).
 * 
 * The parameter @var{ideal} is provided to the quenching operation
 * and permits to avoid some splittings: if an element of @math{A} factors as
 * @math{f_1\,f_2 = 0} then the branch @math{f_i = 0} is generated only 
 * if @math{f_i} is zero or a zero divisor modulo @var{ideal}.
 * 
 * The initial and the separants of @math{r} are not stored in @math{S}.
 * Polynomials are supposed to have coefficients in @var{K}.
 */

BAD_DLL void
bad_complete_quadruple (
    bad_tableof_quadruple tabG,
    bap_polynom_mpz r,
    bad_regchain ideal,
    bad_base_field K,
    bad_selection_strategy strategy,
    bad_splitting_tree tree)
{
  struct bad_quadruple *G;
  struct bad_intersectof_regchain *tabC;
  struct bad_quench_map map;
  struct bav_variable *v;
  ba0_int_p k, l;
  bool first_loop;
  struct ba0_mark M;

  G = tabG->tab[tabG->size - 1];
  v = bap_leader_polynom_mpz (r);
/* 
 * A copy of r is inserted at index j in A (= G->A).
 * A->tab [A->size .. l-1] = the polynomials thrown away from A 
 *  due to the insertion of r, in order to keep it differentially
 *  triangular
 */
  bad_insert_in_regchain (&G->A, r, &k, &l);
/*
 * The triangular set A is transformed into finitely many regular chains
 */
  tabC = bad_new_intersectof_regchain ();
  ba0_realloc_table ((ba0_table) & tabC->inter, 1);
  tabC->inter.tab[0] = &G->A;
  tabC->inter.size = 1;

  ba0_push_another_stack ();
  ba0_record (&M);
  bad_init_from_complete_quench_map (&map, k, &G->A);
  ba0_pull_stack ();

  bad_quench_and_handle_exceptions_regchain (tabC, &map, ideal, K);

  ba0_realloc2_table ((ba0_table) tabG,
      tabG->size + tabC->inter.size - 1,
      (ba0_new_function *) & bad_new_quadruple);

  first_loop = true;
  tabG->size -= 1;
  for (int j = 0; j < tabC->inter.size; j++)
    {
      struct bad_quadruple *H;
      if (first_loop)
        {
          H = G;
          first_loop = false;
        }
      else
        H = bad_new_quadruple ();

      bad_set_as_child2_quadruple (H, G, tabC->inter.tab[j],
          bad_regularisation_edge, tree);
      tabG->tab[tabG->size] = H;
      tabG->size += 1;

      if (bad_defines_a_differential_ideal_attchain (&G->A.attrib))
        {
/*
 * In the differential case, 
 *    o the list D of critical pairs is updated,
 *    o the elements of S are partially reduced w.r.t. r
 *
 * Observe that r = H->decision_system.tab [k] may have been
 *  modified by the quenching process
 */
          if (bav_global.R.ders.size == 1)
            {
/*
 * Ordinary case
 */
              if (l != G->A.decision_system.size)
                {
                  struct bad_critical_pair *pair;

                  pair = bad_new_critical_pair_polynom_mpz
                      (H->A.decision_system.tab[k],
                      G->A.decision_system.tab[l - 1]);

                  H->D = (bad_listof_critical_pair) ba0_insert2_list
                      (pair, (struct ba0_list *) G->D,
                      (ba0_cmp2_function *) &
                      bad_is_a_simpler_critical_pair, strategy);
                }
            }
          else
/*
 * Partial case
 */
            bad_update_D (G, l, H->A.decision_system.tab[k], strategy);
          if (!bad_partially_reduce_S (H, K))
            tabG->size -= 1;
        }
    }

  ba0_restore (&M);
}

/*
 *    Insert r in A.
 *    If A involves an element with the same leader as r then this
 * element is overwritten with r.
 *    Otherwise, a copy of r is inserted at the right place in A.
 *    The index of r in A is stored in *k.
 * 
 *    In the differential case, some polynomials may be thrown away
 * from A (the ones the leader of which is a derivative of the leader
 * of r). 
 *    These polynomials, which may be needed by the calling function,
 * are stored at the end of A (at indices > A->decision_system.size).
 * The first index after the last of these polynomials is stored in *l.
 * 
 *    At the end we therefore have
 * 
 * 			+------------------+-------------------+
 * A->decision_system	| kept pols.  r    | thrown away pols  |
 * 			+------------------+-------------------+
 * 				      ^     ^			^
 * 				      *k    size		*l
 * 
 *    Quenching is not called so that the resulting A is not yet a
 * regular chain.
 */

static void
bad_insert_in_regchain (
    bad_regchain A,
    bap_polynom_mpz r,
    ba0_int_p *k,
    ba0_int_p *l)
{
  bav_variable u, v = BAV_NOT_A_VARIABLE;
  ba0_int_p i, old_size, new_size;
  bool found;
  ba0_mpz_t *lc;

  u = bap_leader_polynom_mpz (r);

  if (u->root->type != bav_dependent_symbol &&
      u->root->type != bav_temporary_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  old_size = A->decision_system.size;
  if (bad_defines_a_differential_ideal_attchain (&A->attrib))
    {
      for (i = A->decision_system.size - 1; i >= 0; i--)
        {
          v = bap_leader_polynom_mpz (A->decision_system.tab[i]);
          if (bav_is_proper_derivative (v, u))
            ba0_delete_table ((ba0_table) & A->decision_system, i);
        }
    }
  new_size = A->decision_system.size;
/*
 * We now have
 *	+---------------------------+----------------+
 *   A  | polynomials kept in A     | thrown away    |
 *      +---------------------------+----------------+
 *                                   size             old_size
 */
  i = 0;
  found = false;
  while (i < new_size && !found)
    {
      v = bap_leader_polynom_mpz (A->decision_system.tab[i]);
      if (bav_R_variable_number (u) <= bav_R_variable_number (v))
        found = true;
      else
        i += 1;
    }
/*
 * The polynomial r must be inserted at index i.
 * If u = v then A->decision_system.tab [i] is overwritten else a part
 * of A->decision_system must be shifted to the right.
 */
  if (k != (ba0_int_p *) 0)
    *k = i;

  if (found && u == v)
    {
      bap_set_polynom_mpz (A->decision_system.tab[i], r);
      if (l != (ba0_int_p *) 0)
        *l = old_size;
    }
  else
    {
/*
 * Creates a new entry and moves it at index i (shifting to the
 * right, all the elements of A at index greater than or equal to i).
 */
      A->decision_system.size = old_size;
      bad_realloc_regchain (A, A->decision_system.size + 1);
      A->decision_system.size += 1;
      ba0_move_from_tail_table
          ((ba0_table) & A->decision_system,
          (ba0_table) & A->decision_system, i);
      bap_set_polynom_mpz (A->decision_system.tab[i], r);
      A->decision_system.size = new_size + 1;

      if (l != (ba0_int_p *) 0)
        *l = old_size + 1;
    }
/*
 * Should be useless
 */
  lc = bap_numeric_initial_polynom_mpz (A->decision_system.tab[i]);
  if (ba0_mpz_sgn (*lc) < 0)
    bap_neg_polynom_mpz (A->decision_system.tab[i], A->decision_system.tab[i]);
}

/*
 * Updates the list D of G in the case of PDE.
 *
 * The thrown away elements of A are located in A->tab [A->size .. l-1].
 */

static void
bad_update_D (
    bad_quadruple G,
    ba0_int_p l,
    bap_polynom_mpz r,
    bad_selection_strategy strategy)
{
  bad_listof_critical_pair cour;
  bad_critical_pair pair;
  struct bav_rank rkp, rkq;
  bav_variable u, v;
  ba0_int_p i;
/*
 * One throws away non reduction critical pairs which involve one of
 *	the thrown away polynomials.
 *
 * remove = true if the pair is a triangular pair involving one of 
 * the thrown away elements.
 */
  cour = G->D;
  while (cour != (bad_listof_critical_pair) 0)
    {
      pair = cour->value;
      if (!bad_is_a_reduction_critical_pair (pair))
        {
          rkp = bap_rank_polynom_mpz (&pair->p);
          rkq = bap_rank_polynom_mpz (&pair->q);
          if (!bad_is_rank_of_regchain (&rkp, &G->A, (ba0_int_p *) 0)
              || !bad_is_rank_of_regchain (&rkq, &G->A, (ba0_int_p *) 0))
            pair->tag = bad_rejected_easy_critical_pair;
        }
      cour = cour->next;
    }
/*
 * One now generates all the new critical pairs between r and all the
 * former elements of A (apart the possible one which had the same leader
 * as r).
 */
  u = bap_leader_polynom_mpz (r);
  for (i = 0; i < l; i++)
    {
      v = bap_leader_polynom_mpz (G->A.decision_system.tab[i]);
      if (u != v && u->root == v->root)
        {
          pair = bad_new_critical_pair_polynom_mpz
              (r, G->A.decision_system.tab[i]);
          G->D = (bad_listof_critical_pair) ba0_cons_list
              (pair, (ba0_list) G->D);
        }
    }
/*
 * The list of critical pairs is now sorted by increasing order.
 * The simplest pairs to process occur at the beginning of the list
 *
 * The tagged pairs have a penalty.
 */
  G->D = (bad_listof_critical_pair) ba0_sort2_list
      ((ba0_list) G->D,
      (ba0_cmp2_function *) & bad_is_a_simpler_critical_pair, strategy);
}

/*
 * Reduces S partially w.r.t. A.
 * Returns false if some element of S simplifies to zero.
 */

static bool
bad_partially_reduce_S (
    bad_quadruple G,
    bad_base_field K)
{
  bap_listof_polynom_mpz prec, cour, rmov;
  struct bap_product_mpz prod;
  ba0_int_p i;
  bool consistent;
  struct ba0_mark M;
/*
 * One first removes from S all the non partially reduced elements.
 * These discarded elements are stored in the list rmov.
 */
  prec = (bap_listof_polynom_mpz) 0;
  cour = G->S;
  rmov = (bap_listof_polynom_mpz) 0;
  while (cour != (bap_listof_polynom_mpz) 0)
    {
      if (bad_is_a_partially_reduced_polynom_wrt_regchain (cour->value, &G->A))
        {
          prec = cour;
          cour = cour->next;
        }
      else
        {
          if (prec == (bap_listof_polynom_mpz) 0)
            G->S = cour->next;
          else
            prec->next = cour->next;
          cour->next = rmov;
          rmov = cour;
          if (prec == (bap_listof_polynom_mpz) 0)
            cour = G->S;
          else
            cour = prec->next;
        }
    }
/*
 * One then reduces each element of rmov partially w.r.t. A
 * and stores the factors of the so obtained products in S.
 */
  ba0_push_another_stack ();
  ba0_record (&M);
  bap_init_product_mpz (&prod);
  consistent = true;
  while (rmov != (bap_listof_polynom_mpz) 0 && consistent)
    {
      bad_reduce_polynom_by_regchain
          (&prod, (bap_product_mpz) 0, rmov->value, &G->A,
          bad_partial_reduction, bad_all_derivatives_to_reduce);
/*
 * Modified Dec/11 2008. Led to a modification of test/inclusion.c
 */
      consistent = !bap_is_zero_product_mpz (&prod);

      ba0_pull_stack ();
      for (i = 0; i < prod.size && consistent; i++)
        consistent = bad_simplify_and_store_in_S_quadruple
            (G, &prod.tab[i].factor, K);
      ba0_push_another_stack ();
      rmov = rmov->next;
    }

  ba0_pull_stack ();
  ba0_restore (&M);

  return consistent;
}
