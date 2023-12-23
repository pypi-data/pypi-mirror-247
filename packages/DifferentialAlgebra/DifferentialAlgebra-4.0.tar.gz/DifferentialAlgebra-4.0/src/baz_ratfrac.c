#include "baz_polyspec_mpz.h"
#include "baz_gcd_polynom_mpz.h"
#include "baz_ratfrac.h"

/*
 * Initializes R to zero.
 */

/*
 * texinfo: baz_init_ratfrac
 * Initialize @var{R} to zero.
 */

BAZ_DLL void
baz_init_ratfrac (
    baz_ratfrac R)
{
  bap_init_polynom_mpz (&R->numer);
  bap_init_polynom_one_mpz (&R->denom);
}

/*
 * texinfo: baz_init_readonly_ratfrac
 * Initialize @var{R} to zero in readonly mode (note: the denominator is
 * not readonly).
 */

BAZ_DLL void
baz_init_readonly_ratfrac (
    baz_ratfrac R)
{
  bap_init_readonly_polynom_mpz (&R->numer);
  bap_init_polynom_one_mpz (&R->denom);
}

/*
 * texinfo: baz_new_ratfrac
 * Allocate a new ratfrac, initialize it and return it.
 */

BAZ_DLL baz_ratfrac
baz_new_ratfrac (
    void)
{
  baz_ratfrac A;

  A = (baz_ratfrac) ba0_alloc (sizeof (struct baz_ratfrac));
  baz_init_ratfrac (A);
  return A;
}

/*
 * texinfo: baz_set_ratfrac
 * Assign @var{B} to @var{A}.
 */

BAZ_DLL void
baz_set_ratfrac (
    baz_ratfrac A,
    baz_ratfrac B)
{
  if (A != B)
    {
      bap_set_polynom_mpz (&A->numer, &B->numer);
      bap_set_polynom_mpz (&A->denom, &B->denom);
    }
}

/*
 * texinfo: baz_set_ratfrac_zero
 * Assign @math{0} to @var{A}.
 */

BAZ_DLL void
baz_set_ratfrac_zero (
    baz_ratfrac A)
{
  bap_set_polynom_zero_mpz (&A->numer);
  bap_set_polynom_one_mpz (&A->denom);
}

/*
 * texinfo: baz_set_ratfrac_one
 * Assign @math{1} to @var{A}.
 */

BAZ_DLL void
baz_set_ratfrac_one (
    baz_ratfrac A)
{
  bap_set_polynom_one_mpz (&A->numer);
  bap_set_polynom_one_mpz (&A->denom);
}

/*
 * texinfo: baz_set_ratfrac_term
 * Assign @var{T} to @var{R}.
 */

BAZ_DLL void
baz_set_ratfrac_term (
    baz_ratfrac R,
    bav_term T)
{
  bap_set_polynom_term_mpz (&R->numer, T);
  bap_set_polynom_one_mpz (&R->denom);
}

/*
 * texinfo: baz_set_ratfrac_polynom
 * Assign @var{A} to @var{R}.
 */

BAZ_DLL void
baz_set_ratfrac_polynom (
    baz_ratfrac R,
    bap_polynom_mpz A)
{
  bap_set_polynom_mpz (&R->numer, A);
  bap_set_polynom_one_mpz (&R->denom);
}

/*
 * texinfo: baz_set_ratfrac_fraction
 * Assign @math{P/Q} to @var{R}.
 */

BAZ_DLL void
baz_set_ratfrac_fraction (
    baz_ratfrac R,
    bap_polynom_mpz P,
    bap_polynom_mpz Q)
{
  if (bap_is_zero_polynom_mpz (P))
    baz_set_ratfrac_zero (R);
  else if (bap_is_zero_polynom_mpz (Q))
    BA0_RAISE_EXCEPTION (BA0_ERRIVZ);
  else
    {
      bap_set_polynom_mpz (&R->numer, P);
      bap_set_polynom_mpz (&R->denom, Q);
    }
}

/*
 * A parsing function for @code{baz_rel_ratfrac}.
 * The only relational operator recognized is the equality sign.
 * This function is called by @code{ba0_scanf/%relQz}.

BAZ_DLL void *
baz_scanf_ratfrac_eqn (
    void *R)
{
  baz_ratfrac A = (baz_ratfrac) R;
  struct baz_ratfrac B, C;
  struct ba0_mark M;

  if (A == (baz_ratfrac) 0)
    A = baz_new_ratfrac ();

  ba0_push_another_stack ();
  ba0_record (&M);

  baz_init_ratfrac (&B);
  baz_scanf_ratfrac (&B);

  if (!ba0_sign_token_analex ("="))
    {
      ba0_pull_stack ();
      baz_set_ratfrac (A, &B);
    }
  else
    {
      baz_init_ratfrac (&C);
      ba0_get_token_analex ();
      baz_scanf_ratfrac (&C);
      ba0_pull_stack ();
      baz_sub_ratfrac (A, &B, &C);
    }

  ba0_restore (&M);
  return A;
}
 */

static void *baz_scanf2_ratfrac (
    void *);

BAZ_DLL void *
baz_scanf_ratfrac (
    void *R)
{
  baz_ratfrac A;

  A = (baz_ratfrac) baz_scanf2_ratfrac (R);
  baz_reduce_ratfrac (A, A);
  return A;
}

