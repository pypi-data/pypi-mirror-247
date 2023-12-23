#include "bad_regchain.h"
#include "bad_quench_regchain.h"
#include "bad_regularize.h"
#include "bad_intersectof_regchain.h"
#include "bad_reduction.h"
#include "bad_global.h"
#include "bad_invert.h"

/****************************************************************************
 CONSTRUCTORS AND RELATED FUNCTIONS
 ****************************************************************************/

/*
 * texinfo: bad_init_regchain
 * Initialize @var{C} to the empty chain.
 */

BAD_DLL void
bad_init_regchain (
    bad_regchain C)
{
  C->number = -1;
  bad_init_attchain (&C->attrib);
  ba0_init_table ((ba0_table) & C->decision_system);
/*
    ba0_init_table ((ba0_table)&C->simplification_system);
*/
}

/*
 * texinfo: bad_reset_regchain
 * Reset @var{C} to the empty chain.
 */

BAD_DLL void
bad_reset_regchain (
    bad_regchain C)
{
  bad_reset_attchain (&C->attrib);
  ba0_reset_table ((ba0_table) & C->decision_system);
/*
    ba0_reset_table ((ba0_table)&C->simplification_system);
*/
}

/*
 * texinfo: bad_new_regchain
 * Allocate a new regular chain, initialize it and return it.
 */

BAD_DLL bad_regchain
bad_new_regchain (
    void)
{
  bad_regchain C;

  C = (bad_regchain) ba0_alloc (sizeof (struct bad_regchain));
  bad_init_regchain (C);
  return C;
}

/*
 * texinfo: bad_realloc_regchain
 * Realloc the decision system of @var{C} so that
 * it can receive at least @var{n} polynomials.
 * Existing elements are preserved.
 */

BAD_DLL void
bad_realloc_regchain (
    bad_regchain C,
    ba0_int_p n)
{
  ba0_realloc2_table
      ((ba0_table) & C->decision_system, n,
      (ba0_new_function *) & bap_new_polynom_mpz);
/*
    ba0_realloc2_table
	((ba0_table)&C->simplification_system, m,
				(ba0_new_function*)&bap_new_polynom_mpz);
*/
}

/*
 * texinfo: bad_set_regchain
 * Assign @var{B} to @var{A}.
 */

BAD_DLL void
bad_set_regchain (
    bad_regchain A,
    bad_regchain B)
{
  ba0_int_p i;

  if (A == B)
    return;

  bav_R_push_ordering (B->attrib.ordering);

  bad_realloc_regchain (A, B->decision_system.size);
  for (i = 0; i < B->decision_system.size; i++)
    bap_set_polynom_mpz (A->decision_system.tab[i], B->decision_system.tab[i]);
  A->decision_system.size = B->decision_system.size;
/*
    for (i = 0; i < B->simplification_system.size; i++)
	bap_set_polynom_mpz (A->simplification_system.tab [i],
					B->simplification_system.tab [i]);
    A->simplification_system.size = B->simplification_system.size;
*/
  bad_set_attchain (&A->attrib, &B->attrib);

  bav_R_pull_ordering ();
}

/*
 * Given to qsort, this function sorts a table of polynomials, in 
 * increasing order.
 */

static int
bad_comp_for_increasing (
    const void *PP,
    const void *QQ)
{
  bap_polynom_mpz P = *(bap_polynom_mpz *) PP;
  bap_polynom_mpz Q = *(bap_polynom_mpz *) QQ;

  if (bap_lt_rank_polynom_mpz (P, Q))
    return -1;
  else if (bap_equal_rank_polynom_mpz (P, Q))
    return 0;
  else
    return 1;
}

/*
 * texinfo: bad_fast_primality_test_regchain
 * Set the @code{bad_prime_ideal_property} of @var{C}, if @var{C}
 * is proved (after a fast test) to define a prime ideal.
 */

BAD_DLL void
bad_fast_primality_test_regchain (
    bad_regchain C)
{
  if (C->decision_system.size > 0 && bad_is_explicit_regchain (C))
    bad_set_property_attchain (&C->attrib, bad_prime_ideal_property);
  else if (C->decision_system.size == 0)
    bad_clear_property_attchain (&C->attrib, bad_prime_ideal_property);
}

/*
 * C must be [non empty,] free of independent polynomials, triangular
 * differential => differentially triangular
 */

