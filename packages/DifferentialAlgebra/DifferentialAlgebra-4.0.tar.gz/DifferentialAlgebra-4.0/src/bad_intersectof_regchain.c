#include "bad_intersectof_regchain.h"

/*
 * texinfo: bad_init_intersectof_regchain
 * Initialize @var{ideal} to the empty intersection.
 */

BAD_DLL void
bad_init_intersectof_regchain (
    bad_intersectof_regchain ideal)
{
  bad_init_attchain (&ideal->attrib);
  ba0_init_table ((ba0_table) & ideal->inter);
}

/*
 * texinfo: bad_new_intersectof_regchain
 * Allocate a new intersection, initialize it and return it.
 */

BAD_DLL bad_intersectof_regchain
bad_new_intersectof_regchain (
    void)
{
  bad_intersectof_regchain ideal;

  ideal = (bad_intersectof_regchain) ba0_alloc
      (sizeof (struct bad_intersectof_regchain));
  bad_init_intersectof_regchain (ideal);
  return ideal;
}

/*
 * texinfo: bad_reset_intersectof_regchain
 * Reset @var{ideal} to the empty intersection.
 */

BAD_DLL void
bad_reset_intersectof_regchain (
    bad_intersectof_regchain ideal)
{
  bad_reset_attchain (&ideal->attrib);
  ba0_reset_table ((ba0_table) & ideal->inter);
}

/*
 * texinfo: bad_realloc_intersectof_regchain
 * Realloc the table @code{inter} of @var{I} if needed in such a way that 
 * the table can receive at least @var{n} regular chains. 
 * Formerly stored regular chains are kept.
 */

BAD_DLL void
bad_realloc_intersectof_regchain (
    bad_intersectof_regchain I,
    ba0_int_p n)
{
  ba0_realloc2_table ((ba0_table) & I->inter, n,
      (ba0_new_function *) & bad_new_regchain);
}

/*
 * texinfo: bad_set_intersectof_regchain_regchain
 * Assign @var{C} to @var{I}.
 */

BAD_DLL void
bad_set_intersectof_regchain_regchain (
    bad_intersectof_regchain I,
    bad_regchain ideal)
{
  bad_set_attchain (&I->attrib, &ideal->attrib);
  bad_realloc_intersectof_regchain (I, 1);
  if (I->inter.tab[0] != ideal)
    bad_set_regchain (I->inter.tab[0], ideal);
  I->inter.size = 1;
}

/*
 * texinfo: bad_append_intersectof_regchain_regchain
 * Append the regular chain @var{ideal} to @var{I}.
 * If @var{I} is empty, assign the attributes of @var{ideal} to 
 * those of @var{I} 
 * else intersects the attributes of @var{ideal} with those of @var{I}
 * by calling @code{bad_intersect_attchain}. 
 * Exception @code{BAD_ERRIAC} may be raised.
 */

BAD_DLL void
bad_append_intersectof_regchain_regchain (
    bad_intersectof_regchain I,
    bad_regchain ideal)
{
  if (I->inter.size == 0)
    bad_set_intersectof_regchain_regchain (I, ideal);
  else
    {
      bad_realloc_intersectof_regchain (I, I->inter.size + 1);
      if (!ba0_member_table (ideal, (ba0_table) & I->inter))
        {
          bad_intersect_attchain (&I->attrib, &ideal->attrib);
          bad_set_regchain (I->inter.tab[I->inter.size++], ideal);
        }
    }
}

/*
 * texinfo: bad_append_intersectof_regchain
 * Append the regular chains of @var{J} to @var{I}.
 */

BAD_DLL void
bad_append_intersectof_regchain (
    bad_intersectof_regchain I,
    bad_intersectof_regchain J)
{
  ba0_int_p i;

  if (I != J)
    {
      bad_realloc_intersectof_regchain (I, I->inter.size + J->inter.size);
      for (i = 0; i < J->inter.size; i++)
        bad_append_intersectof_regchain_regchain (I, J->inter.tab[i]);
    }
}