static void *
baz_scanf2_ratfrac (
    void *R)
{
  baz_ratfrac A = (baz_ratfrac) R;
  struct baz_ratfrac S, P;
  struct ba0_mark M;

  if (A == (baz_ratfrac) 0)
    A = baz_new_ratfrac ();

  ba0_push_another_stack ();
  ba0_record (&M);
  baz_init_ratfrac (&S);
  baz_init_ratfrac (&P);

  if (!ba0_sign_token_analex ("-"))
    {
      baz_scanf_product_ratfrac (&S);
      ba0_get_token_analex ();
    }
  while (ba0_sign_token_analex ("+") || ba0_sign_token_analex ("-"))
    {
      if (ba0_sign_token_analex ("+"))
        {
          ba0_get_token_analex ();
          baz_scanf_product_ratfrac (&P);
          ba0_get_token_analex ();
          baz_add_ratfrac (&S, &S, &P);
        }
      else
        {
          ba0_get_token_analex ();
          baz_scanf_product_ratfrac (&P);
          ba0_get_token_analex ();
          baz_sub_ratfrac (&S, &S, &P);
        }
    }
  ba0_unget_token_analex (1);
  ba0_pull_stack ();
  baz_set_ratfrac (A, &S);
  ba0_restore (&M);
  return A;
}

static ba0_scanf_function baz_scanf_power_ratfrac;

BAZ_DLL void *
baz_scanf_product_ratfrac (
    void *AA)
{
  baz_ratfrac A;
  struct baz_ratfrac B;
  struct ba0_mark M;

  if (AA == (void *) 0)
    A = baz_new_ratfrac ();
  else
    A = (baz_ratfrac) AA;

  ba0_push_another_stack ();
  ba0_record (&M);
  baz_init_ratfrac (&B);
  ba0_pull_stack ();

  baz_scanf_power_ratfrac (A);

  ba0_get_token_analex ();
  while (ba0_sign_token_analex ("*") || ba0_sign_token_analex ("/"))
    {
      if (ba0_sign_token_analex ("*"))
        {
          ba0_get_token_analex ();
          ba0_push_another_stack ();
          baz_scanf_power_ratfrac (&B);
          ba0_pull_stack ();
          baz_mul_ratfrac (A, A, &B);
        }
      else
        {
          ba0_get_token_analex ();
          ba0_push_another_stack ();
          baz_scanf_power_ratfrac (&B);
          ba0_pull_stack ();
          baz_div_ratfrac (A, A, &B);
        }
      ba0_get_token_analex ();
    }

  ba0_unget_token_analex (1);

  ba0_restore (&M);
  return A;
}

static ba0_scanf_function baz_scanf_atomic_ratfrac;

static void *
baz_scanf_power_ratfrac (
    void *AA)
{
  baz_ratfrac A;
  bav_Idegree d = 0;            /* to avoid a warning */
  bool exponent;

  if (AA == (void *) 0)
    A = baz_new_ratfrac ();
  else
    A = (baz_ratfrac) AA;

  baz_scanf_atomic_ratfrac (A);
  ba0_get_token_analex ();

  exponent = false;
  if (ba0_sign_token_analex ("^"))
    exponent = true;
  else if (ba0_sign_token_analex ("*"))
    {
      ba0_get_token_analex ();
      if (ba0_sign_token_analex ("*"))
        exponent = true;
      else
        ba0_unget_token_analex (1);
    }

  if (exponent)
    {
      ba0_get_token_analex ();
      if (ba0_type_token_analex () == ba0_integer_token)
        d = (bav_Idegree) atoi (ba0_value_token_analex ());
      else if (ba0_sign_token_analex ("("))
        ba0_scanf ("(%d)", &d);
      else
        BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);
      baz_pow_ratfrac (A, A, d);
    }
  else
    ba0_unget_token_analex (1);

  return A;
}

static void *
baz_scanf_atomic_ratfrac (
    void *AA)
{
  baz_ratfrac A;
  struct bap_polynom_mpz P;
  bav_variable v;
  ba0_mpz_t c;
  struct ba0_mark M;

  if (AA == (void *) 0)
    A = baz_new_ratfrac ();
  else
    A = (baz_ratfrac) AA;

  if (ba0_type_token_analex () == ba0_integer_token)
    {
      struct bav_rank rg;

      ba0_push_another_stack ();
      ba0_record (&M);
      ba0_mpz_init (c);
      ba0_scanf ("%z", c);
      bap_init_polynom_mpz (&P);
      rg = bav_constant_rank ();
      bap_set_polynom_crk_mpz (&P, c, &rg);
      ba0_pull_stack ();
      baz_set_ratfrac_polynom (A, &P);
      ba0_restore (&M);
    }
  else if (ba0_type_token_analex () == ba0_string_token)
    {
      ba0_push_another_stack ();
      ba0_record (&M);
      bap_init_polynom_mpz (&P);
      ba0_scanf ("%v", &v);
/*
 * Do not check for zero derivatives of parameters
 */
      bap_set_polynom_variable_mpz (&P, v, 1);
      ba0_pull_stack ();
      baz_set_ratfrac_polynom (A, &P);
      ba0_restore (&M);
    }
  else if (ba0_sign_token_analex ("("))
    {
      ba0_get_token_analex ();
      baz_scanf2_ratfrac (A);
      ba0_get_token_analex ();
      if (!ba0_sign_token_analex (")"))
        BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);
    }
  else
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);
  return A;
}

/*
 * texinfo: baz_scanf_expanded_ratfrac
 * Parsing functions for rational fractions.
 * The numerator and the denominator are supposed to be expanded
 * polynomials over the rational numbers.
 * They are parsed by @code{bap_scanf_expanded_polynom_mpq}.
 * This function is called by @code{ba0_scanf/%expanded_Qz}.
 */