static void
bad_check_consistency_regchain (
    bad_regchain C)
{
  bav_variable u, v;
  ba0_int_p i, j;
/*
    if (C->decision_system.size == 0)
	BA0_RAISE_EXCEPTION (BAD_ERRNRC);
*/
  for (i = 0; i < C->decision_system.size; i++)
    if (bap_is_independent_polynom_mpz
        (C->decision_system.tab[i], (bav_tableof_parameter) 0))
      BA0_RAISE_EXCEPTION (BAD_ERRNRC);

  for (i = 0; i < C->decision_system.size; i++)
    {
      u = bap_leader_polynom_mpz (C->decision_system.tab[i]);
      for (j = i + 1; j < C->decision_system.size; j++)
        {
          v = bap_leader_polynom_mpz (C->decision_system.tab[j]);
          if (u == v)
            BA0_RAISE_EXCEPTION (BAD_ERRNRC);
          if (bad_defines_a_differential_ideal_regchain (C) &&
              (bav_is_derivative (u, v) || bav_is_derivative (v, u)))
            BA0_RAISE_EXCEPTION (BAD_ERRNRC);
        }
    }
}

/*
 * texinfo: bad_remove_zero_derivatives_of_tableof_parameter_from_regchain
 * Remove from @var{D}, the equations which state
 * that some derivatives of the elements of @var{P} are zero. 
 * Result in @var{C}. This function is used when printing regular chains.
 */

BAD_DLL void
bad_remove_zero_derivatives_of_tableof_parameter_from_regchain (
    bad_regchain C,
    bad_regchain D,
    bav_tableof_parameter P)
{
  struct bav_tableof_variable nulles;
  bav_variable v;
  ba0_int_p i;
  struct ba0_mark M;

  if (C != D)
    bad_set_regchain (C, D);

  ba0_record (&M);
  ba0_init_table ((ba0_table) & nulles);
  bav_zero_derivatives_of_tableof_parameter (&nulles, P);

  bav_R_mark_variables (false);
  for (i = 0; i < nulles.size; i++)
    nulles.tab[i]->hack = true;
  for (i = C->decision_system.size - 1; i >= 0; i--)
    {
      v = bap_leader_polynom_mpz (C->decision_system.tab[i]);
      if (v->hack)
        ba0_delete_table ((ba0_table) & C->decision_system, i);
    }
  ba0_restore (&M);
}

static void
bad_set_and_extend_regchain_tableof_polynom_mpz_all_parameters (
    bad_regchain C,
    bap_tableof_polynom_mpz T,
    bav_tableof_parameter P,
    ba0_tableof_string properties,
    bool pretend,
    bad_base_field K)
{
  ba0_int_p i;
/*
 * Set. T may be C->decision_system. T may also be zero.
 */
  if (&C->decision_system != T)
    {
      if (T == (bap_tableof_polynom_mpz) 0)
        C->decision_system.size = 0;
      else
        {
          bad_realloc_regchain (C, T->size);
          for (i = 0; i < T->size; i++)
            bap_set_polynom_mpz (C->decision_system.tab[i], T->tab[i]);
          C->decision_system.size = T->size;
        }
    }
/*
 * Extend. Then free Q.
 */
  if (P != (bav_tableof_parameter) 0)
    bap_zero_derivatives_of_tableof_parameter_mpz (&C->decision_system, P);
/*
 * Sort decision_system before checking
 */
  qsort (C->decision_system.tab, C->decision_system.size,
      sizeof (bap_polynom_mpz), &bad_comp_for_increasing);
/*
 * Set the properties (+ automatic)
 */
  bad_set_properties_attchain (&C->attrib, properties);
  bad_set_automatic_properties_attchain (&C->attrib);

  if (!pretend)
    {
      struct bad_quench_map map;
      struct ba0_mark M;

      bad_check_consistency_regchain (C);

      ba0_push_another_stack ();
      ba0_record (&M);
      bad_init_quench_map (&map, C);
      ba0_pull_stack ();

      bad_quench_regchain (C, C, &map, K, (bap_polynom_mpz *) 0);

      ba0_restore (&M);
    }
}

static void
bad_set_and_extend_regchain_tableof_polynom_mpz_necessary_parameters (
    bad_regchain C,
    bap_tableof_polynom_mpz T,
    bav_tableof_parameter P,
    ba0_tableof_string properties,
    bool pretend,
    bad_base_field K)
{
  struct bav_tableof_parameter Q;
  struct ba0_mark M;
  ba0_int_p i;
/*
 * Compute the parameters of P, actually involved in T
 */
  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_table ((ba0_table) & Q);
  if (P != (bav_tableof_parameter) 0)
    {
      if (T != (bap_tableof_polynom_mpz) 0)
        {
          for (i = 0; i < T->size; i++)
            bap_involved_parameters_polynom_mpz (&Q, T->tab[i], P);
        }
    }
  ba0_pull_stack ();
  bad_set_and_extend_regchain_tableof_polynom_mpz_all_parameters
      (C, T, &Q, properties, pretend, K);
  ba0_restore (&M);
}

