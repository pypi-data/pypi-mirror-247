#include "bad_reduction.h"
#include "bad_regularize.h"
#include "bad_global.h"

/*
 * texinfo: bad_set_settings_reduction
 * Set @code{bad_reduction_strategy}, @code{bad_redzero_strategy} and
 * @code{bad_number_of_redzero_tries} to @var{reduction_strategy}, 
 * @var{redzero_strategy} and @var{number_of_redzero_tries}. 
 * Zero values are replaced by default values.
 */

BAD_DLL void
bad_set_settings_reduction (
    enum bad_typeof_reduction_strategy reduction_strategy,
    enum bad_typeof_redzero_strategy redzero_strategy,
    ba0_int_p number_of_redzero_tries)
{
  bad_initialized_global.reduction.reduction_strategy =
      reduction_strategy ? reduction_strategy :
      bad_gcd_prem_and_factor_reduction_strategy;
  bad_initialized_global.reduction.redzero_strategy =
      redzero_strategy ? redzero_strategy :
      bad_deterministic_using_probabilistic_redzero_strategy;
  bad_initialized_global.reduction.number_of_redzero_tries =
      number_of_redzero_tries ? number_of_redzero_tries : 2;
}

/*
 * texinfo: bad_get_settings_reduction
 * Assign to @var{reduction_strategy}, @var{redzero_strategy} 
 * and @var{number_of_redzero_tries} the values of the
 * corresponding setting variables.
 */

BAD_DLL void
bad_get_settings_reduction (
    enum bad_typeof_reduction_strategy *reduction_strategy,
    enum bad_typeof_redzero_strategy *redzero_strategy,
    ba0_int_p *number_of_redzero_tries)
{
  if (reduction_strategy)
    *reduction_strategy = bad_initialized_global.reduction.reduction_strategy;
  if (redzero_strategy)
    *redzero_strategy = bad_initialized_global.reduction.redzero_strategy;
  if (number_of_redzero_tries)
    *number_of_redzero_tries =
        bad_initialized_global.reduction.number_of_redzero_tries;
}

/***************************************************************************
 SMALL REDUCTION RELATED FUNCTIONS.

 bad_is_a_reducible_polynom_by_regchain
 bad_is_a_partially_reduced_polynom_wrt_regchain
 bad_reduced_to_zero_derivatives_by_regchain

 ***************************************************************************/

static bool bad_is_a_reducible_term_by_regchain (
    bav_term,
    bad_regchain,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce,
    bav_rank,
    ba0_int_p *);

/*
 * texinfo: bad_is_a_reducible_polynom_by_regchain
 * Return @code{true} if @var{C} permits to reduce @var{A} w.r.t. the reduction 
 * defined by @var{type_red} and @var{type_der}. If so @var{rg} receives
 * the  highest reducible rank and @var{index} receives the index of some 
 * element of @var{C} able to reduce this rank. The two last parameters may
 * be the zero pointer.
 */

BAD_DLL bool
bad_is_a_reducible_polynom_by_regchain (
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bav_rank rg,
    ba0_int_p *index)
{
  return bad_is_a_reducible_term_by_regchain
      (&A->total_rank, C, type_red, type_der, rg, index);
}

/*
 * texinfo: bad_is_a_reducible_product_by_regchain
 * Variant of the @code{bad_is_a_reducible_polynom_by_regchain}, for products.
 */

BAD_DLL bool
bad_is_a_reducible_product_by_regchain (
    bap_product_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    ba0_int_p *index)
{
  struct bav_term T, U;
  ba0_int_p i;
  bool b;
  struct ba0_mark M;

  ba0_record (&M);

  bav_init_term (&T);
  bav_init_term (&U);

  for (i = 0; i < A->size; i++)
    {
      bav_pow_term (&U, &A->tab[i].factor.total_rank, A->tab[i].exponent);
      bav_mul_term (&T, &T, &U);
    }

  b = bad_is_a_reducible_term_by_regchain
      (&T, C, type_red, type_der, (struct bav_rank *) 0, index);
  ba0_restore (&M);
  return b;
}

/*
   Subfunction of bad_is_a_reducible_polynom_by_regchain.
   Subfunction of bad_some_product_of_factors_is_reducible
   See this function.
*/

static bool
bad_is_a_reducible_term_by_regchain (
    bav_term T,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bav_rank rg,
    ba0_int_p *indice)
{
  bav_variable u, v;
  bav_Idegree d, e;
  ba0_int_p i, j;
  bool found;

  bav_R_push_ordering (C->attrib.ordering);

  found = false;
  for (i = 0; i < T->size && !found; i++)
    {
      u = T->rg[i].var;
      d = T->rg[i].deg;
      if ((type_red == bad_algebraic_reduction &&
              bad_is_leader_of_regchain (u, C, &j)) ||
          (type_red != bad_algebraic_reduction &&
              bad_is_derivative_of_leader_of_regchain (u, C, &j)))
        {
          v = bap_leader_polynom_mpz (C->decision_system.tab[j]);
          e = bap_leading_degree_polynom_mpz (C->decision_system.tab[j]);
          if ((i > 0 || type_der == bad_all_derivatives_to_reduce)
              && ((v != u && type_red != bad_algebraic_reduction)
                  || (v == u && type_red != bad_partial_reduction && d >= e)))
            {
              if (rg != (bav_rank) 0)
                *rg = T->rg[i];
              if (indice != (ba0_int_p *) 0)
                *indice = j;
              found = true;
            }
        }
    }

  bav_R_pull_ordering ();

  return found;
}

/*
 * texinfo: bad_is_a_partially_reduced_polynom_wrt_regchain
 * Return @code{true} if @var{A} is partially reduced w.r.t. @var{C} i.e. if
 * @var{A} does note involve any proper derivative of any leader of @var{C}.
 */

BAD_DLL bool
bad_is_a_partially_reduced_polynom_wrt_regchain (
    bap_polynom_mpz A,
    bad_regchain C)
{
  return !bad_is_a_reducible_polynom_by_regchain
      (A, C, bad_partial_reduction, bad_all_derivatives_to_reduce,
      (bav_rank) 0, (ba0_int_p *) 0);
}

/*
 * texinfo: bad_is_a_partially_reduced_product_wrt_regchain
 * Variant of @code{bad_is_a_partially_reduced_polynom_wrt_regchain}, 
 * for products.
 */

BAD_DLL bool
bad_is_a_partially_reduced_product_wrt_regchain (
    bap_product_mpz A,
    bad_regchain C)
{
  ba0_int_p i;

  for (i = 0; i < A->size; i++)
    if (!bad_is_a_partially_reduced_polynom_wrt_regchain (&A->tab[i].factor, C))
      return false;
  return true;
}

/*
 * texinfo: bad_reduced_to_zero_derivatives_by_regchain
 * Assign to @var{nulles} derivatives which are reduced to zero by @var{C}
 * w.r.t. reduction @var{type_der}.
 * This set is not guaranteed to be complete in any sense.
 */

BAD_DLL void
bad_reduced_to_zero_derivatives_by_regchain (
    bav_tableof_variable nulles,
    bad_regchain C,
    enum bad_typeof_reduction type_red)
{
  bap_polynom_mpz P;
  ba0_int_p i, j, k;
  bav_variable v, x;

  ba0_reset_table ((ba0_table) nulles);

  k = C->decision_system.size;
  k *= BA0_MAX (1, bav_global.R.ders.size);
  ba0_realloc_table ((ba0_table) nulles, k);

  bav_R_push_ordering (C->attrib.ordering);

  switch (type_red)
    {
    case bad_algebraic_reduction:
      j = 0;
      for (i = 0; i < C->decision_system.size; i++)
        {
          P = C->decision_system.tab[i];
          v = bap_leader_polynom_mpz (P);
          if (bap_is_variable_polynom_mpz (P))
            nulles->tab[j++] = v;
        }
      nulles->size = j;
      break;
    case bad_partial_reduction:
    case bad_full_reduction:
      j = 0;
      for (i = 0; i < C->decision_system.size; i++)
        {
          P = C->decision_system.tab[i];
          v = bap_leader_polynom_mpz (P);
          if (bap_is_variable_polynom_mpz (P))
            nulles->tab[j++] = v;
          else if (bap_is_derivative_minus_independent_polynom_mpz (P))
            {
              for (k = 0; k < bav_global.R.ders.size; k++)
                {
                  x = bav_R_derivation_index_to_derivation (k);
                  if (bav_degree_term (&P->total_rank, x) == 0)
                    nulles->tab[j++] = bav_diff_variable (v, x->root);
                }
            }
          else if (bap_is_univariate_polynom_mpz (P))
            {
              for (k = 0; k < bav_global.R.ders.size; k++)
                {
                  x = bav_R_derivation_index_to_derivation (k);
                  nulles->tab[j++] = bav_diff_variable (v, x->root);
                }
            }
        }
      nulles->size = j;
      break;
    }