BAZ_DLL void *
baz_scanf_expanded_ratfrac (
    void *AA)
{
  baz_ratfrac A;
  struct bap_polynom_mpq Anum, Aden;
  struct ba0_mark M;
  ba0_mpq_t q;
  ba0_mpz_t qnum, qden;
  ba0_mpz_t den_numer, den_denom;
  bool minus, coeffnum;
  ba0_int_p n;

  if (AA == (void *) 0)
    A = baz_new_ratfrac ();
  else
    A = (baz_ratfrac) AA;

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * Read a possible starting minus sign.
 * This minus sign will only matter if there is a leading numerical factor.
 * It will then apply to this factor.
 */

  if (ba0_sign_token_analex ("-"))
    {
      ba0_get_token_analex ();
      minus = true;
      n = 1;
    }
  else
    {
      minus = false;
      n = 0;
    }
/*
 * Read a possible leading numerical factor.
 * We are not yet sure that the numerical factor is a global factor.
 *
 * Observe that we cannot read directly a rational number for
 * a rational fraction of the form 1/u would raise an exception.
 */
  ba0_mpz_init_set_ui (qnum, 1);
  ba0_mpz_init_set_ui (qden, 1);
  if (ba0_type_token_analex () == ba0_integer_token)
    {
      coeffnum = true;
      ba0_scanf_mpz (qnum);
      ba0_get_token_analex ();
      n += 1;
      if (ba0_sign_token_analex ("/"))
        {
          ba0_get_token_analex ();
          n += 1;
          if (ba0_type_token_analex () == ba0_integer_token)
            {
              ba0_scanf_mpz (qden);
              ba0_get_token_analex ();
              n += 1;
            }
          else
            {
              ba0_unget_token_analex (1);
              n -= 1;
            }
        }
    }
  else
    coeffnum = false;
  ba0_mpq_init (q);
  ba0_mpq_set_num (q, qnum);
  ba0_mpq_set_den (q, qden);
  ba0_mpq_canonicalize (q);
  if (minus)
    ba0_mpq_neg (q, q);
/*
 * If there is a leading numerical factor then, it is in q.
 * The minus sign is taken into account.
 * 
 * If there is no leading numerical factor then we will have to
 * undo all ba0_get_token before reding the numerator. In this case,
 * the number of ba0_unget_token to perform is stored in n.
 */
  if (!coeffnum)
    {
      if (ba0_sign_token_analex ("*") || ba0_sign_token_analex ("/")
          || ba0_sign_token_analex ("+") || ba0_sign_token_analex ("-"))
        BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);
    }
/*
 * Let us read the numerator and denominator of the rational fraction
 */
  bap_init_polynom_mpq (&Anum);
  bap_init_polynom_mpq (&Aden);
  bap_set_polynom_one_mpq (&Anum);
  bap_set_polynom_one_mpq (&Aden);

  if ((coeffnum && ba0_sign_token_analex ("*")) || !coeffnum)
    {
      if (ba0_sign_token_analex ("*"))
        {
          ba0_get_token_analex ();
          n += 1;
        }
      if (!ba0_sign_token_analex ("("))
        {
/*
 * The leading rational is actually not a leading numerical factor.
 * Undo all ba0_get_token_analex and reset q to 1/1.
 */
          while (n > 0)
            {
              ba0_unget_token_analex (1);
              n -= 1;
            }
          ba0_mpq_set_ui (q, 1);
        }
/*
 * Read numerator and denominator
 */
      bap_scanf_expanded_polynom_mpq (&Anum);
      ba0_get_token_analex ();
      if (ba0_sign_token_analex ("/"))
        {
          ba0_get_token_analex ();
          bap_scanf_expanded_polynom_mpq (&Aden);
        }
      else
        ba0_unget_token_analex (1);
    }
  else if (ba0_sign_token_analex ("+") || ba0_sign_token_analex ("-"))
    {
/*
 * numerical factor +/- ...
 */
      while (n > 0)
        {
          ba0_unget_token_analex (1);
          n -= 1;
        }
      ba0_mpq_set_ui (q, 1);
/*
 * Read numerator 
 */
      bap_scanf_expanded_polynom_mpq (&Anum);
    }
  else if (ba0_sign_token_analex ("/"))
    {
      ba0_get_token_analex ();
      bap_scanf_expanded_polynom_mpq (&Aden);
    }
  else
    ba0_unget_token_analex (1);
/*
 * Incorporate the numerical factor q in Anum.
 */
  bap_mul_polynom_numeric_mpq (&Anum, &Anum, q);
/*
 * Let us compute the result
 */
  ba0_pull_stack ();

  ba0_mpz_init (den_numer);
  ba0_mpz_init (den_denom);
  bap_numer_polynom_mpq (&A->numer, den_numer, &Anum);
  bap_numer_polynom_mpq (&A->denom, den_denom, &Aden);
  bap_mul_polynom_numeric_mpz (&A->numer, &A->numer, den_denom);
  bap_mul_polynom_numeric_mpz (&A->denom, &A->denom, den_numer);
  if (ba0_mpz_sgn (*bap_numeric_initial_polynom_mpz (&A->denom)) < 0)
    {
      bap_neg_polynom_mpz (&A->numer, &A->numer);
      bap_neg_polynom_mpz (&A->denom, &A->denom);
    }
  ba0_restore (&M);
  return A;
}

/*
 * texinfo: baz_scanf_careful_expanded_ratfrac
 * Parsing functions for rational fractions.
 * The numerator and the denominator are supposed to be expanded
 * polynomials over the rational numbers.
 * Expressions such as @code{u[x,y] - u[y,x]} are recognized to be @math{0}.
 * Zero derivatives of parameters are simplified to @math{0}.
 * This function is called by @code{ba0_scanf/%careful_expanded_Qz}.
 */