/*
 * texinfo: bad_set_and_extend_regchain_tableof_polynom_mpz
 * Assign to @var{C} the table @var{T} with properties
 * given in @var{properties} plus some other ones
 * (see @code{bad_set_automatic_properties_attchain}).
 * 
 * For some parameters of @var{P}, some equations @math{p = 0}, stating
 * that some derivatives of these parameters are zero, are appended
 * to @var{C} (if @var{allpars} is true, all parameters of @var{P} are
 * concerned else, only the parameters of @var{P} which occur in @var{T}
 * are concerned).
 * In any case, the function does not generate 
 * any equation @math{p = 0} such that @math{p} is the derivative of the leader 
 * of some existing element of @var{T}.
 * 
 * The table @var{T} does not need to be sorted.
 * the table @var{T} may be the @code{decision_system} field of @var{C}
 * (this feature permits to extend an already existing regular chain).
 * 
 * If the boolean @var{pretend} is @code{true} then that's all.
 * 
 * Otherwise, the function checks that the polynomials depend
 * on dependent variables and form a triangular set (and a 
 * differentially triangular one in the differential case).
 * If they do not, exception @code{BAD_ERRNRC} is raised.
 * 
 * Last, the function @code{bad_quench_regchain} is called to make the regular
 * chain hold the properties with the exception of the
 * coherence, prime ideal and differential ideal properties. 
 * This function may raise the exceptions @code{BAD_EXRCNC}
 * or @code{BAD_EXRDDZ}.
 * 
 * The parameters @var{T}, @var{P} and @var{properties} may be zero.
 */

BAD_DLL void
bad_set_and_extend_regchain_tableof_polynom_mpz (
    bad_regchain C,
    bap_tableof_polynom_mpz T,
    bav_tableof_parameter P,
    ba0_tableof_string properties,
    bool allpars,
    bool pretend)
{
  struct bad_base_field K0;

  bad_init_base_field (&K0);
  if (allpars)
    bad_set_and_extend_regchain_tableof_polynom_mpz_all_parameters
        (C, T, P, properties, pretend, &K0);
  else
    bad_set_and_extend_regchain_tableof_polynom_mpz_necessary_parameters
        (C, T, P, properties, pretend, &K0);
}

/*
 * texinfo: bad_set_and_extend_regchain_tableof_ratfrac_mpz
 * Apply @code{bad_set_and_extend_regchain_tableof_polynom_mpz}
 * over the set of numerators of the rational fractions.
 */

BAD_DLL void
bad_set_and_extend_regchain_tableof_ratfrac_mpz (
    bad_regchain C,
    baz_tableof_ratfrac T,
    bav_tableof_parameter P,
    ba0_tableof_string properties,
    bool allpars,
    bool pretend)
{
  struct baz_ratfrac R;
  struct ba0_mark M;
  ba0_int_p i;

  ba0_push_another_stack ();
  ba0_record (&M);
  baz_init_ratfrac (&R);
  ba0_pull_stack ();

  bad_realloc_regchain (C, T->size);
  for (i = 0; i < T->size; i++)
    {
      ba0_push_another_stack ();
      baz_reduce_ratfrac (&R, T->tab[i]);
      ba0_pull_stack ();
      baz_numer_ratfrac (C->decision_system.tab[i], &R);
    }
  C->decision_system.size = T->size;

  bad_set_and_extend_regchain_tableof_polynom_mpz
      (C, &C->decision_system, P, properties, allpars, pretend);
}

/*
 * texinfo: bad_set_number_regchain
 * Assign @var{number} to the field @code{number} of @var{C}.
 */

BAD_DLL void
bad_set_number_regchain (
    bad_regchain C,
    ba0_int_p number)
{
  C->number = number;
}

/*
 * texinfo: bad_set_property_regchain
 * Set property @var{prop} of @var{C}.
 */

BAD_DLL void
bad_set_property_regchain (
    bad_regchain C,
    enum bad_property_attchain prop)
{
  bad_set_property_attchain (&C->attrib, prop);
}

/*
 * texinfo: bad_set_properties_regchain
 * Set the properties of @var{C} with @var{T}.
 * Do not set properties automatically 
 * (see @code{bad_set_automatic_properties_attchain}).
 */

BAD_DLL void
bad_set_properties_regchain (
    bad_regchain C,
    ba0_tableof_string T)
{
  bad_set_properties_attchain (&C->attrib, T);
}

/*
 * texinfo: bad_has_property_regchain
 * Return @code{true} if @var{C} has the property @var{P}.
 */

BAD_DLL bool
bad_has_property_regchain (
    bad_regchain C,
    enum bad_property_attchain P)
{
  return bad_has_property_attchain (&C->attrib, P);
}