  bav_R_pull_ordering ();
/*
   Remove duplicates
*/
  for (i = 0; i < nulles->size; i++)
    nulles->tab[i]->hack = 0;
  for (i = 0; i < nulles->size; i++)
    {
      if (nulles->tab[i]->hack)
        {
          nulles->size -= 1;
          BA0_SWAP (bav_variable, nulles->tab[i], nulles->tab[nulles->size]);
        }
    }
}

/*
 * texinfo: bad_reduce_easy_polynom_by_regchain
 * Reduce @var{A} by the elements of @var{C} which are likely to decrease
 * the number of monomials of @var{A}. The result is stored in @var{R} 
 * and @var{H}.
 */

BAD_DLL void
bad_reduce_easy_polynom_by_regchain (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red)
{
  struct bap_polynom_mpz B;
  struct bav_rank rk;
  struct ba0_mark M;
  ba0_int_p i;
  bool once;

  if (type_red != bad_algebraic_reduction)
    BA0_RAISE_EXCEPTION (BA0_ERRNYP);

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_polynom_mpz (&B);
  once = false;
  for (i = C->decision_system.size - 1; i >= 0; i--)
    {
      if (bap_is_rank_minus_monom_polynom_mpz (C->decision_system.tab[i]))
        {
          rk = bap_rank_polynom_mpz (C->decision_system.tab[i]);
          if (bap_degree_polynom_mpz (once ? &B : A, rk.var) >= rk.deg)
            {
              bap_prem_polynom_mpz (&B, (bav_Idegree *) 0,
                  once ? &B : A, C->decision_system.tab[i], rk.var);
              once = true;
            }
        }
    }
  ba0_pull_stack ();
  if (once)
    {
/*
 * A bit complicated because it used to take the numeric primpart
 */
      if (bap_is_zero_polynom_mpz (&B))
        bap_set_polynom_zero_mpz (R);
      else
        bap_set_polynom_mpz (R, &B);
    }
  else if (R != A)
    bap_set_polynom_mpz (R, A);
  ba0_restore (&M);
}

/*
 * texinfo: bad_ensure_nonzero_initial_mod_regchain
 * Replace @var{A0} by its reductum while its initial is reduced to zero 
 * by @var{C}, using the type of reduction @var{type_red}. Result in @var{R}.
 */

BAD_DLL void
bad_ensure_nonzero_initial_mod_regchain (
    bap_polynom_mpz R,
    bap_polynom_mpz A0,
    bad_regchain C,
    enum bad_typeof_reduction type_red)
{
  struct bap_polynom_mpz init;
  bap_polynom_mpz reductum, A;
  bool simplified, go_on;

  A = bap_new_readonly_polynom_mpz ();
  reductum = bap_new_readonly_polynom_mpz ();
  bap_init_readonly_polynom_mpz (&init);

  bap_set_readonly_polynom_mpz (A, A0);
  go_on = !bap_is_numeric_polynom_mpz (A);
  simplified = false;
  while (go_on)
    {
      bap_initial_and_reductum_polynom_mpz (&init, reductum, A);
      if (bad_is_a_reduced_to_zero_polynom_by_regchain (&init, C, type_red))
        {
          simplified = true;
          BA0_SWAP (bap_polynom_mpz, reductum, A);
        }
      else
        go_on = false;
    }
  if (A != R || simplified)
    bap_set_polynom_mpz (R, A);
}

/****************************************************************************
 THE MAIN FUNCTIONS.

 REDUCTION + REDUCTION TO ZERO TEST.

 They call the same subroutines. 
 A global flag (bad_reduction_to_zero_test) permits to modify the behaviour 
 of the subroutines.
 ****************************************************************************/

static void bad_reduce_polynom_by_regchain2 (
    bap_product_mpz,
    bap_product_mpz,
    bap_polynom_mpz,
    bad_regchain,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce,
    bool);

/*
 * texinfo: bad_reduce_polynom_by_regchain
 * Reduce @var{A} by @var{C}. Result in @var{R} and @var{H}.
 * If @var{type_red} is @code{bad_algebraic_reduction} then the function
 * computes a relation
 * @math{H\,A = R} modulo the algebraic ideal @math{(C)}
 * where @var{H} is a power product of initials of elements of @var{C} 
 * and @var{R}
 * is algebraically reduced w.r.t. @var{C}. Otherwise, the function computes
 * a relation
 * @math{H\,A = R} modulo the differential ideal @math{[C]}.
 * If @var{type_red} is @code{bad_partial_reduction} then @var{H} is a power
 * product of separants of elements of @var{C} and @var{R} is partially reduced
 * w.r.t. @var{C}. If @var{type_red} is @code{bad_full_reduction} 
 * then @var{H} is
 * a power product of initials and separants of @var{C} and @var{R} is fully
 * reduced w.r.t. @var{C}.
 * The parameter @var{type_der} indicates if the leader of @var{A} is or is not
 * concerned by the reduction. 
 * Parameters @var{R} and @var{H} may be zero pointers.
 * The case where the ordering of @var{C} is different from the current ordering
 * is handled.
 */

BAD_DLL void
bad_reduce_polynom_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der)
{
  bap_product_mpz Rbar, Hbar;
  bap_polynom_mpz Abar;
  struct ba0_mark M;
  bool redzero_test = false;

  if (C->attrib.ordering == bav_R_Iordering ())
    bad_reduce_polynom_by_regchain2
        (R, H, A, C, type_red, type_der, redzero_test);
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      bav_R_push_ordering (C->attrib.ordering);

      if (R != (bap_product_mpz) 0)
        Rbar = bap_new_product_mpz ();
      else
        Rbar = (bap_product_mpz) 0;
      if (H != (bap_product_mpz) 0)
        Hbar = bap_new_product_mpz ();
      else
        Hbar = (bap_product_mpz) 0;

      Abar = bap_new_readonly_polynom_mpz ();
      bap_sort_polynom_mpz (Abar, A);

      bad_reduce_polynom_by_regchain2
          (Rbar, Hbar, Abar, C, type_red, type_der, redzero_test);

      bav_R_pull_ordering ();

      if (R != (bap_product_mpz) 0)
        {
          bap_sort_product_mpz (Rbar, Rbar);
          ba0_pull_stack ();
          bap_set_product_mpz (R, Rbar);
          ba0_push_another_stack ();
        }
      if (H != (bap_product_mpz) 0)
        {
          bap_sort_product_mpz (Hbar, Hbar);
          ba0_pull_stack ();
          bap_set_product_mpz (H, Hbar);
          ba0_push_another_stack ();
        }

      ba0_pull_stack ();
      ba0_restore (&M);
    }
#if defined (BA0_HEAVY_DEBUG)
  ba0_record (&M);
  if (R == (bap_product_mpz) 0 || H == (bap_product_mpz) 0)
    {
      Rbar = bap_new_product_mpz ();
      Hbar = bap_new_product_mpz ();
      bad_reduce_polynom_by_regchain (Rbar, Hbar, A, C, type_red, type_der);
      if (R != (bap_product_mpz) 0)
        Rbar = R;
      if (H != (bap_product_mpz) 0)
        Hbar = H;
    }
  else
    {
      Rbar = R;
      Hbar = H;
    }
  struct bap_polynom_mpz tmp1;
  bap_init_polynom_mpz (&tmp1);
  bap_expand_product_mpz (&tmp1, Hbar);
  bap_mul_polynom_mpz (&tmp1, &tmp1, A);
  struct bap_polynom_mpz tmp2;
  bap_init_polynom_mpz (&tmp2);
  bap_expand_product_mpz (&tmp2, Rbar);
  bap_sub_polynom_mpz (&tmp1, &tmp1, &tmp2);
  if (type_red == bad_partial_reduction)
    type_red = bad_full_reduction;
  if (!bad_is_a_reduced_to_zero_polynom_by_regchain (&tmp1, C, type_red))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  ba0_restore (&M);
#endif
}

static bool bad_is_probably_reduced_to_zero_by_regchain (
    bap_polynom_mpz,
    bad_regchain,
    enum bad_typeof_reduction);

/*
 * texinfo: bad_is_a_reduced_to_zero_polynom_by_regchain
 * Reduction to zero test.
 * Reduction type @code{bad_partial_reduction} makes no sense in this
 * context and is forbidden.
 * The case where the ordering of @var{C} is different from the current ordering
 * is handled.
 */