/*
 * texinfo: bad_set_intersectof_regchain
 * Assign @var{J} to @var{I}.
 */

BAD_DLL void
bad_set_intersectof_regchain (
    bad_intersectof_regchain I,
    bad_intersectof_regchain J)
{
  ba0_int_p i;

  if (I != J)
    {
      bad_set_attchain (&I->attrib, &J->attrib);
      I->inter.size = 0;
      bad_realloc_intersectof_regchain (I, J->inter.size);
      for (i = 0; i < J->inter.size; i++)
        bad_set_regchain (I->inter.tab[i], J->inter.tab[i]);
      I->inter.size = J->inter.size;
    }
}

/*
 * texinfo: bad_set_properties_intersectof_regchain
 * Set the properties of @var{I} with @var{T}.
 */

BAD_DLL void
bad_set_properties_intersectof_regchain (
    bad_intersectof_regchain I,
    ba0_tableof_string P)
{
  bad_set_properties_attchain (&I->attrib, P);
}

/*
 * Comparison function for bad_sort_intersectof_regchain
 */

static int
bad_comp_regchain (
    const void *C0,
    const void *D0)
{
  struct bad_regchain *C = *(struct bad_regchain **) C0;
  struct bad_regchain *D = *(struct bad_regchain **) D0;

/*
 * first compare ranks of polynomials from bottom up
 * if C < D then it should appear later hence 1
 */
  for (int i = 0; i < C->decision_system.size && i < D->decision_system.size;
      i++)
    {
      struct bap_polynom_mpz *P = C->decision_system.tab[i];
      struct bap_polynom_mpz *Q = D->decision_system.tab[i];
      if (bap_lt_rank_polynom_mpz (P, Q))
        return 1;
      else if (bap_lt_rank_polynom_mpz (Q, P))
        return -1;
    }
/*
 * ranks are equal: compare lengths
 * the longer set is smaller
 */
  if (C->decision_system.size > D->decision_system.size)
    return 1;
  else
    return -1;
/*
 * same ranks! but coefficients may differ
 */
  for (int i = 0; i < C->decision_system.size && i < D->decision_system.size;
      i++)
    {
      struct bap_polynom_mpz *P = C->decision_system.tab[i];
      struct bap_polynom_mpz *Q = D->decision_system.tab[i];
      enum ba0_compare_code code = bap_compare_polynom_mpz (P, Q);
      if (code == ba0_lt)
        return 1;
      else if (code == ba0_gt)
        return -1;
    }
/*
 * Meaningless test, in order to have a total order
 */
  return (void *) C < (void *) D;
}

/*
 * texinfo: bad_sort_intersectof_regchain
 * Sort the regular chains of @var{J} by decreasing order. 
 * The result is stored in @var{I}.
 * Regular chains are compared following the classical ordering
 * on differentially triangular sets: ranks of polynomials are
 * compared from bottom up and, in case no difference of ranks is
 * observed, the longer set is considered as lower than the shorter one.
 * If two regular chains have the same rank, then polynomials are
 * again compared from bottom up, using @code{bap_compare_polynom_mpz}
 * to break ties.
 */

BAD_DLL void
bad_sort_intersectof_regchain (
    struct bad_intersectof_regchain *I,
    struct bad_intersectof_regchain *J)
{
  if (I != J)
    bad_set_intersectof_regchain (I, J);

  qsort (I->inter.tab, I->inter.size,
      sizeof (struct bad_regchain *), &bad_comp_regchain);
}

/*
 * texinfo: bad_remove_redundant_components_intersectof_regchain
 * Perform the inclusion test between the components of @var{J}.
 * For each regular chain @var{C}, if there exists another 
 * regular chain @var{D} such
 * that the inclusion test @math{D \subset C} is positive, then 
 * @var{C} is removed from the intersection. 
 * 
 * This function relies on @code{bad_is_included_regchain} which may fail 
 * to decide if a regchain is included in another one. The computed
 * intersection is thus not guaranteed to be minimal. Polynomials are supposed
 * to have coefficients in @var{K}.
 *
 * The resulting intersection is sorted 
 * (see @code{bad_sort_intersectof_regchain}).
 */