/*
 * texinfo: bad_defines_a_differential_ideal_regchain
 * Return @code{true} if @var{C} holds the 
 * @code{bad_differential_ideal_property} else @code{false}.
 */

BAD_DLL bool
bad_defines_a_differential_ideal_regchain (
    bad_regchain C)
{
  return bad_defines_a_differential_ideal_attchain (&C->attrib);
}

/*
 * texinfo: bad_defines_a_prime_ideal_regchain
 * Return @code{true} 
 * if @var{C} holds the @code{bad_prime_ideal_property}
 * else @code{false}.
 */

BAD_DLL bool
bad_defines_a_prime_ideal_regchain (
    bad_regchain C)
{
  return bad_defines_a_prime_ideal_attchain (&C->attrib);
}

/*
 * texinfo: bad_sort_regchain
 * Assign to @var{A} the regular chain obtained by sorting the polynomials
 * of @var{B} w.r.t. the current ordering. The elements of @var{A} are readonly.
 * Properties of @var{B} become properties of @var{A}.
 */

BAD_DLL void
bad_sort_regchain (
    bad_regchain A,
    bad_regchain B)
{
  ba0_int_p i;

  if (A != B)
    {
      bad_reset_regchain (A);
      bad_realloc_regchain (A, B->decision_system.size);
      for (i = 0; i < B->decision_system.size; i++)
        bap_sort_polynom_mpz
            (A->decision_system.tab[i], B->decision_system.tab[i]);
      A->decision_system.size = B->decision_system.size;
/*
	for (i = 0; i < B->simplification_system.size; i++)
	    bap_sort_polynom_mpz 
		(A->simplification_system.tab [i], 
					B->simplification_system.tab [i]);
	A->simplification_system.size = B->simplification_system.size;
*/
      A->attrib.ordering = bav_R_Iordering ();
      A->attrib.property = B->attrib.property;
    }
  else
    {
      for (i = 0; i < A->decision_system.size; i++)
        bap_sort_polynom_mpz
            (A->decision_system.tab[i], A->decision_system.tab[i]);
/*
        for (i = 0; i < A->simplification_system.size; i++)
	    bap_sort_polynom_mpz 
		(A->simplification_system.tab [i], 
					A->simplification_system.tab [i]);
*/
      A->attrib.ordering = bav_R_Iordering ();
    }
}

/*
 * texinfo: bad_inequations_regchain
 * Assign to @var{res} the initials and separants of @var{C}.
 * Numeric polynomials are discarded. 
 * Polynomials are made primitive. 
 * Redundant polynomials are discarded.
 * Some polynomials may be factored by means of
 * @code{baz_factor_easy_polynom_mpz}.
 */

BAD_DLL void
bad_inequations_regchain (
    bap_tableof_polynom_mpz res,
    bad_regchain C)
{
  struct bap_tableof_polynom_mpz ineqs;
  struct bap_polynom_mpz init, sep;
  struct bap_product_mpz prod;
  struct ba0_mark M;
  ba0_int_p i, k, l;
  bool found;

  ba0_push_another_stack ();
  ba0_record (&M);
  bap_init_product_mpz (&prod);
  bap_init_readonly_polynom_mpz (&init);
  bap_init_polynom_mpz (&sep);
  ba0_init_table ((ba0_table) & ineqs);

  for (i = 0; i < C->decision_system.size; i++)
    {
      bap_initial_polynom_mpz (&init, C->decision_system.tab[i]);
      if (!bap_is_numeric_polynom_mpz (&init))
        {
          baz_factor_easy_polynom_mpz (&prod, &init, 0);
          for (k = 0; k < prod.size; k++)
            {
              found = false;
              for (l = 0; l < ineqs.size && !found; l++)
                found = bap_equal_polynom_mpz
                    (&prod.tab[k].factor, ineqs.tab[l]);
              if (!found)
                {
                  if (ineqs.size >= ineqs.alloc)
                    ba0_realloc2_table
                        ((ba0_table) & ineqs, 2 * ineqs.size + 1,
                        (ba0_new_function *) & bap_new_polynom_mpz);
                  bap_set_polynom_mpz
                      (ineqs.tab[ineqs.size], &prod.tab[k].factor);
                  ineqs.size += 1;
                }
            }
        }
    }
  for (i = 0; i < C->decision_system.size; i++)
    {
      if (bap_leading_degree_polynom_mpz (C->decision_system.tab[i]) > 1)
        {
          bap_separant_polynom_mpz (&sep, C->decision_system.tab[i]);
          bap_normal_numeric_primpart_polynom_mpz (&sep, &sep);
          found = false;
          for (l = 0; l < ineqs.size && !found; l++)
            {
              if (bap_is_factor_polynom_mpz (&sep, ineqs.tab[l], &sep))
                found = bap_is_numeric_polynom_mpz (&sep);
            }
          if (!found)
            {
              if (ineqs.size >= ineqs.alloc)
                ba0_realloc2_table
                    ((ba0_table) & ineqs, 2 * ineqs.size + 1,
                    (ba0_new_function *) & bap_new_polynom_mpz);
              bap_set_polynom_mpz (ineqs.tab[ineqs.size], &sep);
              ineqs.size += 1;
            }
        }
    }

  ba0_pull_stack ();

  res->size = 0;
  ba0_realloc2_table ((ba0_table) res, ineqs.size,
      (ba0_new_function *) & bap_new_polynom_mpz);
  for (i = 0; i < ineqs.size; i++)
    {
      bap_set_polynom_mpz (res->tab[res->size], ineqs.tab[i]);
      res->size += 1;
    }
  ba0_restore (&M);
}