BAD_DLL bool
bad_is_a_reduced_to_zero_polynom_by_regchain (
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red)
{
  volatile bap_polynom_mpz Abar;
  struct ba0_mark M;
  bool redzero_test = true;
  volatile bool b = false;

  if (type_red == bad_partial_reduction)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_record (&M);
  if (C->attrib.ordering != bav_R_Iordering ())
    {
      bav_R_push_ordering (C->attrib.ordering);
      Abar = bap_new_readonly_polynom_mpz ();
      bap_sort_polynom_mpz (Abar, A);
    }
  else
    {
      bav_R_push_ordering (C->attrib.ordering);
      Abar = A;
    }

  switch (bad_initialized_global.reduction.redzero_strategy)
    {
    case bad_deterministic_using_probabilistic_redzero_strategy:
      if (!bad_is_probably_reduced_to_zero_by_regchain (Abar, C, type_red))
        {
          b = false;
          break;
        }
/*
   no break here: one continues in sequence.
*/
    case bad_deterministic_redzero_strategy:

      BA0_TRY
      {
        struct bap_product_mpz R;
        bap_init_product_mpz (&R);
        bad_reduce_polynom_by_regchain2
            (&R, (bap_product_mpz) 0,
            Abar, C, type_red, bad_all_derivatives_to_reduce, redzero_test);
      }
      BA0_CATCH
      {
        if (ba0_global.exception.raised == BAD_EXREDZ)
          {
            b = true;
            break;
          }
        else if (ba0_global.exception.raised == BAD_EXNRDZ)
          {
            b = false;
            break;
          }
        else
          BA0_RE_RAISE_EXCEPTION;
      }
      BA0_ENDTRY;

      BA0_RAISE_EXCEPTION (BA0_ERRALG);
      break;
    case bad_probabilistic_redzero_strategy:
      b = bad_is_probably_reduced_to_zero_by_regchain (Abar, C, type_red);
      break;
    }

  bav_R_pull_ordering ();
  ba0_restore (&M);

  return b;
}

/*
 * texinfo: bad_is_included_regchain
 * Test if @var{C} is included in @var{D}. 
 * Polynomials are supposed to have coefficients in @var{K}.
 */

BAD_DLL enum bad_typeof_inclusion_test_result
bad_is_included_regchain (
    bad_regchain A,
    bad_regchain B,
    bad_base_field K)
{
  struct bap_polynom_mpz initial, separant;
  struct ba0_mark M;
  ba0_int_p b, i;
  volatile enum bad_typeof_inclusion_test_result result =
      bad_inclusion_test_uncertain;

  ba0_record (&M);

  b = K->relations.decision_system.size;
  for (i = b; i < A->decision_system.size; i++)
    {
      if (!bad_is_a_reduced_to_zero_polynom_by_regchain
          (A->decision_system.tab[i], B, bad_full_reduction))
        {
          result = bad_inclusion_test_negative;
          goto fin;
        }
    }
/*
 * Exception handling.
 * If the regularity test produces an exception then the result
 * is "bad_inclusion_test_uncertain". 
 *
 * Splittings of B are thus not handled here.
 */
  BA0_TRY
  {
    bap_init_readonly_polynom_mpz (&initial);
    for (i = b; i < A->decision_system.size; i++)
      {
        bap_initial_polynom_mpz (&initial, A->decision_system.tab[i]);
        bad_check_regularity_polynom_mod_regchain (&initial, B, K, 0);
      }
    if (bad_defines_a_differential_ideal_regchain (A) ||
        bad_defines_a_differential_ideal_regchain (B))
      {
        if ((!bad_defines_a_differential_ideal_regchain (A)) ||
            (!bad_defines_a_differential_ideal_regchain (B)))
          BA0_RAISE_EXCEPTION (BA0_ERRNYP);
        bap_init_polynom_mpz (&separant);
        for (i = b; i < A->decision_system.size; i++)
          {
            if (bap_leading_degree_polynom_mpz (A->decision_system.tab[i]) > 1)
              {
                bap_separant_polynom_mpz (&separant, A->decision_system.tab[i]);
                bad_check_regularity_polynom_mod_regchain (&separant, B, K, 0);
              }
          }
      }
    result = bad_inclusion_test_positive;
  }
  BA0_CATCH
  {
    if (ba0_global.exception.raised != BAD_EXRNUL &&
        ba0_global.exception.raised != BAD_EXRDDZ)
      BA0_RE_RAISE_EXCEPTION;
    result = bad_inclusion_test_uncertain;
  }
  BA0_ENDTRY;
fin:
  ba0_restore (&M);
  return result;
}

/*
   Same parameters as bad_reduce_polynom_by_regchain.
   The global variable bad_reduction_to_zero_test indicates if this function
   must perform the reduction or only decide if the remainder is zero
   or not. In this last case, the function does not normally terminates
   but raises one of the exceptions BAD_EXREDZ (reduction to zero) and
   BAD_EXNRDZ (reduction to nonzero).
*/

static void bad_prem_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool);

static void bad_prem_and_change_of_ordering_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool);

static void bad_gcd_prem_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool);

static void bad_gcd_prem_and_factor_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool);

static void
bad_reduce_polynom_by_regchain2 (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  if (R == (bap_product_mpz) 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  switch (bad_initialized_global.reduction.reduction_strategy)
    {
    case bad_prem_reduction_strategy:
      bad_prem_reduction_by_regchain
          (R, H, A, C, type_red, type_der, redzero_test);
      break;
    case bad_prem_and_change_of_ordering_reduction_strategy:
      bad_prem_and_change_of_ordering_reduction_by_regchain
          (R, H, A, C, type_red, type_der, redzero_test);
      break;
    case bad_gcd_prem_reduction_strategy:
      bad_gcd_prem_reduction_by_regchain
          (R, H, A, C, type_red, type_der, redzero_test);
      break;
    case bad_gcd_prem_and_factor_reduction_strategy:
      bad_gcd_prem_and_factor_reduction_by_regchain
          (R, H, A, C, type_red, type_der, redzero_test);
      break;
    }
}

/****************************************************************************
 PREM REDUCTION ALGORITHM

 The most basic one.
 ****************************************************************************/

static void bad_prem_reduction_by_regchain2 (
    bap_polynom_mpz,
    bav_term,
    bav_term,
    bap_polynom_mpz,
    bad_regchain,
    bav_tableof_variable,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce,
    bool);

static void bad_unzip_power_product (
    bap_product_mpz H,
    bad_regchain C,
    bav_term I,
    bav_term S);

static void
bad_prem_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  bap_polynom_mpz P;
  struct bav_term Ippcm, Sppcm;
  struct bav_tableof_variable nulles;
  struct bav_rank rg;
  ba0_int_p i;
  struct ba0_mark M;

  if (R != (bap_product_mpz) 0)
    {
      bap_set_product_one_mpz (R);
      P = bap_new_polynom_mpz ();
    }
  else
    P = BAP_NOT_A_POLYNOM_mpz;

  if (H != (bap_product_mpz) 0)
    bap_set_product_one_mpz (H);

  if (!bad_is_a_reducible_polynom_by_regchain
      (A, C, type_red, type_der, &rg, &i))
    {
      if (redzero_test)
        BA0_RAISE_EXCEPTION
            (bap_is_zero_polynom_mpz (A) ? BAD_EXREDZ : BAD_EXNRDZ);
      if (R != (bap_product_mpz) 0)
        bap_set_product_polynom_mpz (R, A, 1);
      return;
    }

  ba0_record (&M);
  ba0_push_another_stack ();

  bav_init_term (&Ippcm);
  bav_realloc_term (&Ippcm, C->decision_system.size);
  bav_init_term (&Sppcm);
  bav_realloc_term (&Sppcm, C->decision_system.size);

  ba0_init_table ((ba0_table) & nulles);
  bad_reduced_to_zero_derivatives_by_regchain (&nulles, C, type_red);

  bad_prem_reduction_by_regchain2
      (P, &Ippcm, &Sppcm, A, C, &nulles, type_red, type_der, redzero_test);

  ba0_pull_stack ();

  if (R != (bap_product_mpz) 0)
    bap_set_product_polynom_mpz (R, P, 1);

  if (H != (bap_product_mpz) 0)
    bad_unzip_power_product (H, C, &Ippcm, &Sppcm);

  ba0_restore (&M);
  return;
}

/*
   The core of bad_prem_reduction_by_regchain.

   The terms $I$ and $S$ provide a cstack representation for the
	power products of initials and separants.

   Each element of $C$ is represented by its leader.
*/

static void bad_diff_element_of_regchain (
    bap_polynom_mpz,
    bap_polynom_mpz,
    bav_variable,
    bav_tableof_variable);