BAD_DLL void
bad_remove_redundant_components_intersectof_regchain (
    bad_intersectof_regchain I,
    bad_intersectof_regchain J,
    bad_base_field K)
{
  bad_sort_intersectof_regchain (I, J);
  for (int i = 1; i < I->inter.size; i++)
    {
      bool found = false;
      for (int j = 0; j < i && !found; j++)
        found = bad_is_included_regchain
            (I->inter.tab[j], J->inter.tab[i], K) ==
            bad_inclusion_test_positive;
      if (found)
        ba0_delete_table ((ba0_table) & J->inter, i);
    }
}

/*
 * texinfo: bad_fast_primality_test_intersectof_regchain
 * Apply @code{bad_fast_primality_test_regchain} over each component
 * of @var{I}. 
 */

BAD_DLL void
bad_fast_primality_test_intersectof_regchain (
    bad_intersectof_regchain ideal)
{
  ba0_int_p i;

  for (i = 0; i < ideal->inter.size; i++)
    bad_fast_primality_test_regchain (ideal->inter.tab[i]);
}

/*
 * texinfo: bad_scanf_intersectof_regchain
 * A parsing function for intersections of regular chains.
 * It is called by @code{ba0_scanf/%intersectof_regchain}.
 * It relies on @code{bad_scanf_regchain}.
 */

BAD_DLL void *
bad_scanf_intersectof_regchain (
    void *I)
{
  bad_intersectof_regchain ideal;
  ba0_tableof_string P;
  ba0_int_p i, differentiel;

  if (I == (void *) 0)
    ideal = bad_new_intersectof_regchain ();
  else
    ideal = (bad_intersectof_regchain) I;

  P = (ba0_tableof_string) ba0_new_table ();
  ba0_scanf ("intersectof_regchain (%t[%regchain], %t[%s])", &ideal->inter, P);

  bad_set_properties_attchain (&ideal->attrib, P);

  differentiel = 0;
  if (bad_defines_a_differential_ideal_attchain (&ideal->attrib))
    differentiel++;
  for (i = 0; i < ideal->inter.size; i++)
    if (bad_defines_a_differential_ideal_attchain
        (&ideal->inter.tab[i]->attrib))
      differentiel++;
  if (differentiel > 0 && differentiel < 1 + ideal->inter.size)
    BA0_RAISE_EXCEPTION (BAD_ERRIRC);

  if (bad_defines_a_prime_ideal_attchain (&ideal->attrib))
    {
      if (ideal->inter.size > 1)
        BA0_RAISE_EXCEPTION (BAD_ERRIRC);
      else if (ideal->inter.size == 1 &&
          !bad_defines_a_prime_ideal_attchain (&ideal->inter.tab[0]->attrib))
        BA0_RAISE_EXCEPTION (BAD_ERRIRC);
    }

  return ideal;
}

/*
 * texinfo: bad_scanf_intersectof_pretend_regchain
 * A parsing function for intersections of regular chains.
 * It is called by @code{ba0_scanf/%intersectof_pretend_regchain}.
 * It relies on @code{bad_scanf_pretend_regchain}.
 */

BAD_DLL void *
bad_scanf_intersectof_pretend_regchain (
    void *I)
{
  bad_intersectof_regchain ideal;
  ba0_tableof_string P;
  ba0_int_p i, differentiel;

  if (I == (void *) 0)
    ideal = bad_new_intersectof_regchain ();
  else
    ideal = (bad_intersectof_regchain) I;

  P = (ba0_tableof_string) ba0_new_table ();
  ba0_scanf
      ("intersectof_regchain (%t[%pretend_regchain], %t[%s])",
      &ideal->inter, P);

  bad_set_properties_attchain (&ideal->attrib, P);

  differentiel = 0;
  if (bad_defines_a_differential_ideal_attchain (&ideal->attrib))
    differentiel++;
  for (i = 0; i < ideal->inter.size; i++)
    if (bad_defines_a_differential_ideal_attchain
        (&ideal->inter.tab[i]->attrib))
      differentiel++;
  if (differentiel > 0 && differentiel < 1 + ideal->inter.size)
    BA0_RAISE_EXCEPTION (BAD_ERRIRC);

  if (bad_defines_a_prime_ideal_attchain (&ideal->attrib))
    {
      if (ideal->inter.size > 1)
        BA0_RAISE_EXCEPTION (BAD_ERRIRC);
      else if (ideal->inter.size == 1 &&
          !bad_defines_a_prime_ideal_attchain (&ideal->inter.tab[0]->attrib))
        BA0_RAISE_EXCEPTION (BAD_ERRIRC);
    }

  return ideal;
}