/*
 * texinfo: bad_scanf_regchain
 * A parsing function for regular chains.
 * It is called by @code{ba0_scanf/%regchain}.
 * The parsed string is expected to have the form
 * @code{regchain ([rational fractions], [properties])}.
 * The function checks that the numerators of @var{ratfrac} 
 * form a regular chain.
 * It calls @code{bad_quench_regchain} to make the chain
 * satisfy the properties listed in @var{property}
 * except the coherence, prime ideal and differential ideal properties.
 * The input table @var{ratfrac} needs not be sorted.
 */

BAD_DLL void *
bad_scanf_regchain (
    void *A)
{
  bad_regchain C;
  baz_tableof_ratfrac ratfrac;
  ba0_tableof_string properties;
  struct ba0_mark M;

  if (A == (void *) 0)
    C = bad_new_regchain ();
  else
    {
      C = (bad_regchain) A;
      bad_reset_attchain (&C->attrib);
    }

  ba0_push_another_stack ();
  ba0_record (&M);
  ratfrac = (baz_tableof_ratfrac) ba0_new_table ();
  properties = (ba0_tableof_string) ba0_new_table ();
  ba0_scanf ("regchain (%t[%Qz], %t[%s])", ratfrac, properties);
  ba0_pull_stack ();
  bad_set_and_extend_regchain_tableof_ratfrac_mpz
      (C, ratfrac, (bav_tableof_parameter) 0, properties, true, false);
  ba0_restore (&M);
  return C;
}

/*
 * texinfo: bad_scanf_pretend_regchain
 * A parsing function for regular chains.
 * It is called by @code{ba0_scanf/%pretend_regchain}.
 * The parsed string is expected to have the form
 * @code{regchain ([rational fractions], [properties])}.
 * No test is performed.
 * The input table @var{ratfrac} needs not be sorted.
 */

BAD_DLL void *
bad_scanf_pretend_regchain (
    void *A)
{
  bad_regchain C;
  baz_tableof_ratfrac ratfrac;
  ba0_tableof_string properties;
  struct ba0_mark M;

  if (A == (void *) 0)
    C = bad_new_regchain ();
  else
    {
      C = (bad_regchain) A;
      bad_reset_attchain (&C->attrib);
    }

  ba0_push_another_stack ();
  ba0_record (&M);
  ratfrac = (baz_tableof_ratfrac) ba0_new_table ();
  properties = (ba0_tableof_string) ba0_new_table ();
  ba0_scanf ("regchain (%t[%Qz], %t[%s])", ratfrac, properties);
  ba0_pull_stack ();
  bad_set_and_extend_regchain_tableof_ratfrac_mpz
      (C, ratfrac, (bav_tableof_parameter) 0, properties, true, true);
  ba0_restore (&M);
  return C;
}

/*
 * texinfo: bad_printf_regchain
 * A printing function for regular chains.
 * it is called by @code{ba0_printf/%regchain}.
 * The output format is 
 * @code{regchain ([rational fractions], [properties])}.
 */

BAD_DLL void
bad_printf_regchain (
    void *A)
{
  bad_regchain C = (bad_regchain) A;
  ba0_tableof_string P;
  struct ba0_mark M;

  ba0_record (&M);

  P = (ba0_tableof_string) ba0_new_table ();
  bad_properties_attchain (P, &C->attrib);
  ba0_printf ("regchain (%t[%Az], %t[%s])", &C->decision_system, P);

  ba0_restore (&M);
}

/*
 * texinfo: bad_printf_regchain_equations
 * A printing function for regcular chains.
 * It is called by @code{ba0_printf/%regchain_equations}.
 * The output format is the one of a table of polynomials.
 */

BAD_DLL void
bad_printf_regchain_equations (
    void *A)
{
  bad_regchain C = (bad_regchain) A;

  ba0_printf ("%t[%Az]", &C->decision_system);
}

/*
 * Readonly static data
 */