BAZ_DLL void *
baz_scanf_careful_expanded_ratfrac (
    void *AA)
{
  baz_ratfrac A;
/*
 * Fix me.
 * not a call to scanf_expanded_ratfrac which misses some cases.
 * The call to baz_scanf2_ratfrac catches u[x,y] - u[y,x] = 0
 */
  A = baz_scanf2_ratfrac (AA);
  if (!bav_depends_on_zero_derivatives_of_parameter_term
      (&A->numer.total_rank, &bav_global.parameters) &&
      !bav_depends_on_zero_derivatives_of_parameter_term
      (&A->denom.total_rank, &bav_global.parameters))
    {
      baz_reduce_ratfrac (A, A);
      return A;
    }

  if (bav_depends_on_zero_derivatives_of_parameter_term
      (&A->denom.total_rank, &bav_global.parameters))
    {
      bap_simplify_zero_derivatives_of_parameter_polynom_mpz
          (&A->denom, &A->denom, &bav_global.parameters);
      if (bap_is_zero_polynom_mpz (&A->denom))
        BA0_RAISE_EXCEPTION (BA0_ERRIVZ);
/*
 * In the case of an exception, A gets corrupted.
 */
    }
  if (bav_depends_on_zero_derivatives_of_parameter_term
      (&A->numer.total_rank, &bav_global.parameters))
    bap_simplify_zero_derivatives_of_parameter_polynom_mpz
        (&A->numer, &A->numer, &bav_global.parameters);
  baz_reduce_ratfrac (A, A);
  return A;
}

/*
 * texinfo: baz_printf_ratfrac
 * The general printing function for rational fractions.
 * It is called by @code{ba0_printf/%Qz}.
 */

BAZ_DLL void
baz_printf_ratfrac (
    void *AA)
{
  baz_ratfrac A = (baz_ratfrac) AA;

  if (baz_is_zero_ratfrac (A))
    ba0_put_char ('0');
  else if (bap_is_one_polynom_mpz (&A->denom))
    bap_printf_polynom_mpz (&A->numer);
  else
    {
      ba0_put_char ('(');
      bap_printf_polynom_mpz (&A->numer);
      ba0_put_string (")/(");
      bap_printf_polynom_mpz (&A->denom);
      ba0_put_char (')');
    }
}

/*
 * Readonly static data
 */

static char _struct_ratfrac[] = "struct baz_ratfrac";

BAZ_DLL ba0_int_p
baz_garbage1_ratfrac (
    void *AA,
    enum ba0_garbage_code code)
{
  baz_ratfrac A = (baz_ratfrac) AA;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (A, sizeof (struct baz_ratfrac), _struct_ratfrac);

  n += bap_garbage1_polynom_mpz (&A->numer, ba0_embedded);
  n += bap_garbage1_polynom_mpz (&A->denom, ba0_embedded);

  return n;
}

BAZ_DLL void *
baz_garbage2_ratfrac (
    void *AA,
    enum ba0_garbage_code code)
{
  baz_ratfrac A;

  if (code == ba0_isolated)
    A = ba0_new_addr_gc_info (AA, _struct_ratfrac);
  else
    A = (baz_ratfrac) AA;

  bap_garbage2_polynom_mpz (&A->numer, ba0_embedded);
  bap_garbage2_polynom_mpz (&A->denom, ba0_embedded);
  return A;
}

BAZ_DLL void *
baz_copy_ratfrac (
    void *AA)
{
  baz_ratfrac B;

  B = baz_new_ratfrac ();
  baz_set_ratfrac (B, (baz_ratfrac) AA);
  return B;
}

/*
 * texinfo: baz_sort_ratfrac
 * Sort @var{A} with respect to the current ordering.
 * The result, which is readonly, is stored in @var{R}.
 */

BAZ_DLL void
baz_sort_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A)
{
  bap_sort_polynom_mpz (&R->numer, &A->numer);
  bap_sort_polynom_mpz (&R->denom, &A->denom);
}

/*
 * texinfo: baz_physort_ratfrac
 * Apply @code{bap_physort_polynom_mpz} over the numerator and
 * the denominator of @var{R}.
 */

BAZ_DLL void
baz_physort_ratfrac (
    baz_ratfrac R)
{
  bap_physort_polynom_mpz (&R->numer);
  bap_physort_polynom_mpz (&R->denom);
}

/*
 * texinfo: baz_is_zero_ratfrac
 * Return @code{true} if @var{R} if @math{0}.
 */

BAZ_DLL bool
baz_is_zero_ratfrac (
    baz_ratfrac R)
{
  return bap_is_zero_polynom_mpz (&R->numer);
}

/*
 * texinfo: baz_is_one_ratfrac
 * Return @code{true} if @var{R} is @math{1}.
 */

BAZ_DLL bool
baz_is_one_ratfrac (
    baz_ratfrac R)
{
  return bap_equal_polynom_mpz (&R->numer, &R->denom);
}

/*
 * texinfo: baz_is_numeric_ratfrac
 * Return @code{true} if the numerator and the denomnator of @var{R}
 * are numerical.
 */

BAZ_DLL bool
baz_is_numeric_ratfrac (
    baz_ratfrac R)
{
  return bap_is_numeric_polynom_mpz (&R->numer) &&
      bap_is_numeric_polynom_mpz (&R->denom);
}

/*
 * texinfo: baz_equal_ratfrac
 * Return @code{true} if @var{A} and @var{B} have the same numerator and the
 * same denominator.
 */

BAZ_DLL bool
baz_equal_ratfrac (
    baz_ratfrac A,
    baz_ratfrac B)
{
  return bap_equal_polynom_mpz (&A->numer, &B->numer) &&
      bap_equal_polynom_mpz (&A->denom, &B->denom);
}

/*
 * texinfo: baz_depend_ratfrac
 * Return @code{true} if @var{A} depends on @var{v}.
 */

BAZ_DLL bool
baz_depend_ratfrac (
    baz_ratfrac A,
    bav_variable v)
{
  return bap_depend_polynom_mpz (&A->numer, v) ||
      bap_depend_polynom_mpz (&A->denom, v);
}

/*
 * texinfo: baz_mark_indets_ratfrac
 * Assign @code{true} to the field @code{hack} of all variables occuring
 * in @var{R}. This function is often used in conjunction with
 * @code{bav_R_marked_variables}.
 */