static void
bad_prem_reduction_by_regchain2 (
    bap_polynom_mpz R,
    bav_term I,
    bav_term S,
    bap_polynom_mpz A,
    bad_regchain C,
    bav_tableof_variable nulles,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  bap_polynom_mpz B, Rbar;
  struct bav_rank rg;
  bav_Idegree e;
  ba0_int_p i;
  struct ba0_mark M;

  bav_set_term_one (I);
  bav_set_term_one (S);
  bav_realloc_term (I, C->decision_system.size);
  bav_realloc_term (S, C->decision_system.size);

  if (!bad_is_a_reducible_polynom_by_regchain
      (A, C, type_red, type_der, &rg, &i))
    {
      if (redzero_test)
        BA0_RAISE_EXCEPTION
            (bap_is_zero_polynom_mpz (A) ? BAD_EXREDZ : BAD_EXNRDZ);
      if (R != BAP_NOT_A_POLYNOM_mpz && R != A)
        bap_set_polynom_mpz (R, A);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  if (type_red == bad_algebraic_reduction)
    B = C->decision_system.tab[i];
  else
    {
      B = bap_new_polynom_mpz ();
      bad_diff_element_of_regchain
          (B, C->decision_system.tab[i], rg.var, nulles);
    }

  Rbar = bap_new_polynom_mpz ();

  bap_prem_polynom_mpz (Rbar, &e, A, B, BAV_NOT_A_VARIABLE);
  if (e > 0)
    {
      struct bav_rank rk = bap_rank_polynom_mpz (C->decision_system.tab[i]);
      if (rg.var == rk.var || rk.deg == 1)
        bav_mul_term_variable (I, I, rk.var, e);
      else
        bav_mul_term_variable (S, S, rk.var, e);
    }

  while (bad_is_a_reducible_polynom_by_regchain
      (Rbar, C, type_red, type_der, &rg, &i))
    {
      if (type_red == bad_algebraic_reduction)
        B = C->decision_system.tab[i];
      else
        bad_diff_element_of_regchain
            (B, C->decision_system.tab[i], rg.var, nulles);
/*
ba0_printf ("struct bav_rank a reduire : %v^%d\n", rg.var, rg.deg);
ba0_printf ("|R| = %d\n|B| = %d\n", 
		bap_nbmon_polynom_mpz (Rbar), bap_nbmon_polynom_mpz (B));
*/
      bap_prem_polynom_mpz (Rbar, &e, Rbar, B, BAV_NOT_A_VARIABLE);
      if (e > 0)
        {
          struct bav_rank rk = bap_rank_polynom_mpz (C->decision_system.tab[i]);
          if (rg.var == rk.var || rk.deg == 1)
            bav_mul_term_variable (I, I, rk.var, e);
          else
            bav_mul_term_variable (S, S, rk.var, e);
        }
/*
ba0_printf ("prem effectue\n");
*/
    }

  if (redzero_test)
    BA0_RAISE_EXCEPTION
        (bap_is_zero_polynom_mpz (Rbar) ? BAD_EXREDZ : BAD_EXNRDZ);

  ba0_pull_stack ();
  bap_set_polynom_mpz (R, Rbar);
  ba0_restore (&M);
/*
ba0_printf ("fin de reduction\n");
*/
}

/*
 * u is a derivative theta v of some leader v of A
 * Sets R to theta A.
 */

static void
bad_diff_element_of_regchain (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bav_variable u,
    bav_tableof_variable nulles)
{
  bav_variable v;
  bav_variable s;
  bool first = true;

/*
 * if u lies in nulles then the equation to be return is u = 0.
 */
  if (bav_is_derivative2 (u, nulles))
    bap_set_polynom_variable_mpz (R, u, 1);
  else
    {
      v = bap_leader_polynom_mpz (A);
      while (u != v)
        {
          s = bav_derivation_between_derivatives (u, v);
          v = bav_diff_variable (v, s->root);
          bap_diff_polynom_mpz (R, first ? A : R, s->root, nulles);
          first = false;
        }
      if (first && R != A)
        bap_set_polynom_mpz (R, A);
    }
}

/*
   The terms $I$ and $S$ provide a cstack representation of the power
   product $H$ of initials and separants of elements of $C$.

   Elements of $C$ are represented by their leaders.
*/

static void
bad_unzip_power_product (
    bap_product_mpz H,
    bad_regchain C,
    bav_term I,
    bav_term S)
{
  struct bap_polynom_mpz init, sep;
  ba0_int_p i, k;
  struct ba0_mark M;

  bap_realloc_product_mpz (H, I->size + S->size);

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_readonly_polynom_mpz (&init);
  bap_init_polynom_mpz (&sep);

  for (i = 0; i < I->size; i++)
    {
      bad_is_leader_of_regchain (I->rg[i].var, C, &k);
      bap_initial_polynom_mpz (&init, C->decision_system.tab[k]);
      ba0_pull_stack ();
      bap_mul_product_polynom_mpz (H, H, &init, I->rg[i].deg);
      ba0_push_another_stack ();
    }

  for (i = 0; i < S->size; i++)
    {
      bad_is_leader_of_regchain (S->rg[i].var, C, &k);
      bap_separant_polynom_mpz (&sep, C->decision_system.tab[k]);
      ba0_pull_stack ();
      bap_mul_product_polynom_mpz (H, H, &sep, S->rg[i].deg);
      ba0_push_another_stack ();
    }

  ba0_pull_stack ();
  ba0_restore (&M);
}

/****************************************************************************
 PREM AND CHANGE OF RANKING REDUCTION ALGORITHM

 It is a variant of the basic algorithm.
 A change of ordering is performed so that the variables which are
	not concerned by the reduction process get higher than
	the other ones.
 The basic reduction algorithm is afterwards coefficientwise.
 ****************************************************************************/

static void bad_derivatives_not_concerned_by_the_reduction (
    bav_term,
    bap_polynom_mpz,
    bad_regchain,
    bav_tableof_variable,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce);

static void
bad_prem_and_change_of_ordering_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
/*
 * volatile qualifiers do not seem to be needed
 */
  struct bap_itercoeff_mpz iter;
  struct bap_creator_mpz crea;
  struct bap_itermon_mpz itermon;
  struct bap_polynom_mpz AA, init, sep, p, c;
  volatile bap_polynom_mpz P;
  struct bav_tableof_term termes;
  struct bap_tableof_polynom_mpz restes;
  struct bav_tableof_variable nulles;
  struct bav_term T, Ippcm, Sppcm, Inew, Snew;
  bav_variable v;
  struct bav_rank rg;
  bav_Iordering r;
  bav_Idegree d;
  ba0_int_p nbmon, i, j, k;
  struct ba0_mark M;
/*
   P = null pointer in the case of a reduction test to zero.
     = the polynomial where to store the remainder in the other case
*/
  if (R != (bap_product_mpz) 0)
    {
      bap_set_product_one_mpz (R);
      P = bap_new_polynom_mpz ();
    }
  else
    P = BAP_NOT_A_POLYNOM_mpz;

  if (H != (bap_product_mpz) 0)
    bap_set_product_one_mpz (H);
/*
   Quick test of irreducibility
*/
  if (!bad_is_a_reducible_polynom_by_regchain
      (A, C, type_red, type_der, &rg, &i))
    {
      if (redzero_test)
        BA0_RAISE_EXCEPTION
            (bap_is_zero_polynom_mpz (A) ? BAD_EXREDZ : BAD_EXNRDZ);
      if (R != (bap_product_mpz) 0)
        bap_set_product_polynom_mpz (R, A, 1);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_init_table ((ba0_table) & nulles);
  bad_reduced_to_zero_derivatives_by_regchain (&nulles, C, type_red);
/*
   T = the product of the derivatives not concerned by the reduction process.
*/
  bav_init_term (&T);
  bad_derivatives_not_concerned_by_the_reduction
      (&T, A, C, &nulles, type_red, type_der);
/*
   If T is empty then the classical algorithm is applied.
*/
  bav_init_term (&Ippcm);
  bav_realloc_term (&Ippcm, C->decision_system.size);
  bav_init_term (&Sppcm);
  bav_realloc_term (&Sppcm, C->decision_system.size);

  if (T.size == 0)
    {
      bad_prem_reduction_by_regchain2
          (P, &Ippcm, &Sppcm, A, C, &nulles, type_red, type_der, redzero_test);

      ba0_pull_stack ();

      if (R != (bap_product_mpz) 0)
        bap_set_product_polynom_mpz (R, P, 1);

      if (H != (bap_product_mpz) 0)
        bad_unzip_power_product (H, C, &Ippcm, &Sppcm);

      ba0_restore (&M);
      return;
    }

/*
   If T is not empty, the derivatives not concerned by the reduction are
	ranked higher than the other ones in a new ordering r.
   AA = the polynomial A reordered w.r.t. r.
   v = the lowest derivative not concerned by the reduction.

ba0_printf ("reduction de Ritt : |A| = %d, |X| = %d, |neutres| = %d\n",
			bap_nbmon_polynom_mpz (A), A->total_rank.size, T.size);
*/
  v = T.rg[T.size - 1].var;

  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);
  for (i = T.size - 1; i >= 0; i--)
    bav_R_set_maximal_variable (T.rg[i].var);

  bap_init_readonly_polynom_mpz (&AA);
  bap_sort_polynom_mpz (&AA, A);
/*
   The special case of a reduction to zero test is handled separately.

   From now on, all derivatives must be reduced !
*/
  if (redzero_test)
    {
      bap_init_readonly_polynom_mpz (&c);

      bap_begin_itercoeff_mpz (&iter, &AA, v);
      while (!bap_outof_itercoeff_mpz (&iter))
        {
          bap_coeff_itercoeff_mpz (&c, &iter);

          BA0_TRY
          {
            bad_prem_reduction_by_regchain2
                (BAP_NOT_A_POLYNOM_mpz, &Ippcm, &Sppcm, &c, C,
                &nulles, type_red, bad_all_derivatives_to_reduce, redzero_test);
/*
   An exception must be raised
*/
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          }
          BA0_CATCH
          {
            if (ba0_global.exception.raised != BAD_EXREDZ)
              BA0_RE_RAISE_EXCEPTION;
          }
          BA0_ENDTRY;

          bap_next_itercoeff_mpz (&iter);
        }
    }
/*
   The case of a real reduction.
   First we count the number of elementary reductions to perform.
*/
  i = 0;
  bap_begin_itercoeff_mpz (&iter, &AA, v);
  while (!bap_outof_itercoeff_mpz (&iter))
    {
      i++;
      bap_next_itercoeff_mpz (&iter);
    }
/*
   AA = sum of lambda_i T_i.
   restes [i] = the remainder of the reduction of lambda_i
   termes [i] = T_i.
*/
  ba0_init_table ((ba0_table) & restes);
  ba0_init_table ((ba0_table) & termes);
  ba0_realloc2_table
      ((ba0_table) & restes, i, (ba0_new_function *) & bap_new_polynom_mpz);
  ba0_realloc2_table ((ba0_table) & termes, i,
      (ba0_new_function *) & bav_new_term);
  restes.size = i;
  termes.size = i;
/*
   Ippcm and Sppcm receive the lcm of the power products of initials
	and separants (cumulating variables).
   They were initialized above.
   Inew and Snew receive the contribution of the last reduction.
*/
  bav_init_term (&Inew);
  bav_init_term (&Snew);

  bap_init_polynom_mpz (&p);
  bap_init_readonly_polynom_mpz (&c);
  bap_init_readonly_polynom_mpz (&init);
  bap_init_polynom_mpz (&sep);
/*
   Main loop
*/
  bap_begin_itercoeff_mpz (&iter, &AA, v);
  for (i = 0; i < restes.size; i++)
    {
      bap_coeff_itercoeff_mpz (&c, &iter);
/*
   Computation of restes [i] and termes [i].
   All derivatives must be reduced.
*/
      bad_prem_reduction_by_regchain2
          (restes.tab[i], &Inew, &Snew, &c, C,
          &nulles, type_red, bad_all_derivatives_to_reduce, redzero_test);
      bap_term_itercoeff_mpz (termes.tab[i], &iter);
/*
   Painful loops to update Ippcm, Sppcm and formerly computed remainders.
*/
      for (j = 0; j < Ippcm.size; j++)
        {
          d = Ippcm.rg[j].deg - bav_degree_term (&Inew, Ippcm.rg[j].var);
          if (d > 0)
            {
              bad_is_leader_of_regchain (Ippcm.rg[j].var, C, &k);
              bap_initial_polynom_mpz (&init, C->decision_system.tab[k]);
              bap_pow_polynom_mpz (&p, &init, d);
              bap_mul_polynom_mpz (restes.tab[i], restes.tab[i], &p);
            }
        }
      for (j = 0; j < Sppcm.size; j++)
        {
          d = Sppcm.rg[j].deg - bav_degree_term (&Snew, Sppcm.rg[j].var);
          if (d > 0)
            {
              bad_is_leader_of_regchain (Sppcm.rg[j].var, C, &k);
              bap_separant_polynom_mpz (&sep, C->decision_system.tab[k]);
              bap_pow_polynom_mpz (&p, &sep, d);
              bap_mul_polynom_mpz (restes.tab[i], restes.tab[i], &p);
            }
        }
      for (j = 0; j < Inew.size; j++)
        {
          d = Inew.rg[j].deg - bav_degree_term (&Ippcm, Inew.rg[j].var);
          if (d > 0)
            {
              bad_is_leader_of_regchain (Inew.rg[j].var, C, &k);
              bap_initial_polynom_mpz (&init, C->decision_system.tab[k]);
              bap_pow_polynom_mpz (&p, &init, d);
              for (k = 0; k < i; k++)
                bap_mul_polynom_mpz (restes.tab[k], restes.tab[k], &p);
            }
        }
      for (j = 0; j < Snew.size; j++)
        {
          d = Snew.rg[j].deg - bav_degree_term (&Sppcm, Snew.rg[j].var);
          if (d > 0)
            {
              bad_is_leader_of_regchain (Snew.rg[j].var, C, &k);
              bap_separant_polynom_mpz (&sep, C->decision_system.tab[k]);
              bap_pow_polynom_mpz (&p, &sep, d);
              for (k = 0; k < i; k++)
                bap_mul_polynom_mpz (restes.tab[k], restes.tab[k], &p);
            }
        }
      bav_lcm_term (&Ippcm, &Ippcm, &Inew);
      bav_lcm_term (&Sppcm, &Sppcm, &Snew);

      bap_next_itercoeff_mpz (&iter);
    }
/*
   Exit the main loop.

   nbmon = the number of monomials of the collected remainder.
   T     = total rank of the collected remainder.
*/
  nbmon = 0;
  bav_set_term_one (&T);
  for (i = 0; i < restes.size; i++)
    {
      if (!bap_is_zero_polynom_mpz (restes.tab[i]))
        {
          bav_lcm_term (&T, &T, termes.tab[i]);
          bav_lcm_term (&T, &T, &restes.tab[i]->total_rank);
          nbmon += bap_nbmon_polynom_mpz (restes.tab[i]);
        }
    }
/*
   Creation of the collected remainder P.
*/
  bap_begin_creator_mpz (&crea, P, &T, bap_exact_total_rank, nbmon);

  for (i = 0; i < restes.size; i++)
    {
      bap_begin_itermon_mpz (&itermon, restes.tab[i]);
      while (!bap_outof_itermon_mpz (&itermon))
        {
          ba0_mpz_t *lc;

          lc = bap_coeff_itermon_mpz (&itermon);
          bap_term_itermon_mpz (&T, &itermon);
          bav_mul_term (&T, &T, termes.tab[i]);

          bap_write_creator_mpz (&crea, &T, *lc);

          bap_next_itermon_mpz (&itermon);
        }
    }

  bap_close_creator_mpz (&crea);
/*
   The monomials of the collected remainder P must be physically reordered
	w.r.t. the current ordering.
*/
  bav_R_pull_ordering ();
  bap_physort_polynom_mpz (P);

  bav_R_free_ordering (r);

  ba0_pull_stack ();

  if (R != (bap_product_mpz) 0)
    bap_set_product_polynom_mpz (R, P, 1);

  if (H != (bap_product_mpz) 0)
    bad_unzip_power_product (H, C, &Ippcm, &Sppcm);

  ba0_restore (&M);
}