static char _regchain[] = "struct bad_regchain";
static char _regchain_decision[] = "bad_regchain->decision_system.tab";

BAD_DLL ba0_int_p
bad_garbage1_regchain (
    void *A,
    enum ba0_garbage_code code)
{
  bad_regchain C = (bad_regchain) A;
  ba0_int_p i, n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (C, sizeof (struct bad_regchain), _regchain);

  if (C->decision_system.alloc > 0)
    {
      n += ba0_new_gc_info
          (C->decision_system.tab,
          C->decision_system.alloc * sizeof (bap_polynom_mpz),
          _regchain_decision);

      for (i = 0; i < C->decision_system.alloc; i++)
        n += bap_garbage1_polynom_mpz (C->decision_system.tab[i], ba0_isolated);
    }
/*
    if (C->simplification_system.alloc > 0)
    {	n += ba0_new_gc_info 
		(C->simplification_system.tab,
		 C->simplification_system.alloc * sizeof(bap_polynom_mpz),
		 "bad_regchain->simplification_system.tab");

	for (i = 0; i < C->simplification_system.alloc; i++)
	    n += bap_garbage1_polynom_mpz 
			(C->simplification_system.tab [i], ba0_isolated);
    }
*/
  return n;
}

BAD_DLL void *
bad_garbage2_regchain (
    void *A,
    enum ba0_garbage_code code)
{
  bad_regchain C;
  ba0_int_p i;

  if (code == ba0_isolated)
    C = (bad_regchain) ba0_new_addr_gc_info (A, _regchain);
  else
    C = (bad_regchain) A;

  if (C->decision_system.alloc > 0)
    {
      C->decision_system.tab =
          (bap_polynom_mpz *)
          ba0_new_addr_gc_info (C->decision_system.tab, _regchain_decision);

      for (i = 0; i < C->decision_system.alloc; i++)
        C->decision_system.tab[i] = bap_garbage2_polynom_mpz
            (C->decision_system.tab[i], ba0_isolated);
    }
/*
    if (C->simplification_system.alloc > 0)
    {	C->simplification_system.tab = (bap_polynom_mpz*)ba0_new_addr_gc_info
	    (C->simplification_system.tab, 
	     "bad_regchain->simplification_system.tab");

	for (i = 0; i < C->simplification_system.alloc; i++)
	    C->simplification_system.tab [i] =
		bap_garbage2_polynom_mpz 
			(C->simplification_system.tab [i], ba0_isolated);
    }
*/
  return C;
}

BAD_DLL void *
bad_copy_regchain (
    void *A)
{
  bad_regchain B, C = (bad_regchain) A;

  B = bad_new_regchain ();
  bad_set_regchain (B, C);
  return B;
}

/****************************************************************************
 PREDICATES
 ****************************************************************************/


/*
 * texinfo: bad_is_rank_of_regchain
 * Return @code{true} if @var{rg} is the rank of some element of @var{C}.
 * If so and @var{i} is not the zero pointer, @var{i} receives the index of 
 * the element.
 */

BAD_DLL bool
bad_is_rank_of_regchain (
    bav_rank rg,
    bad_regchain C,
    ba0_int_p *i)
{
  ba0_int_p k;
  bool b;

  bav_R_push_ordering (C->attrib.ordering);
  if (!bad_is_leader_of_regchain (rg->var, C, &k))
    b = false;
  else if (rg->deg != bap_leading_degree_polynom_mpz
      (C->decision_system.tab[k]))
    b = false;
  else
    {
      if (i != (ba0_int_p *) 0)
        *i = k;
      b = true;
    }
  bav_R_pull_ordering ();
  return b;
}

/*
 * texinfo: bad_is_leader_of_regchain
 * Return @code{true} if @var{v} is the leading derivative of some
 * element of @var{C}. 
 * If so and @var{i} is not the zero pointer, @var{i} receives the index of
 * the element.
 */

BAD_DLL bool
bad_is_leader_of_regchain (
    bav_variable v,
    bad_regchain C,
    ba0_int_p *i)
{
  bool b;
  ba0_int_p k;

  bav_R_push_ordering (C->attrib.ordering);
  b = false;
  for (k = 0; (!b) && k < C->decision_system.size; k++)
    {
      if (v == bap_leader_polynom_mpz (C->decision_system.tab[k]))
        {
          if (i != (ba0_int_p *) 0)
            *i = k;
          b = true;
        }
    }
  bav_R_pull_ordering ();
  return b;
}

/*
 * texinfo: bad_depends_on_leader_of_regchain
 * Return @code{true} if @var{A} depends on the leader of some
 * element of @var{C}, else @code{false}.
 */

BAD_DLL bool
bad_depends_on_leader_of_regchain (
    struct bap_polynom_mpz *A,
    struct bad_regchain *C)
{
  bool b;