BAZ_DLL void
baz_mark_indets_ratfrac (
    baz_ratfrac R)
{
  bap_mark_indets_polynom_mpz (&R->numer);
  bap_mark_indets_polynom_mpz (&R->denom);
}

/*
 * texinfo: baz_leader_ratfrac
 * Return the highest variable occuring in the numerator and the denominator
 * of @var{A}. The rational fraction is supposed to be reduced.
 * Exception @code{BAP_ERRCST} is raised if @var{R} is numerical.
 */

BAZ_DLL bav_variable
baz_leader_ratfrac (
    baz_ratfrac R)
{
  bav_variable w = BAV_NOT_A_VARIABLE;

  if (bap_is_numeric_polynom_mpz (&R->numer))
    {
      if (bap_is_numeric_polynom_mpz (&R->denom))
        BA0_RAISE_EXCEPTION (BAP_ERRCST);
      else
        w = bap_leader_polynom_mpz (&R->denom);
    }
  else if (bap_is_numeric_polynom_mpz (&R->denom))
    w = bap_leader_polynom_mpz (&R->numer);
  else
    {
      bav_variable u, v;
/*
 * The fraction is supposed to be reduced
 */
      u = bap_leader_polynom_mpz (&R->numer);
      v = bap_leader_polynom_mpz (&R->denom);
      w = bav_R_variable_number (u) > bav_R_variable_number (v) ? u : v;
    }
  return w;
}

static struct bav_rank
baz_rank_ratfrac2 (
    bap_polynom_mpz numer,
    bap_polynom_mpz denom)
{
  struct bav_rank rg, rgnum, rgden;
#undef BAP_OLD_RANKDEF
#if defined (BAP_OLD_RANKDEF)
  struct bap_polynom_mpz rem;
  struct ba0_mark M;
#endif

  rgnum = bap_rank_polynom_mpz (numer);
  rgden = bap_rank_polynom_mpz (denom);
  if (bav_is_constant_rank (&rgden))
    rg = rgnum;
  else if (bav_is_constant_rank (&rgnum))
    {
      rg.var = rgden.var;
      rg.deg = -rgden.deg;
    }
  else if (bav_R_variable_number (rgnum.var) >
      bav_R_variable_number (rgden.var))
    rg = rgnum;
  else if (bav_R_variable_number (rgnum.var) <
      bav_R_variable_number (rgden.var))
    {
      rg.var = rgden.var;
      rg.deg = -rgden.deg;
    }
  else if (rgnum.deg != rgden.deg)
    {
      rg.var = rgnum.var;
      rg.deg = rgnum.deg - rgden.deg;
    }
  else
#if defined (BAP_OLD_RANKDEF)
    {
      ba0_record (&M);
      bap_init_polynom_mpz (&rem);
      bap_prem_polynom_mpz (&rem, (bav_Idegree *) 0, numer, denom, rgnum.var);
      rg = baz_rank_ratfrac2 (&rem, denom);
      ba0_restore (&M);
    }
#else
    rg = bav_constant_rank2 (rgnum.var);
#endif
  return rg;
}

/*
 * texinfo: baz_rank_ratfrac
 * Return the rank of @var{A}, which is defined as follows:
 * if @var{A} is numeric, then its rank is the constant rank (or the rank
 * of zero), else it is @math{v^{n-d}} where @math{v}, @math{n} and @math{d}
 * denote the leader of @var{A}, the degree of its numerator in @math{v}
 * and the degree of its denominator in @math{v}. When @math{n=d}, the
 * rank of @math{A} is the constant rank.
 */

BAZ_DLL struct bav_rank
baz_rank_ratfrac (
    baz_ratfrac R)
{
  return baz_rank_ratfrac2 (&R->numer, &R->denom);
}

/*
 * texinfo: baz_initial_ratfrac
 * Assign to @var{init} the initial of @var{R} in readonly mode.
 * Raises the exception @code{BAP_ERRNHL} if the rank of @var{R}
 * has negative degree.
 */

BAZ_DLL void
baz_initial_ratfrac (
    baz_ratfrac init,
    baz_ratfrac R)
{
  struct bav_rank rg;

  rg = baz_rank_ratfrac (R);
  if (rg.deg <= 0)
    BA0_RAISE_EXCEPTION (BAZ_ERRNHL);
  if (init != R)
    bap_set_readonly_polynom_mpz (&init->denom, &R->denom);
  bap_initial_polynom_mpz (&init->numer, &R->numer);
}

/*
 * texinfo: baz_reductum_ratfrac
 * Assign to @var{reductum} the reductum of @var{R} in readonly mode.
 * Raises the exception @code{BAP_ERRNHL} if the rank of @var{R}
 * has negative degree.
 */

BAZ_DLL void
baz_reductum_ratfrac (
    baz_ratfrac reductum,
    baz_ratfrac R)
{
  struct bav_rank rg;

  rg = baz_rank_ratfrac (R);
  if (rg.deg <= 0)
    BA0_RAISE_EXCEPTION (BAZ_ERRNHL);
  if (reductum != R)
    bap_set_readonly_polynom_mpz (&reductum->denom, &R->denom);
  bap_reductum_polynom_mpz (&reductum->numer, &R->numer);
}

/*
 * texinfo: baz_lcoeff_and_reductum_ratfrac
 * Assign to @var{lcoeff} and @var{reductum} the leading coefficient and
 * the reductum of @var{R} w.r.t. @var{v}. The variable @var{v} does not
 * need to be greater than or equal to the leading variable of @var{R}.
 * If @var{v} is the zero pointer, it is taken to be the leading variable
 * of @var{R}.
 * The rational fraction @var{R} may be a numerical rational fraction.
 * In that case, @var{R} is assigned to @var{lcoeff} and zero is
 * assigned to @var{reductum}.
 * The resulting rational fractions are plain rational fractions (not readonly).
 * Exception @code{BAP_ERRNHL} is raised if @var{v} is zero and the rank
 * of @var{R} has negative degree.
 * Exception @code{BAP_ERRVPD} is raised if @var{v} is nonzero and is 
 * present in the denominator of @var{R}.
 */