/*
   Stores in $T$ the derivatives not concerned by the reduction of $A$ by $C$.
   They are the ones which are in $A$ but not in $C$ (and which are not
	going to appear by differentiating elements of $C$ in the case
	of differential reductions).

   It would be nicer to use a table of variables instead of a term
	but there are much more functions available on terms than
	on tables of variables.
*/

static void
bad_derivatives_not_concerned_by_the_reduction (
    bav_term T,
    bap_polynom_mpz A,
    bad_regchain C,
    bav_tableof_variable nulles,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der)
{
  struct bav_term B, D, E, F;
  bav_variable u, v, s;
  ba0_int_p i, j;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&B);
  bav_init_term (&D);
  bav_init_term (&E);
  bav_init_term (&F);

  bav_realloc_term (&B, bav_global.R.vars.size);
  bav_realloc_term (&F, bav_global.R.vars.size);

  bav_set_term (&D, &A->total_rank);

  for (i = 0; i < C->decision_system.size; i++)
    bav_lcm_term (&F, &F, &C->decision_system.tab[i]->total_rank);

  if (type_red == bad_algebraic_reduction)
    {
      for (i = 0; i < D.size; i++)
        {
          u = D.rg[i].var;
          if (bav_degree_term (&F, u) == 0)
            bav_mul_term_variable (&B, &B, u, 1);
        }
    }
  else
    {
      bav_realloc_term (&E, bav_global.R.vars.size);

      for (i = 0; i < D.size; i++)
        {
          u = D.rg[i].var;
          if (bad_is_derivative_of_leader_of_regchain (u, C, &j))
            {
              bav_set_term (&E, &C->decision_system.tab[j]->total_rank);
              bav_lcm_term (&D, &D, &E);
              v = bap_leader_polynom_mpz (C->decision_system.tab[j]);
              while (u != v)
                {
                  s = bav_derivation_between_derivatives (u, v);
                  v = bav_diff_variable (v, s->root);
                  bav_diff_term (&E, &E, s->root, nulles);
                  bav_lcm_term (&D, &D, &E);
                  bav_lcm_term (&F, &F, &E);
                }
            }
          else if (bav_degree_term (&F, u) == 0)
            bav_mul_term_variable (&B, &B, u, 1);
        }
    }

  if (type_der == bad_all_but_leader_to_reduce)
    bav_mul_term_variable (&B, &B, bap_leader_polynom_mpz (A), 1);

  for (i = 0; i < B.size; i++)
    B.rg[i].deg = 1;

  ba0_pull_stack ();
  bav_set_term (T, &B);
  ba0_restore (&M);
}