  b = false;
  for (int k = 0; (!b) && k < A->total_rank.size; k++)
    b = bad_is_leader_of_regchain (A->total_rank.rg[k].var, C, (ba0_int_p *) 0);
  return b;
}

/*
 * texinfo: bad_is_derivative_of_leader_of_regchain
 * Return @code{true} if @var{v} is a derivative of the leading derivative
 * of some
 * element of @var{C}. 
 * If so and @var{i} is not the zero pointer, @var{i} receives the index of
 * the element.
 */

BAD_DLL bool
bad_is_derivative_of_leader_of_regchain (
    bav_variable v,
    bad_regchain C,
    ba0_int_p *i)
{
  bav_variable w;
  bool b;
  ba0_int_p k;

  bav_R_push_ordering (C->attrib.ordering);
  b = false;
  for (k = 0; k < C->decision_system.size && (!b); k++)
    {
      w = bap_leader_polynom_mpz (C->decision_system.tab[k]);
      if (bav_is_derivative (v, w))
        {
          if (i != (ba0_int_p *) 0)
            *i = k;
          b = true;
        }
    }
  bav_R_pull_ordering ();
  return b;
}

/*
 * texinfo: bad_is_solved_regchain
 * Return @code{true} if @var{C} could be written as
 * @math{p(x_1) = 0}, @math{x_2 = f_2(x_1)}, @dots{}, @math{x_n = f_n(x_1)}
 * where @math{p} and the @math{f_i} are polynomials.
 */

BAD_DLL bool
bad_is_solved_regchain (
    bad_regchain C)
{
  bav_variable x;
  bap_tableof_polynom_mpz T;
  ba0_int_p i;

  T = &C->decision_system;
  if (T->size == 0 || T->tab[0]->total_rank.size > 1)
    return false;
  x = bap_leader_polynom_mpz (T->tab[0]);
  for (i = 1; i < T->size; i++)
    {
      if (!bap_is_solved_polynom_mpz (T->tab[i]))
        return false;
      if (T->tab[i]->total_rank.size > 2 ||
          (T->tab[i]->total_rank.size == 2 &&
              !bap_depend_polynom_mpz (T->tab[i], x)))
        return false;
    }
  return true;
}

/*
 * texinfo: bad_is_orthonomic_regchain
 * Return @code{true} if the elements of @var{C} have leading degrees @math{1}
 * and independent initials.
 */

BAD_DLL bool
bad_is_orthonomic_regchain (
    bad_regchain C)
{
  struct bap_polynom_mpz init;
  struct ba0_mark M;
  ba0_int_p i;
  bool b;

  ba0_record (&M);
  bap_init_readonly_polynom_mpz (&init);
  b = true;
  for (i = 0; b && i < C->decision_system.size; i++)
    {
      if (bap_leading_degree_polynom_mpz (C->decision_system.tab[i]) != 1)
        b = false;
      else
        {
          bap_initial_polynom_mpz (&init, C->decision_system.tab[i]);
          b = bap_is_independent_polynom_mpz (&init, (bav_tableof_parameter) 0);
        }
    }
  ba0_restore (&M);
  return b;
}

/*
 * texinfo: bad_is_explicit_regchain
 * Return @code{true} if the elements of @var{C} have leading degrees @math{1}.
 */

BAD_DLL bool
bad_is_explicit_regchain (
    bad_regchain C)
{
  ba0_int_p i;

  for (i = 0; i < C->decision_system.size; i++)
    if (bap_leading_degree_polynom_mpz (C->decision_system.tab[i]) != 1)
      return false;
  return true;
}

/*
 * texinfo: bad_is_zero_regchain
 * Return @code{true} if @var{C} is empty.
 */

BAD_DLL bool
bad_is_zero_regchain (
    bad_regchain C)
{
  return C->decision_system.size == 0;
}

/*
 * texinfo: bad_product_of_leading_degrees_regchain
 * Return the product of the leading degrees of the elements of @var{C}.
 */

BAD_DLL ba0_int_p
bad_product_of_leading_degrees_regchain (
    bad_regchain C)
{
  ba0_int_p r, i;

  r = 1;
  for (i = 0; i < C->decision_system.size; i++)
    r *= bap_leading_degree_polynom_mpz (C->decision_system.tab[i]);
  return r;
}


/************************************************************************
 MISCELLANEOUS FUNCTIONS
 ************************************************************************/

/*
 * texinfo: bad_ordering_eliminating_leaders_of_regchain
 * Return an ordering @var{r} w.r.t. which the leaders of the elements of @var{C}
 * are greater than any other variable. The ordering is not necessarily
 * a ranking in the sense of Kolchin. The ordering between the leaders on
 * the one hand and and other variables on the other hand are preserved.
 * This function does not change the current ordering.
 */