BAZ_DLL void
baz_lcoeff_and_reductum_ratfrac (
    baz_ratfrac lcoeff,
    baz_ratfrac reductum,
    baz_ratfrac R,
    bav_variable v)
{
  struct bav_rank rg;

  if (v == BAV_NOT_A_VARIABLE)
    {
      rg = baz_rank_ratfrac (R);
      if (rg.deg <= 0)
        BA0_RAISE_EXCEPTION (BAZ_ERRNHL);
    }
  else if (bap_depend_polynom_mpz (&R->denom, v))
    BA0_RAISE_EXCEPTION (BAZ_ERRVPD);

  if (lcoeff != (baz_ratfrac) 0 && lcoeff != R)
    bap_set_polynom_mpz (&lcoeff->denom, &R->denom);
  if (reductum != (baz_ratfrac) 0 && reductum != R)
    bap_set_polynom_mpz (&reductum->denom, &R->denom);
  bap_lcoeff_and_reductum_polynom_mpz
      (lcoeff !=
      (baz_ratfrac) 0 ? &lcoeff->numer : (bap_polynom_mpz) 0,
      reductum !=
      (baz_ratfrac) 0 ? &reductum->numer : (bap_polynom_mpz) 0, &R->numer, v);
}

/*
 * texinfo: baz_numer_ratfrac
 * Assign to @var{A} the numerator of @var{R}.
 */

BAZ_DLL void
baz_numer_ratfrac (
    bap_polynom_mpz A,
    baz_ratfrac R)
{
  bap_set_polynom_mpz (A, &R->numer);
}

/*
 * texinfo: baz_denom_ratfrac
 * Assign to @var{A} the denominator of @var{R}.
 */

BAZ_DLL void
baz_denom_ratfrac (
    bap_polynom_mpz A,
    baz_ratfrac R)
{
  bap_set_polynom_mpz (A, &R->denom);
}

/*
 * texinfo: baz_reduce_numeric_ratfrac
 * Divide the numerator and the denominator of @var{A} by the gcd of their
 * numerical content. Result in @var{R}.
 * The numerical leading coefficient of the denominator of @var{R} is positive.
 */

BAZ_DLL void
baz_reduce_numeric_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A)
{
  ba0_mpz_t contnum, contden, gcd;
  struct ba0_mark M;

  if (baz_is_zero_ratfrac (A))
    baz_set_ratfrac_zero (R);
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);
      ba0_mpz_init (contnum);
      ba0_mpz_init (contden);
      ba0_mpz_init (gcd);
      bap_numeric_content_polynom_mpz (contnum, &A->numer);
      bap_numeric_content_polynom_mpz (contden, &A->denom);
      ba0_mpz_gcd (gcd, contnum, contden);
      if (ba0_mpz_sgn (*bap_numeric_initial_polynom_mpz (&A->denom)) < 0)
        ba0_mpz_neg (gcd, gcd);
      ba0_pull_stack ();
      bap_exquo_polynom_numeric_mpz (&R->numer, &A->numer, gcd);
      bap_exquo_polynom_numeric_mpz (&R->denom, &A->denom, gcd);
      ba0_restore (&M);
    }
}

/*
 * texinfo: baz_reduce_ratfrac
 * Assign to @var{R} the reduced fraction @var{A}.
 * The gcd of the numerator and the denominator of @var{A} is factored out.
 * The numerical leading coefficient of the denominator of @var{R} is positive.
 */

BAZ_DLL void
baz_reduce_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A)
{
  if (bap_is_zero_polynom_mpz (&A->numer))
    baz_set_ratfrac_zero (R);
  else if (bap_is_numeric_polynom_mpz (&A->denom))
    baz_reduce_numeric_ratfrac (R, A);
  else
    {
      baz_gcd_polynom_mpz
          (BAP_NOT_A_POLYNOM_mpz, &R->numer, &R->denom, &A->numer, &A->denom);
      if (ba0_mpz_sgn (*bap_numeric_initial_polynom_mpz (&R->denom)) < 0)
        {
          bap_neg_polynom_mpz (&R->numer, &R->numer);
          bap_neg_polynom_mpz (&R->denom, &R->denom);
        }
    }
}

/*
 * texinfo: baz_neg_ratfrac
 * Assign @math{- A} to @var{R}.
 */

BAZ_DLL void
baz_neg_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A)
{
  bap_neg_polynom_mpz (&R->numer, &A->numer);
  if (R != A)
    bap_set_polynom_mpz (&R->denom, &A->denom);
}

/*
 * texinfo: baz_add_ratfrac
 * Assign @math{A + B} to @math{R}.
 */