/****************************************************************************
 GCD_PREM STRATEGY

 Remainders are computed by gcd_prem 
 ****************************************************************************/

static void
bad_gcd_prem_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  R = (bap_product_mpz) 0;
  H = (bap_product_mpz) 0;
  A = (bap_polynom_mpz) 0;
  C = (bad_regchain) 0;
  type_red = bad_algebraic_reduction;
  type_der = bad_all_derivatives_to_reduce;
  redzero_test = true;

  BA0_RAISE_EXCEPTION (BA0_ERRNYP);
}

/****************************************************************************
 GCD_PREM AND FACTOR REDUCTION STRATEGY

 Remainders are computed by gcd_prem and factored decision_systematically.
 ****************************************************************************/

static void bad_combine_factors_up_to_reducibility (
    bap_polynom_mpz,
    bap_product_mpz,
    bap_polynom_mpz);

static void bad_remainder_irreducible_factorwise (
    bap_product_mpz,
    bap_product_mpz,
    bap_polynom_mpz,
    bad_regchain,
    bap_listof_polynom_mpz,
    bav_tableof_variable,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce,
    bool);

static void
bad_gcd_prem_and_factor_reduction_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  bap_listof_polynom_mpz divisors;
  struct bap_polynom_mpz init, sep;
  struct bav_tableof_variable nulles;
  bap_product_mpz Rbar, Hbar, Hk;
  bap_polynom_mpz Abar, Ck;
  bav_variable vk;
  ba0_int_p k;
  struct ba0_mark M;

  if (R == (bap_product_mpz) 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
/*
   There is no need to initialize R and H for they are going to be 
   initialized by bad_remainder_irreducible_factorwise.
*/
  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_init_table ((ba0_table) & nulles);
  bad_reduced_to_zero_derivatives_by_regchain (&nulles, C, type_red);
/*
 * Quite often, initials and separants of C show up as factors
 * after a few reductions.
 */
#define WITH_DIVISORS 1
#undef WITH_DIVISORS
  divisors = (bap_listof_polynom_mpz) 0;
  bap_init_readonly_polynom_mpz (&init);
  bap_init_polynom_mpz (&sep);
#if defined (WITH_DIVISORS)
  for (k = 0; k < C->decision_system.size; k++)
    {
      bap_initial_polynom_mpz (&init, C->decision_system.tab[k]);
      if (!bap_is_numeric_polynom_mpz (&init))
        {
          divisors = (bap_listof_polynom_mpz) ba0_cons_list
              (bap_new_polynom_mpz (), (ba0_list) divisors);
          bap_numeric_primpart_polynom_mpz (divisors->value, &init);
        }
    }
  for (k = 0; k < C->decision_system.size; k++)
    {
      if (bap_leading_degree_polynom_mpz (C->decision_system.tab[k]) > 1)
        {
          bap_separant_polynom_mpz (&sep, C->decision_system.tab[k]);
          if (!bap_is_numeric_polynom_mpz (&sep))
            {
              divisors = (bap_listof_polynom_mpz) ba0_cons_list
                  (bap_new_polynom_mpz (), (ba0_list) divisors);
              bap_numeric_primpart_polynom_mpz (divisors->value, &sep);
            }
        }
    }
  divisors = (bap_listof_polynom_mpz) ba0_reverse_list ((ba0_list) divisors);
#endif
  ba0_pull_stack ();
/*
   Computes a remainder (a product) irreducible factorwise
*/
  bad_remainder_irreducible_factorwise
      (R, H, A, C, divisors, &nulles, type_red, type_der, redzero_test);

  if (type_red == bad_partial_reduction ||
      !bad_is_a_reducible_product_by_regchain (R, C, type_red, type_der, &k))
    goto fin;
/*
   We have to handle the problem of irreducible factors the product of which
	is not irreducible.
*/
  ba0_push_another_stack ();

  Abar = bap_new_polynom_mpz ();
  Rbar = bap_new_product_mpz ();
  if (H != (bap_product_mpz) 0)
    {
      Hbar = bap_new_product_mpz ();
      Hk = bap_new_product_mpz ();
    }
  else
    {
      Hbar = (bap_product_mpz) 0;
      Hk = (bap_product_mpz) 0;
    }

  ba0_pull_stack ();
/*
 * Loop invariant H*A = R modulo the ideal
 */
  do
    {
      ba0_push_another_stack ();

      Ck = C->decision_system.tab[k];
      vk = bap_leader_polynom_mpz (Ck);
      bad_combine_factors_up_to_reducibility (Abar, R, Ck);
      baz_gcd_prem_polynom_mpz (Abar, Hk, Abar, Ck, vk);
      bad_remainder_irreducible_factorwise
          (Rbar, Hbar, Abar, C, divisors, &nulles,
          bad_algebraic_reduction, type_der, redzero_test);

      ba0_pull_stack ();

      bap_mul_product_mpz (R, R, Rbar);
      if (H != (bap_product_mpz) 0)
        {
          bap_mul_product_mpz (H, H, Hk);
          bap_mul_product_mpz (H, H, Hbar);
        }
    }
  while (bad_is_a_reducible_product_by_regchain (R, C, type_red, type_der, &k));
fin:
  if (redzero_test)
    BA0_RAISE_EXCEPTION (bap_is_zero_product_mpz (R) ? BAD_EXREDZ : BAD_EXNRDZ);
  ba0_restore (&M);
}

/*
   Subfunction of bad_gcd_prem_and_factor_reduction_by_regchain
   Computes R and H.
   It is only guaranteed that each factor of the remainder is irreducible.
   However, some products of these irreducible factors may be reducible.

   Parameters R and H may be zero.
   If a factor is reduced to zero and bad_reduction_to_zero_test,
	the exception BAD_EXREDZ is raised. The exception BAD_EXNRDZ
	is not raised by this function.
*/

static void
bad_remainder_irreducible_factorwise (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_polynom_mpz A,
    bad_regchain C,
    bap_listof_polynom_mpz divisors,
    bav_tableof_variable nulles,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  struct bap_product_mpz P;
  bap_product_mpz H_F, Rbar, Hbar;
  struct bap_polynom_mpz B, F;
  enum bad_typeof_derivative_to_reduce new_type_der;
  struct bav_rank rg;
  bav_variable v = BAV_NOT_A_VARIABLE;
  ba0_int_p i, k;
  struct ba0_mark M;
/*
   P = a factorization of A
   for each factor p^d of P do
      if irreducible then
	 R = R * p^d
      else
	 (F, H_F) = gcd_prem (p, the convenient element of C)
	 (Rbar, Hbar) = recursive call (F , ...)
	 R = R * Rbar^d
	 H = H * (Hbar * H_F)^d
      fi
   done
*/
/*
    ba0_printf ("\n%Az\n\n", A);
*/
  if (H != (bap_product_mpz) 0)
    bap_set_product_one_mpz (H);

  if (bap_is_zero_polynom_mpz (A))
    {
      if (redzero_test)
        BA0_RAISE_EXCEPTION (BAD_EXREDZ);
      if (R != (bap_product_mpz) 0)
        bap_set_product_zero_mpz (R);
      return;
    }

  if (R != (bap_product_mpz) 0)
    bap_set_product_one_mpz (R);

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_product_mpz (&P);
  baz_factor_easy_polynom_mpz (&P, A, divisors);

  if (R != (bap_product_mpz) 0)
    Rbar = bap_new_product_mpz ();
  else
    Rbar = (bap_product_mpz) 0;

  if (H != (bap_product_mpz) 0)
    {
      Hbar = bap_new_product_mpz ();
      H_F = bap_new_product_mpz ();
    }
  else
    {
      Hbar = (bap_product_mpz) 0;
      H_F = (bap_product_mpz) 0;
    }

  bap_init_polynom_mpz (&B);
  bap_init_polynom_mpz (&F);

  if (!bap_is_independent_polynom_mpz (A, (bav_tableof_parameter) 0))
    v = bap_leader_polynom_mpz (A);

  if (!redzero_test && R != (bap_product_mpz) 0)
    {
      ba0_pull_stack ();
      bap_mul_product_numeric_mpz (R, R, P.num_factor);
      ba0_push_another_stack ();
    }

  for (i = 0; i < P.size; i++)
    {
      if (type_der == bad_all_but_leader_to_reduce &&
          !bap_depend_polynom_mpz (&P.tab[i].factor, v))
        new_type_der = bad_all_derivatives_to_reduce;
      else
        new_type_der = type_der;
      if (!bad_is_a_reducible_polynom_by_regchain
          (&P.tab[i].factor, C, type_red, new_type_der, &rg, &k))
        {
          if (R != (bap_product_mpz) 0)
            {
              ba0_pull_stack ();
              bap_mul_product_polynom_mpz
                  (R, R, &P.tab[i].factor, P.tab[i].exponent);
              ba0_push_another_stack ();
            }
        }
      else
        {
          bad_diff_element_of_regchain
              (&B, C->decision_system.tab[k], rg.var, nulles);
          if (H_F != (bap_product_mpz) 0)
            bap_set_product_one_mpz (H_F);
          baz_gcd_prem_polynom_mpz
              (&F, H_F, &P.tab[i].factor, &B, BAV_NOT_A_VARIABLE);

          if (redzero_test && bap_is_zero_polynom_mpz (&F))
            BA0_RAISE_EXCEPTION (BAD_EXREDZ);

          if (type_der == bad_all_but_leader_to_reduce &&
              !bap_depend_polynom_mpz (&F, v))
            new_type_der = bad_all_derivatives_to_reduce;
          else
            new_type_der = type_der;

          bad_remainder_irreducible_factorwise
              (Rbar, Hbar, &F, C, divisors, nulles,
              type_red, new_type_der, redzero_test);

          if (Rbar != (bap_product_mpz) 0)
            bap_pow_product_mpz (Rbar, Rbar, P.tab[i].exponent);

          if (H != (bap_product_mpz) 0)
            {
              bap_mul_product_mpz (H_F, H_F, Hbar);
              bap_pow_product_mpz (H_F, H_F, P.tab[i].exponent);
            }

          ba0_pull_stack ();
          if (R != (bap_product_mpz) 0)
            bap_mul_product_mpz (R, R, Rbar);
          if (H != (bap_product_mpz) 0)
            bap_mul_product_mpz (H, H, H_F);
          ba0_push_another_stack ();
        }
    }
  ba0_pull_stack ();
/*
    ba0_printf ("belongs_to ((%Pz)*(%Az)-(%Pz), ideal);\n", H, A, R);
*/
  ba0_restore (&M);
}