/*
 * texinfo: bad_printf_intersectof_regchain
 * A printing function for intersections of regular chains.
 * It is called by @code{ba0_printf/%intersectof_regchain}.
 */

BAD_DLL void
bad_printf_intersectof_regchain (
    void *I)
{
  bad_intersectof_regchain ideal = (bad_intersectof_regchain) I;
  ba0_tableof_string P;
  struct ba0_mark M;

  ba0_record (&M);
  P = (ba0_tableof_string) ba0_new_table ();
  bad_properties_attchain (P, &ideal->attrib);
  ba0_printf ("intersectof_regchain (%t[%regchain], %t[%s])", &ideal->inter, P);
  ba0_restore (&M);
}

/*
 * texinfo: bad_printf_intersectof_regchain_equations
 * A printing function for intersections of regular chains.
 * It is called by @code{ba0_printf/%intersectof_regchain_equations}.
 * It relies on @code{bad_printf_regchain_equations}.
 */

BAD_DLL void
bad_printf_intersectof_regchain_equations (
    void *I)
{
  bad_intersectof_regchain ideal = (bad_intersectof_regchain) I;

  ba0_printf ("%t[%regchain_equations]", &ideal->inter);
}

/*
 * Readonly static data
 */

static char _struct_intersect[] = "bad_intersectof_regchain";
static char _struct_intersect_tab[] = "bad_intersectof_regchain->inter.tab";

BAD_DLL ba0_int_p
bad_garbage1_intersectof_regchain (
    void *I,
    enum ba0_garbage_code code)
{
  bad_intersectof_regchain ideal = (bad_intersectof_regchain) I;
  ba0_int_p i, n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info
        (ideal, sizeof (struct bad_intersectof_regchain), _struct_intersect);

  if (ideal->inter.alloc > 0)
    {
      n += ba0_new_gc_info
          (ideal->inter.tab,
          ideal->inter.alloc * sizeof (bad_regchain), _struct_intersect_tab);
      for (i = 0; i < ideal->inter.alloc; i++)
        n += bad_garbage1_regchain (ideal->inter.tab[i], ba0_isolated);
    }

  return n;
}

BAD_DLL void *
bad_garbage2_intersectof_regchain (
    void *I,
    enum ba0_garbage_code code)
{
  bad_intersectof_regchain ideal;
  ba0_int_p i;

  if (code == ba0_isolated)
    ideal = (bad_intersectof_regchain) ba0_new_addr_gc_info
        (I, _struct_intersect);
  else
    ideal = (bad_intersectof_regchain) I;

  if (ideal->inter.alloc > 0)
    {
      ideal->inter.tab = (bad_regchain *) ba0_new_addr_gc_info
          (ideal->inter.tab, _struct_intersect_tab);
      for (i = 0; i < ideal->inter.alloc; i++)
        ideal->inter.tab[i] =
            bad_garbage2_regchain (ideal->inter.tab[i], ba0_isolated);
    }

  return ideal;
}

BAD_DLL void *
bad_copy_intersectof_regchain (
    void *I)
{
  bad_intersectof_regchain ideal;

  ideal = bad_new_intersectof_regchain ();
  bad_set_intersectof_regchain (ideal, (bad_intersectof_regchain) I);
  return ideal;
}