BAZ_DLL void
baz_add_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    baz_ratfrac B)
{
  struct bap_polynom_mpz Abar, Bbar;
  struct ba0_mark M;

  if (bap_equal_polynom_mpz (&A->denom, &B->denom))
    {
      bap_add_polynom_mpz (&R->numer, &A->numer, &B->numer);
      if (R != A && R != B)
        bap_set_polynom_mpz (&R->denom, &A->denom);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_polynom_mpz (&Abar);
  bap_init_polynom_mpz (&Bbar);
  bap_mul_polynom_mpz (&Bbar, &A->numer, &B->denom);
  bap_mul_polynom_mpz (&Abar, &B->numer, &A->denom);

  ba0_pull_stack ();

  bap_add_polynom_mpz (&R->numer, &Abar, &Bbar);
  if (bap_is_zero_polynom_mpz (&R->numer))
    baz_set_ratfrac_zero (R);
  else
    bap_mul_polynom_mpz (&R->denom, &A->denom, &B->denom);

  ba0_restore (&M);
}

/*
 * texinfo: baz_sub_ratfrac
 * Assign @math{A - B} to @math{R}.
 */

BAZ_DLL void
baz_sub_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    baz_ratfrac B)
{
  struct bap_polynom_mpz Abar, Bbar;
  struct ba0_mark M;

  if (bap_equal_polynom_mpz (&A->denom, &B->denom))
    {
      bap_sub_polynom_mpz (&R->numer, &A->numer, &B->numer);
      if (R != A && R != B)
        bap_set_polynom_mpz (&R->denom, &A->denom);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_polynom_mpz (&Abar);
  bap_init_polynom_mpz (&Bbar);
  bap_mul_polynom_mpz (&Bbar, &A->numer, &B->denom);
  bap_mul_polynom_mpz (&Abar, &B->numer, &A->denom);

  ba0_pull_stack ();

  bap_sub_polynom_mpz (&R->numer, &Bbar, &Abar);
  if (bap_is_zero_polynom_mpz (&R->numer))
    baz_set_ratfrac_zero (R);
  else
    bap_mul_polynom_mpz (&R->denom, &A->denom, &B->denom);

  ba0_restore (&M);
}

/*
 * texinfo: baz_mul_ratfrac_numeric
 * Assign @math{c\,A} to @math{R}.
 */

BAZ_DLL void
baz_mul_ratfrac_numeric (
    baz_ratfrac R,
    baz_ratfrac A,
    ba0_mpz_t c)
{
  if (baz_is_zero_ratfrac (A) || ba0_mpz_sgn (c) == 0)
    baz_set_ratfrac_zero (R);
  else
    {
      if (!ba0_mpz_is_one (c))
        bap_mul_polynom_numeric_mpz (&R->numer, &A->numer, c);
      if (R != A)
        bap_set_polynom_mpz (&R->denom, &A->denom);
    }
}

/*
 * texinfo: baz_mul_ratfrac_numeric_mpq
 * Assign @math{q\,A} to @math{R}.
 */

BAZ_DLL void
baz_mul_ratfrac_numeric_mpq (
    baz_ratfrac R,
    baz_ratfrac A,
    ba0_mpq_t q)
{
  if (baz_is_zero_ratfrac (A) || ba0_mpz_sgn (ba0_mpq_numref (q)) == 0)
    baz_set_ratfrac_zero (R);
  else
    {
      if (!ba0_mpq_is_one (q))
        {
          bap_mul_polynom_numeric_mpz (&R->numer, &A->numer, ba0_mpq_numref (q));
          bap_mul_polynom_numeric_mpz (&R->denom, &A->denom, ba0_mpq_denref (q));
        }
      if (R != A)
        bap_set_polynom_mpz (&R->denom, &A->denom);
    }
}

/*
 * texinfo: baz_mul_ratfrac_variable
 * Assign @math{A\,v^d} to @var{R}.
 */

BAZ_DLL void
baz_mul_ratfrac_variable (
    baz_ratfrac R,
    baz_ratfrac A,
    bav_variable v,
    bav_Idegree d)
{
  struct bav_term term;
  bav_Idegree e;
  struct ba0_mark M;

  if (d == 0)
    {
      if (A != R)
        baz_set_ratfrac (R, A);
      return;
    }
  else
    {
      bap_is_variable_factor_polynom_mpz (&A->denom, v, &e);
      if (e == 0)
        {
          bap_mul_polynom_variable_mpz (&R->numer, &A->numer, v, d);
          if (A != R)
            bap_set_polynom_mpz (&R->denom, &A->denom);
        }
      else
        {
          if (e < d)
            bap_mul_polynom_variable_mpz (&R->numer, &A->numer, v, d - e);

          ba0_push_another_stack ();
          ba0_record (&M);
          bav_init_term (&term);
          bav_set_term_variable (&term, v, e);
          ba0_pull_stack ();

          bap_exquo_polynom_term_mpz (&R->denom, &A->denom, &term);

          ba0_restore (&M);
        }
    }
}


/*
 * texinfo: baz_mul_ratfrac
 * Assign @math{A\,B} to @math{R}.
 */

BAZ_DLL void
baz_mul_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    baz_ratfrac B)
{
  bap_mul_polynom_mpz (&R->numer, &A->numer, &B->numer);
  if (bap_is_zero_polynom_mpz (&R->numer))
    baz_set_ratfrac_zero (R);
  else
    bap_mul_polynom_mpz (&R->denom, &A->denom, &B->denom);
}

/*
 * texinfo: baz_invert_ratfrac
 * Assign @math{1/A} to @math{R}.
 */

BAZ_DLL void
baz_invert_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A)
{
  if (baz_is_zero_ratfrac (A))
    BA0_RAISE_EXCEPTION (BA0_ERRIVZ);
  if (R == A)
    {
      BA0_SWAP (struct bap_polynom_mpz,
          R->numer,
          R->denom);
    }
  else
    {
      bap_set_polynom_mpz (&R->numer, &A->denom);
      bap_set_polynom_mpz (&R->denom, &A->numer);
    }
}

/*
 * texinfo: baz_div_ratfrac
 * Assign @math{A/B} to @math{R}.
 */

BAZ_DLL void
baz_div_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    baz_ratfrac B)
{
  struct baz_ratfrac C;

  if (baz_is_zero_ratfrac (B))
    BA0_RAISE_EXCEPTION (BA0_ERRIVZ);

  C.numer = B->denom;
  C.denom = B->numer;

  baz_mul_ratfrac (R, A, &C);
}

/*
 * texinfo: baz_pow_ratfrac
 * Assign @math{A^d} to @var{R}. The exponent @var{d} is allowed to be negative.
 */