/*
   Stores in A a product of factors of R reducible by B.
   Such a product of factors exists.
   The product R is factored out by A.

   The elements of R are assumed to be irreducible factorwise.
   Thus the reduction type necessarily is a purely algebraic reduction.
*/

static void
bad_combine_factors_up_to_reducibility (
    bap_polynom_mpz A,
    bap_product_mpz R,
    bap_polynom_mpz B)
{
  bav_variable x;
  bav_Idegree d;
  ba0_int_p i;

  bap_set_polynom_one_mpz (A);
  x = bap_leader_polynom_mpz (B);
  d = bap_leading_degree_polynom_mpz (B);

  i = 0;
  while (bap_degree_polynom_mpz (A, x) < d)
    {
      while (bav_degree_term (&R->tab[i].factor.total_rank, x) == 0)
        i++;
      while (bap_degree_polynom_mpz (A, x) < d && R->tab[i].exponent > 0)
        {
          bap_mul_polynom_mpz (A, A, &R->tab[i].factor);
          R->tab[i].exponent--;
        }
      i++;
    }
/*
   Normalization of R.
   Factors with exponent 0 are moved at the end of the product.
*/
  i = 0;
  while (i < R->size)
    {
      if (R->tab[i].exponent == 0)
        {
          if (i != R->size - 1)
            BA0_SWAP (struct bap_power_mpz,
                R->tab[i],
                R->tab[R->size - 1]);
          R->size--;
        }
      else
        i++;
    }
}

/****************************************************************************
 PROBABILISTIC REDUCTION TO ZERO TEST.

 It takes the polynomials modulo (p, x_k - alpha_k) where p is a prime
 number and the x_k are the derivatives under the stairs of the 
 regular chain C.

 Then it applies the basic algorithm.
 ****************************************************************************/

/*
   type_red == bad_full_reduction || bad_algebraic_reduction
*/

static bool bad_is_probably_reduced_to_zero_by_regchain2 (
    bap_polynom_mpz,
    bad_regchain,
    ba0_mint_hp,
    bav_tableof_variable,
    enum bad_typeof_reduction);

static bool
bad_is_probably_reduced_to_zero_by_regchain (
    bap_polynom_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red)
{
  struct bav_tableof_variable nulles;
  bool b;
  ba0_int_p i;
  ba0_mint_hp prime;
  struct ba0_mark M;
/*
   The only known example where the probabilistic test algorithm
   gave a wrong answer was due to an irreducible nonzero polynomial
   which was zero modulo the ideal.
*/
  if (!bad_is_a_reducible_polynom_by_regchain
      (A, C, type_red, bad_all_derivatives_to_reduce,
          (struct bav_rank *) 0, (ba0_int_p *) 0))
    return bap_is_zero_polynom_mpz (A);

  ba0_record (&M);

  ba0_init_table ((ba0_table) & nulles);
  bad_reduced_to_zero_derivatives_by_regchain (&nulles, C, type_red);

  prime = ba0_largest_small_prime ();
  b = true;
  for (i = 0;
      b && i < bad_initialized_global.reduction.number_of_redzero_tries; i++)
    {
      b = bad_is_probably_reduced_to_zero_by_regchain2
          (A, C, prime, &nulles, type_red);
      prime = ba0_previous_small_prime (prime);
    }

  ba0_restore (&M);
  return b;
}

static void bad_random_eval_variables_under_the_stairs (
    bap_polynom_mint_hp,
    bap_polynom_mpz,
    bad_regchain,
    ba0_mint_hp);

static bool
bad_is_probably_reduced_to_zero_by_regchain2 (
    bap_polynom_mpz A,
    bad_regchain C,
    ba0_mint_hp prime,
    bav_tableof_variable nulles,
    enum bad_typeof_reduction type_red)
{
  struct bap_polynom_mpz B;
  struct bap_polynom_mint_hp Abar, Bbar;
  struct bav_rank rg;
  bool b;
  ba0_int_p i;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_polynom_mint_hp (&Abar);
  bad_random_eval_variables_under_the_stairs (&Abar, A, C, prime);
  bap_init_polynom_mpz (&B);
  bap_init_polynom_mint_hp (&Bbar);
/*
   One calls the subfunction bad_is_a_reducible_term_by_regchain
	instead of the common function bad_is_a_reducible_polynom_by_regchain
	for this last one is defined for polynomials with coefficients
	ba0_mpz_t and not for ba0_mint_hp.
*/
  while (bad_is_a_reducible_term_by_regchain
      (&Abar.total_rank, C, type_red, bad_all_derivatives_to_reduce, &rg, &i))
    {
      bad_diff_element_of_regchain
          (&B, C->decision_system.tab[i], rg.var, nulles);
      bad_random_eval_variables_under_the_stairs (&Bbar, &B, C, prime);
      bap_prem_polynom_mint_hp (&Abar, (bav_Idegree *) 0, &Abar,
          &Bbar, BAV_NOT_A_VARIABLE);
    }
  b = bap_is_zero_polynom_mint_hp (&Abar);
  ba0_pull_stack ();
  ba0_restore (&M);
  return b;
}

/*
   Subfunction of bad_random_eval_variables_under_the_stairs

   The array stairs contains the set of leaders of some regular chain C.
   Returns true if the variable v is a variable under the stairs of C
	i.e. if v is a derivative under the stairs or any variable which 
	is not a derivative
*/

#define bad_stairs	bad_global.reduction.stairs

static bool
bad_is_a_variable_under_the_stairs (
    void *v)
{
  bav_variable x = (bav_variable) v;
  ba0_int_p i;

  if (x->root->type != bav_dependent_symbol)
    return true;

  for (i = 0; i < bad_stairs->size; i++)
    if (bav_is_derivative (x, bad_stairs->tab[i]))
      return false;

  return true;
}

/*
   Subfunction of bad_random_eval_variables_under_the_stairs

   The array stairs contains the set of leaders of some regular chain C.
   Returns true if the variable v is a non algebraic variable of C
        i.e. if v is different from any leader of C.
*/

static bool
bad_is_a_non_algebraic_variable (
    void *v)
{
  bav_variable x = (bav_variable) v;
  ba0_int_p i;

  if (x->root->type != bav_dependent_symbol)
    return true;

  for (i = 0; i < bad_stairs->size; i++)
    if (x == bad_stairs->tab[i])
      return false;

  return true;
}

/*
   Sets R to A mod I where I = (prime, x_k - alpha_k)
   The derivatives x_k are the derivatives under the stairs of C.
   The values alpha_k are computed heuristically.
*/

