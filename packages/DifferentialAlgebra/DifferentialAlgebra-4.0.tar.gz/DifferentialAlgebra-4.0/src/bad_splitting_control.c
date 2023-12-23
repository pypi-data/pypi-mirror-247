#include "bad_splitting_control.h"

/*
 * texinfo: bad_init_splitting_control
 * Initialize @var{C}. The field @code{first_leaf_only} is set
 * to @code{false}. The fields @code{dimlb} and @code{apply_dimlb_one_eq}
 * are set to @code{bad_algebraic_dimension_lower_bound} and @code{true}.
 */

BAD_DLL void
bad_init_splitting_control (
    bad_splitting_control S)
{
  memset (S, 0, sizeof (struct bad_splitting_control));
  S->first_leaf_only = false;
  S->dimlb = bad_algebraic_dimension_lower_bound;
  S->apply_dimlb_one_eq = true;
}

/*
 * texinfo: bad_new_splitting_control
 * Allocate a new @code{bad_splitting_control}, initialize it and return it.
 */

BAD_DLL bad_splitting_control
bad_new_splitting_control (
    void)
{
  bad_splitting_control S;

  S = (bad_splitting_control) ba0_alloc (sizeof (struct bad_splitting_control));
  bad_init_splitting_control (S);
  return S;
}

/*
 * texinfo: bad_set_splitting_control
 * Assign @var{T} to @var{S}.
 */

BAD_DLL void
bad_set_splitting_control (
    bad_splitting_control S,
    bad_splitting_control T)
{
  if (S != T)
    *S = *T;
}

/*
 * texinfo: bad_set_first_leaf_only_splitting_control
 * Assign @var{b} to the field @code{first_leaf_only} of @var{C}.
 */

BAD_DLL void
bad_set_first_leaf_only_splitting_control (
    bad_splitting_control S,
    bool b)
{
  S->first_leaf_only = b;
}

/*
 * texinfo: bad_set_dimension_lower_bound_splitting_control
 * Assign @var{lb} and @var{one_eq} to the fields
 * @code{dimlb} and @code{apply_dimlb_one_eq} of @var{C}.
 */

BAD_DLL void
bad_set_dimension_lower_bound_splitting_control (
    bad_splitting_control S,
    enum bad_typeof_dimension_lower_bound lb,
    bool one_eq)
{
  S->dimlb = lb;
  S->apply_dimlb_one_eq = one_eq;
}

/*
 * texinfo: bad_apply_dimension_lower_bound_splitting_control
 * Return @code{true} if differential elimination methods
 * must cut branches by application of the dimension lower bound.
 * The parameter @var{eqns} is the set of input equations.
 * The parameter @var{attchain} is the field @code{attrib} of
 * the regular chains to be computed.
 * The parameter @var{eqns} may be zero.
 */

BAD_DLL bool
bad_apply_dimension_lower_bound_splitting_control (
    bad_splitting_control S,
    bap_listof_polynom_mpz eqns,
    bad_attchain A)
{
  bap_listof_polynom_mpz L;
  struct bav_tableof_variable T;
  struct ba0_mark M;
  ba0_int_p nbders = 0, length;
  bool b = false;
/*
 * bad_no_dimension_lower_bound overrides apply_dimlb_one_eq
 */
  if (S->dimlb == bad_no_dimension_lower_bound)
    return false;
/*
 * The case of a single equation, provided that the table
 * of input equations (without the base field ones) is given.
 */
  length = ba0_length_list ((ba0_list) eqns);
  if (length == 1 && S->apply_dimlb_one_eq)
    return true;

  ba0_record (&M);
  ba0_init_table ((ba0_table) & T);
  for (L = eqns; L != (bap_listof_polynom_mpz) 0; L = L->next)
    bap_involved_derivations_polynom_mpz (&T, L->value);
  nbders = T.size;
  ba0_restore (&M);

  switch (S->dimlb)
    {
    case bad_no_dimension_lower_bound:
      b = false;
      break;
    case bad_algebraic_dimension_lower_bound:
/*
 * One may perform a non-differential decomposition over a
 * differential system.
 */
      if (!bad_defines_a_differential_ideal_attchain (A))
        b = true;
      else if (bav_global.R.ders.size == 0 || nbders == 0)
        b = true;
      else
        b = false;
      break;
    case bad_ode_dimension_lower_bound:
      if (bav_global.R.ders.size <= 1 || nbders <= 1)
        b = true;
      else
        b = false;
      break;
    case bad_pde_dimension_lower_bound:
      b = true;
      break;
    }
  return b;
}