BAD_DLL bav_Iordering
bad_ordering_eliminating_leaders_of_regchain (
    bad_regchain C)
{
  bav_Iordering r;
  ba0_int_p i;

  r = bav_R_copy_ordering (C->attrib.ordering);
  bav_R_push_ordering (r);
  for (i = 0; i < C->decision_system.size; i++)
    bav_R_set_maximal_variable
        (bap_leader_polynom_mpz (C->decision_system.tab[i]));
  bav_R_pull_ordering ();
  return r;
}

/*
 * texinfo: bad_codimension_regchain
 * Return the codimension (differential or not, depending if @var{C} holds
 * the @code{bad_differential_ideal_property}) of the ideal
 * defined by @var{C}. 
 * Differential polynomials are assumed to have coefficients in @var{K}. 
 * In the algebraic or the ODE case, the codimension is just the number
 * of equations of @var{C} which do not belong to @var{K}.
 * In the partial differential case, the equations whose leaders 
 * are derivatives of the same
 * dependent variable are counted as one equation.
 */

BAD_DLL ba0_int_p
bad_codimension_regchain (
    bad_regchain C,
    bad_base_field K)
{
  struct bav_tableof_variable T;
  bav_variable v;
  ba0_int_p i, n, codim = 0;
  struct ba0_mark M;

/*
 * The defining equations of K (i.e. K->relations) are part of
 * the equations of C. They must not be taken inbto account while
 * counting the codimension.
 */
  if (bad_has_property_regchain (C, bad_differential_ideal_property))
    {
/*
 * ODE case. It is sufficient to count the equations.
 */
      if (bav_global.R.ders.size == 1)
        {
          if (K != (bad_base_field) 0)
            n = K->relations.decision_system.size;
          else
            n = 0;
          codim = C->decision_system.size - n;
        }
      else
/*
 * PDE case. One counts the dependent variables, for which, at
 * least one derivative is a leader.
 */
        {
          ba0_record (&M);
          ba0_init_table ((ba0_table) & T);
          ba0_realloc_table ((ba0_table) & T, bav_global.R.vars.size);
          if (K != (bad_base_field) 0)
            {
              for (i = 0; i < K->relations.decision_system.size; i++)
                {
                  v = bap_leader_polynom_mpz
                      (K->relations.decision_system.tab[i]);
                  v = bav_order_zero_variable (v);
                  if (!ba0_member_table (v, (ba0_table) & T))
                    {
                      T.tab[T.size] = v;
                      T.size += 1;
                    }
                }
              n = T.size;
            }
          else
            n = 0;
/*
 * The defining equations of K are counted twice. Could be optimized.
 */
          ba0_reset_table ((ba0_table) & T);
          for (i = 0; i < C->decision_system.size; i++)
            {
              v = bap_leader_polynom_mpz (C->decision_system.tab[i]);
              v = bav_order_zero_variable (v);
              if (!ba0_member_table (v, (ba0_table) & T))
                {
                  T.tab[T.size] = v;
                  T.size += 1;
                }
            }
          ba0_restore (&M);
          codim = T.size - n;
        }
    }
  else
/*
 * Algebraic case.  It is sufficient to count the equations.
 */
    {
      if (K != (bad_base_field) 0)
        n = K->relations.decision_system.size;
      else
        n = 0;
      codim = C->decision_system.size - n;
    }
  return codim;
}

/*
 * texinfo: bad_sizeof_regchain
 * Return the size of the meory needed to perform a copy of @var{C}.
 */

BAD_DLL unsigned ba0_int_p
bad_sizeof_regchain (
    bad_regchain C)
{
  unsigned ba0_int_p size;
  ba0_int_p i;

  size = ba0_allocated_size (sizeof (struct bad_regchain));
  size += ba0_allocated_size
      (C->decision_system.size * sizeof (bap_polynom_mpz));
  for (i = 0; i < C->decision_system.size; i++)
    size += bap_sizeof_polynom_mpz (C->decision_system.tab[i]);
  return size;
}

/*
 * texinfo: bad_switch_ring_regchain
 * This low level function should be used in conjunction with 
 * @code{bav_set_differential_ring}: if @var{R} is a ring obtained by 
 * application of @code{bav_set_differential_ring}
 * to the ring @var{C} refers to, then this function makes @var{C} 
 * refer to @var{R}. The chain @var{C} is modified.
 */

BAD_DLL void
bad_switch_ring_regchain (
    bad_regchain C,
    bav_differential_ring R)
{
  ba0_int_p i;

  for (i = 0; i < C->decision_system.size; i++)
    bap_switch_ring_polynom_mpz (C->decision_system.tab[i], R);
}