static void
bad_random_eval_variables_under_the_stairs (
    bap_polynom_mint_hp R,
    bap_polynom_mpz A,
    bad_regchain C,
    ba0_mint_hp prime)
{
  ba0_int_p i;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  bad_stairs = (bav_tableof_variable) ba0_new_table ();
  ba0_realloc_table ((ba0_table) bad_stairs, C->decision_system.size);

  for (i = 0; i < C->decision_system.size; i++)
    bad_stairs->tab[i] = bap_leader_polynom_mpz (C->decision_system.tab[i]);

  bad_stairs->size = C->decision_system.size;

  ba0_pull_stack ();

  ba0_mint_hp_module_set (prime, true);

  if (bad_defines_a_differential_ideal_attchain (&C->attrib))
    bap_random_eval_polynom_mpz_to_mint_hp
        (R, A, &bad_is_a_variable_under_the_stairs);
  else
    bap_random_eval_polynom_mpz_to_mint_hp
        (R, A, &bad_is_a_non_algebraic_variable);

  ba0_restore (&M);
}

/*************************************************************************
 OPERATIONS ON PRODUCTS
 *************************************************************************/

static void bad_reduce_product_by_regchain2 (
    bap_product_mpz,
    bap_product_mpz,
    bap_product_mpz,
    bad_regchain,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce,
    bool);

/*
 * texinfo: bad_reduce_product_by_regchain
 * Variant of @code{bad_reduce_polynom_by_regchain}, for products.
 */

BAD_DLL void
bad_reduce_product_by_regchain (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_product_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der)
{
  bap_product_mpz Rbar;
  bap_product_mpz Hbar;
  bap_product_mpz Abar;
  struct ba0_mark M;
  bool redzero_test = false;

  Rbar = R;
  Hbar = H;
  Abar = A;

  if (C->attrib.ordering == bav_R_Iordering ())
    bad_reduce_product_by_regchain2
        (Rbar, Hbar, Abar, C, type_red, type_der, redzero_test);
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      bav_R_push_ordering (C->attrib.ordering);

      if (R != (bap_product_mpz) 0)
        Rbar = bap_new_product_mpz ();
      if (H != (bap_product_mpz) 0)
        Hbar = bap_new_product_mpz ();

      Abar = bap_new_product_mpz ();
      bap_sort_product_mpz (Abar, A);

      bad_reduce_product_by_regchain2
          (Rbar, Hbar, Abar, C, type_red, type_der, redzero_test);

      bav_R_pull_ordering ();

      if (R != (bap_product_mpz) 0)
        {
          bap_sort_product_mpz (Rbar, Rbar);
          ba0_pull_stack ();
          bap_set_product_mpz (R, Rbar);
          ba0_push_another_stack ();
        }
      if (H != (bap_product_mpz) 0)
        {
          bap_sort_product_mpz (Hbar, Hbar);
          ba0_pull_stack ();
          bap_set_product_mpz (H, Hbar);
          ba0_push_another_stack ();
        }

      ba0_pull_stack ();
      ba0_restore (&M);
    }
}

static void bad_reduce_product_by_regchain2 (
    bap_product_mpz,
    bap_product_mpz,
    bap_product_mpz,
    bad_regchain,
    enum bad_typeof_reduction,
    enum bad_typeof_derivative_to_reduce,
    bool redzero_test);

/*
 * texinfo: bad_is_a_reduced_to_zero_product_by_regchain
 * Variant of @code{bad_is_a_reduced_to_zero_polynom_by_regchain}, 
 * for products.
 */

BAD_DLL bool
bad_is_a_reduced_to_zero_product_by_regchain (
    bap_product_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red)
{
  volatile bap_product_mpz Abar;
  volatile bool b = false;
  ba0_int_p i;
  struct ba0_mark M;
  bool redzero_test = true;

  if (type_red == bad_partial_reduction)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_record (&M);
  if (C->attrib.ordering != bav_R_Iordering ())
    {
      bav_R_push_ordering (C->attrib.ordering);
      Abar = bap_new_product_mpz ();
      bap_sort_product_mpz (Abar, A);
    }
  else
    {
      bav_R_push_ordering (C->attrib.ordering);
      Abar = A;
    }

  if (bad_initialized_global.reduction.redzero_strategy ==
      bad_probabilistic_redzero_strategy)
    {
      b = false;
      for (i = 0; (!b) && i < A->size; i++)
        if (bad_is_a_reduced_to_zero_polynom_by_regchain
            (&Abar->tab[i].factor, C, type_red))
          b = true;
      if (b)
        goto fin;
    }

  BA0_TRY
  {
    bad_reduce_product_by_regchain2
        ((bap_product_mpz) 0, (bap_product_mpz) 0,
        Abar, C, type_red, bad_all_derivatives_to_reduce, redzero_test);
/*
   An exception must be raised
*/
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  }
  BA0_CATCH
  {
    if (ba0_global.exception.raised == BAD_EXREDZ)
      b = true;
    else if (ba0_global.exception.raised == BAD_EXNRDZ)
      b = false;
    else
      BA0_RE_RAISE_EXCEPTION;
  }
  BA0_ENDTRY;
fin:
  bav_R_pull_ordering ();
  ba0_restore (&M);
  return b;
}

static void
bad_reduce_product_by_regchain2 (
    bap_product_mpz R,
    bap_product_mpz H,
    bap_product_mpz A,
    bad_regchain C,
    enum bad_typeof_reduction type_red,
    enum bad_typeof_derivative_to_reduce type_der,
    bool redzero_test)
{
  struct bap_product_mpz Abar, Ahat;
  bap_product_mpz Hbar, Hhat;
  struct bap_polynom_mpz F;
  ba0_int_p i, k;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
/*
   First the case A = 0
*/
  if (bap_is_zero_product_mpz (A))
    {
      if (redzero_test)
        BA0_RAISE_EXCEPTION (BAD_EXREDZ);
      ba0_pull_stack ();
      if (R != (bap_product_mpz) 0)
        bap_set_product_zero_mpz (R);
      if (H != (bap_product_mpz) 0)
        bap_set_product_one_mpz (H);
      ba0_restore (&M);
      return;
    }
/*
   One first reduces A factowise. Result in Abar.
*/
  bap_init_product_mpz (&Abar);
  bap_init_product_mpz (&Ahat);
  if (H != (bap_product_mpz) 0)
    {
      Hbar = bap_new_product_mpz ();
      Hhat = bap_new_product_mpz ();
    }
  else
    {
      Hbar = (bap_product_mpz) 0;
      Hhat = (bap_product_mpz) 0;
    }

  if (!redzero_test)
    bap_mul_product_numeric_mpz (&Abar, &Abar, A->num_factor);

  for (i = 0; i < A->size; i++)
    {
      bad_reduce_polynom_by_regchain2
          (&Ahat, Hhat, &A->tab[i].factor, C, type_red, type_der, redzero_test);
      if (bap_is_zero_product_mpz (&Ahat) && redzero_test)
        BA0_RAISE_EXCEPTION (BAD_EXREDZ);
      if (H != (bap_product_mpz) 0)
        {
          bap_pow_product_mpz (Hhat, Hhat, A->tab[i].exponent);
          bap_mul_product_mpz (Hbar, Hbar, Hhat);
        }
      if (bap_is_zero_product_mpz (&Ahat))
        {
          ba0_pull_stack ();
          if (R != (bap_product_mpz) 0)
            bap_set_product_zero_mpz (R);
          if (H != (bap_product_mpz) 0)
            bap_set_product_mpz (H, Hbar);
          ba0_restore (&M);
          return;
        }
      bap_pow_product_mpz (&Ahat, &Ahat, A->tab[i].exponent);
      bap_mul_product_mpz (&Abar, &Abar, &Ahat);
    }
/*
   It may happen that the product is (algebraically) reducible while
	its factors are not.
*/
  bap_init_polynom_mpz (&F);

  while (type_red != bad_partial_reduction &&
      bad_is_a_reducible_product_by_regchain (&Abar, C, type_red, type_der, &k))
    {
      bad_combine_factors_up_to_reducibility
          (&F, &Abar, C->decision_system.tab[k]);
      bad_reduce_polynom_by_regchain2
          (&Ahat, Hhat, &F, C, bad_algebraic_reduction, type_der, redzero_test);
      if (bap_is_zero_product_mpz (&Ahat) && redzero_test)
        BA0_RAISE_EXCEPTION (BAD_EXREDZ);
      if (H != (bap_product_mpz) 0)
        bap_mul_product_mpz (Hbar, Hbar, Hhat);
      if (bap_is_zero_product_mpz (&Ahat))
        {
          ba0_pull_stack ();
          if (R != (bap_product_mpz) 0)
            bap_set_product_zero_mpz (R);
          if (H != (bap_product_mpz) 0)
            bap_set_product_mpz (H, Hbar);
          ba0_restore (&M);
          return;
        }
      bap_mul_product_mpz (&Abar, &Abar, &Ahat);
    }

  if (redzero_test)
    BA0_RAISE_EXCEPTION (BAD_EXNRDZ);

  ba0_pull_stack ();
  if (R != (bap_product_mpz) 0)
    bap_set_product_mpz (R, &Abar);
  if (H != (bap_product_mpz) 0)
    bap_set_product_mpz (H, Hbar);

  ba0_restore (&M);
}