BAZ_DLL void
baz_pow_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    bav_Idegree d)
{
  if (d == 0)
    baz_set_ratfrac_one (R);
  else if (d == 1)
    {
      if (R != A)
        baz_set_ratfrac (R, A);
    }
  else
    {
      bap_pow_polynom_mpz (&R->numer, &A->numer, d > 0 ? d : -d);
      bap_pow_polynom_mpz (&R->denom, &A->denom, d > 0 ? d : -d);
      if (d < 0)
        baz_invert_ratfrac (R, R);
    }

}

/*
 * texinfo: baz_separant_ratfrac
 * Assign the separant of @var{A} (i.e. its derivative w.r.t. to
 * its leader) to @var{R}.
 */

BAZ_DLL void
baz_separant_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A)
{
  struct bap_polynom_mpz sep_num_A;
  struct bap_polynom_mpz sep_den_A;
  bav_variable u;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  u = baz_leader_ratfrac (A);

  if (bap_is_numeric_polynom_mpz (&A->numer) ||
      bap_leader_polynom_mpz (&A->numer) != u)
    {
      bap_init_polynom_mpz (&sep_den_A);
      bap_separant_polynom_mpz (&sep_den_A, &A->denom);
      bap_mul_polynom_mpz (&sep_den_A, &sep_den_A, &A->numer);
      ba0_pull_stack ();
      bap_neg_polynom_mpz (&R->numer, &sep_den_A);
      bap_pow_polynom_mpz (&R->denom, &A->denom, 2);
    }
  else if (bap_is_numeric_polynom_mpz (&A->denom) ||
      bap_leader_polynom_mpz (&A->denom) != u)
    {
      ba0_pull_stack ();
      bap_separant_polynom_mpz (&R->numer, &A->numer);
      if (A != R)
        bap_set_polynom_mpz (&R->denom, &A->denom);
    }
  else
    {
      bap_init_polynom_mpz (&sep_num_A);
      bap_init_polynom_mpz (&sep_den_A);
      bap_separant_polynom_mpz (&sep_num_A, &A->numer);
      bap_separant_polynom_mpz (&sep_den_A, &A->denom);
      bap_mul_polynom_mpz (&sep_num_A, &sep_num_A, &A->denom);
      bap_mul_polynom_mpz (&sep_den_A, &sep_den_A, &A->numer);

      ba0_pull_stack ();

      bap_sub_polynom_mpz (&R->numer, &sep_num_A, &sep_den_A);
      bap_pow_polynom_mpz (&R->denom, &A->denom, 2);
    }
  ba0_restore (&M);
  baz_reduce_ratfrac (R, R);
}

/*
 * texinfo: baz_separant2_ratfrac
 * Assign @math{\partial A / \partial v} to @math{R}.
 */

BAZ_DLL void
baz_separant2_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    bav_variable v)
{
  struct baz_ratfrac B;
  bav_Iordering r;
  struct ba0_mark M;

  if (!baz_depend_ratfrac (A, v))
    baz_set_ratfrac_zero (R);
  else if (baz_leader_ratfrac (A) == v)
    baz_separant_ratfrac (R, A);
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);
      r = bav_R_copy_ordering (bav_R_Iordering ());
      bav_R_push_ordering (r);
      bav_R_set_maximal_variable (v);
      baz_init_readonly_ratfrac (&B);
      baz_sort_ratfrac (&B, A);
      ba0_pull_stack ();
      baz_separant_ratfrac (R, &B);
      bav_R_pull_ordering ();
      baz_physort_ratfrac (R);
      bav_R_free_ordering (r);
      ba0_restore (&M);
    }
}

/*
 * texinfo: baz_diff_ratfrac
 * Assign to @var{R} the rational fraction obtained by differentiating 
 * @var{A} w.r.t. @var{s}. 
 * Every variable which is a derivative of any element of @var{nulles}
 * is considered to be @math{0}.
 */

BAZ_DLL void
baz_diff_ratfrac (
    baz_ratfrac R,
    baz_ratfrac A,
    bav_symbol s,
    bav_tableof_variable nulles)
{
  struct bap_polynom_mpz B;
  struct bap_polynom_mpz C;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_polynom_mpz (&B);
  bap_init_polynom_mpz (&C);

  bap_diff_polynom_mpz (&B, &A->numer, s, nulles);
  bap_diff_polynom_mpz (&C, &A->denom, s, nulles);

  bap_mul_polynom_mpz (&B, &B, &A->denom);
  bap_mul_polynom_mpz (&C, &C, &A->numer);

  ba0_pull_stack ();

  bap_sub_polynom_mpz (&R->numer, &B, &C);
  if (bap_is_zero_polynom_mpz (&R->numer))
    baz_set_ratfrac_zero (R);
  else
    bap_pow_polynom_mpz (&R->denom, &A->denom, 2);

  ba0_restore (&M);
}

/*
 * texinfo: baz_is_constant_ratfrac
 * Return @code{true} if the derivative of @var{A} w.r.t. @var{s} is zero.
 * Zero derivatives of elements of @var{P} are taken into account.
 */

BAZ_DLL bool
baz_is_constant_ratfrac (
    baz_ratfrac A,
    bav_symbol s,
    bav_tableof_parameter P)
{
  return bap_is_constant_polynom_mpz (&A->numer, s, P) &&
      bap_is_constant_polynom_mpz (&A->denom, s, P);
}

/*
 * texinfo: baz_is_independent_ratfrac
 * Return @code{true} if @var{A} only depends on independent variables and 
 * on constants.
 */

BAZ_DLL bool
baz_is_independent_ratfrac (
    baz_ratfrac A,
    bav_tableof_parameter P)
{
  return bap_is_independent_polynom_mpz (&A->numer, P) &&
      bap_is_independent_polynom_mpz (&A->denom, P);
}
