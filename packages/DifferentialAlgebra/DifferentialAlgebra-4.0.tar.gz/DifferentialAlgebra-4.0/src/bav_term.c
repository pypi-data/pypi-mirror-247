#include "bav_differential_ring.h"
#include "bav_term.h"
#include "bav_term_ordering.h"
#include "bav_global.h"
#include "bav_parameter.h"

/*
 * texinfo: bav_init_term
 * Initialize @var{T} to the term @math{1}.
 */

BAV_DLL void
bav_init_term (
    bav_term T)
{
  T->alloc = 0;
  T->size = 0;
  T->rg = (struct bav_rank *) 0;
}

/*
 * texinfo: bav_new_term
 * Allocate a new term, initialize it and return it.
 */

BAV_DLL bav_term
bav_new_term (
    void)
{
  bav_term T = (bav_term) ba0_alloc (sizeof (struct bav_term));
  bav_init_term (T);
  return T;
}

/*
 * texinfo: bav_realloc_term
 * Realloc the field @code{rg} if needed so that it can receive at least
 * @var{n} ranks. The existing ranks are kept.
 */

BAV_DLL void
bav_realloc_term (
    bav_term T,
    ba0_int_p n)
{
  struct bav_rank *tab;

  if (T->alloc < n)
    {
      tab = (struct bav_rank *) ba0_alloc (sizeof (struct bav_rank) * n);
      memcpy (tab, T->rg, T->size * sizeof (struct bav_rank));
      T->rg = tab;
      T->alloc = n;
    }
}

/*
 * texinfo: bav_switch_ring_term
 * Replace each variable occuring in @var{T} by the one obtained by
 * applying @code{bav_switch_ring_variable} over it. See this function.
 * The term @var{T} is modified.
 * This low level function should be used in conjunction with 
 * @code{bav_set_differential_ring}.
 */

BAV_DLL void
bav_switch_ring_term (
    bav_term T,
    bav_differential_ring R)
{
  ba0_int_p i;

  for (i = 0; i < T->size; i++)
    T->rg[i].var = bav_switch_ring_variable (T->rg[i].var, R);
}

/*
 * texinfo: bav_set_term_one
 * Assign the term @math{1} to @var{T}.
 */

BAV_DLL void
bav_set_term_one (
    bav_term T)
{
  T->size = 0;
}

/* 
 * texinfo: bav_set_term_rank
 * Assign @var{rg} to @var{T}.
 * If @var{rg} is the rank of nonzero constant then assigm the term
 * @math{1} to @var{T}.
 * Exception @code{BAV_ERRRGZ} is raised if @var{rg} is the rank of zero.
 */

BAV_DLL void
bav_set_term_rank (
    bav_term T,
    bav_rank rg)
{
  if (bav_is_zero_rank (rg))
    BA0_RAISE_EXCEPTION (BAV_ERRRGZ);
  if (bav_is_constant_rank (rg))
    bav_set_term_one (T);
  else
    {
      bav_realloc_term (T, 1);
      T->rg[0] = *rg;
      T->size = 1;
    }
}

/*
 * texinfo: bav_set_term_variable
 * Assign @math{v^d} to @var{T}.
 * If @var{d} is zero then assign the term @math{1} to @var{T}.
 */

BAV_DLL void
bav_set_term_variable (
    bav_term T,
    bav_variable v,
    bav_Idegree d)
{
  if (d == 0)
    bav_set_term_one (T);
  else
    {
      bav_realloc_term (T, 1);
      T->rg[0].var = v;
      T->rg[0].deg = d;
      T->size = 1;
    }
}

/*
 * texinfo: bav_set_term
 * Assign @var{U} to @var{T}.
 */

BAV_DLL void
bav_set_term (
    bav_term T,
    bav_term U)
{
  if (T != U)
    {
      bav_realloc_term (T, U->size);
      memcpy (T->rg, U->rg, U->size * sizeof (struct bav_rank));
      T->size = U->size;
    }
}

/*
 * texinfo: bav_shift_term
 * Assign to @var{T} the term obtained by removing the leading rank of @var{U}.
 * May raise exception @code{BAV_ERRTEU} (unexpected term one).
 */

BAV_DLL void
bav_shift_term (
    bav_term T,
    bav_term U)
{
  if (bav_is_one_term (U))
    BA0_RAISE_EXCEPTION (BAV_ERRTEU);
  bav_realloc_term (T, U->size - 1);
  memmove (T->rg, U->rg + 1, (U->size - 1) * sizeof (struct bav_rank));
  T->size = U->size - 1;
}

/*
 * texinfo: bav_strip_term
 * Assign to @var{T} the term obtained by removing from @var{U}
 * all the variables with numbers strictly less than @var{n}.
 */

BAV_DLL void
bav_strip_term (
    bav_term T,
    bav_term U,
    bav_Inumber n)
{
  ba0_int_p i;

  i = 0;
  while (i < U->size && bav_R_variable_number (U->rg[i].var) >= n)
    i++;
  if (T == U)
    U->size = i;
  else
    {
      bav_realloc_term (T, i);
      T->size = i;
      memcpy (T->rg, U->rg, T->size * sizeof (struct bav_rank));
    }
}

/*
 * texinfo: bav_is_one_term
 * Return @code{true} if @var{T} is the term @math{1}.
 */

BAV_DLL bool
bav_is_one_term (
    bav_term T)
{
  return T->size == 0;
}

/*
 * texinfo: bav_leader_term
 * Return the leading variable of @var{T}.
 * May raise exception @code{BAV_ERRTEU} (unexpected term one).
 */

BAV_DLL bav_variable
bav_leader_term (
    bav_term T)
{
  if (bav_is_one_term (T))
    BA0_RAISE_EXCEPTION (BAV_ERRTEU);
  return T->rg[0].var;
}

/*
 * texinfo: bav_leading_degree_term
 * Return the degree of the leading rank.
 * May raise exception @code{BAV_ERRTEU} (unexpected term one).
 */

BAV_DLL bav_Idegree
bav_leading_degree_term (
    bav_term T)
{
  if (bav_is_one_term (T))
    BA0_RAISE_EXCEPTION (BAV_ERRTEU);
  return T->rg[0].deg;
}

/*
 * texinfo: bav_total_degree_term
 * Return the total degree of the term: the sum of the degrees of all ranks.
 */

BAV_DLL bav_Idegree
bav_total_degree_term (
    bav_term T)
{
  ba0_int_p i;
  bav_Idegree deg;

  for (i = 0, deg = 0; i < T->size; i++)
    deg += T->rg[i].deg;
  return deg;
}

/*
 * texinfo: bav_maximal_degree_term
 * Return the maximum of the degrees of all ranks.
 */

BAV_DLL bav_Idegree
bav_maximal_degree_term (
    bav_term T)
{
  ba0_int_p i;
  bav_Idegree deg;

  for (i = 0, deg = 0; i < T->size; i++)
    if (deg < T->rg[i].deg)
      deg = T->rg[i].deg;
  return deg;
}

/*
 * texinfo: bav_degree_term
 * Return the degree of @var{T} w.r.t. @var{v}.
 */

BAV_DLL bav_Idegree
bav_degree_term (
    bav_term T,
    bav_variable v)
{
  ba0_int_p i;

  i = 0;
  while (i < T->size && T->rg[i].var != v)
    i++;
  return i < T->size ? T->rg[i].deg : 0;
}

/*
 * texinfo: bav_total_order_term
 * Return the maximum of the orders of the variables of @var{T}.
 */

BAV_DLL bav_Iorder
bav_total_order_term (
    bav_term T)
{
  ba0_int_p i;
  bav_Iorder ord, ordmax;

  ordmax = 0;
  for (i = 0; i < T->size; i++)
    {
      if (T->rg[i].var->root->type != bav_independent_symbol)
        {
          ord = bav_total_order_variable (T->rg[i].var);
          if (ord > ordmax)
            ordmax = ord;
        }
    }
  return ordmax;
}

/*
 * texinfo: bav_leading_rank_term
 * Return the leading rank of @var{T}.
 */

BAV_DLL struct bav_rank
bav_leading_rank_term (
    bav_term T)
{
  if (bav_is_one_term (T))
    return bav_constant_rank ();
  else
    return T->rg[0];
}

/*
 * texinfo: bav_equal_term
 * Return @code{true} if @var{T} and @var{U} are equal.
 */

BAV_DLL bool
bav_equal_term (
    bav_term T,
    bav_term U)
{
  if (T->size != U->size)
    return false;
  if (T == U)
    return true;
  return memcmp (T->rg, U->rg, T->size * sizeof (struct bav_rank)) == 0;
}

/*
 * texinfo: bav_gt_term
 * Return @code{true} if @math{T > U} w.r.t. the lexicographic
 * order induced by the current ordering.
 */

BAV_DLL bool
bav_gt_term (
    bav_term T,
    bav_term U)
{
  bav_Inumber nt, nu;
  ba0_int_p i;

  i = 0;
  while (i < T->size && i < U->size)
    {
      nt = bav_R_variable_number (T->rg[i].var);
      nu = bav_R_variable_number (U->rg[i].var);
      if (nt > nu)
        return true;
      else if (nt < nu)
        return false;
      else if (T->rg[i].deg > U->rg[i].deg)
        return true;
      else if (T->rg[i].deg < U->rg[i].deg)
        return false;
      i += 1;
    }
  return T->size > U->size;
}

/*
 * texinfo: bav_lt_term
 * Return @code{true} if @math{T < U} w.r.t. the lexicographic
 * order induced by the current ordering.
 */

BAV_DLL bool
bav_lt_term (
    bav_term T,
    bav_term U)
{
  bav_Inumber nt, nu;
  ba0_int_p i;

  i = 0;
  while (i < T->size && i < U->size)
    {
      nt = bav_R_variable_number (T->rg[i].var);
      nu = bav_R_variable_number (U->rg[i].var);
      if (nt < nu)
        return true;
      else if (nt > nu)
        return false;
      else if (T->rg[i].deg < U->rg[i].deg)
        return true;
      else if (T->rg[i].deg > U->rg[i].deg)
        return false;
      i += 1;
    }
  return T->size < U->size;
}

/*
 * texinfo: bav_disjoint_term
 * Return @code{true} if @var{T} and @var{U} have no variable in common
 * i.e. if their lcm is equal to their product.
 */

BAV_DLL bool
bav_disjoint_term (
    bav_term T,
    bav_term U)
{
  ba0_int_p i, j;

  for (i = 0; i < T->size; i++)
    for (j = 0; j < U->size; j++)
      if (T->rg[i].var == U->rg[j].var)
        return false;
  return true;
}

/*
 * texinfo: bav_sort_term
 * Sort @var{T} in place in decreasing order w.r.t. the current ordering
 * (useful in the case of a change of current ordering).
 */

BAV_DLL void
bav_sort_term (
    bav_term T)
{
  qsort (T->rg, T->size, sizeof (struct bav_rank), &bav_inv_comp_rank);
}

/*
 * texinfo: bav_lcm_term
 * Assign to @var{R} the least common multiple of @var{T} and @var{U}.
 */

BAV_DLL void
bav_lcm_term (
    bav_term R,
    bav_term T,
    bav_term U)
{
  struct bav_term S;
  ba0_int_p t, u, s;
  bav_Inumber num_t, num_u;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  bav_init_term (&S);
  bav_realloc_term (&S, T->size + U->size);

  t = u = s = 0;
  while (t < T->size && u < U->size)
    {
      if (T->rg[t].var == U->rg[u].var)
        {
          S.rg[s].var = T->rg[t].var;
          S.rg[s].deg = BA0_MAX (T->rg[t].deg, U->rg[u].deg);
          t++;
          u++;
          s++;
        }
      else
        {
          num_t = bav_R_variable_number (T->rg[t].var);
          num_u = bav_R_variable_number (U->rg[u].var);
          S.rg[s++] = num_t > num_u ? T->rg[t++] : U->rg[u++];
        }
    }
  while (t < T->size)
    S.rg[s++] = T->rg[t++];
  while (u < U->size)
    S.rg[s++] = U->rg[u++];
  S.size = s;
  ba0_pull_stack ();
  bav_set_term (R, &S);
  ba0_restore (&M);
}

/*
 * texinfo: bav_gcd_term
 * Assign to @var{R} the greatest common divisor of @var{T} and @var{U}.
 */

BAV_DLL void
bav_gcd_term (
    bav_term R,
    bav_term T,
    bav_term U)
{
  struct bav_term S;
  ba0_int_p t, u, s;
  bav_Inumber num_t, num_u;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  bav_init_term (&S);
  bav_realloc_term (&S, BA0_MAX (T->size, U->size));

  t = u = s = 0;
  while (t < T->size && u < U->size)
    {
      if (T->rg[t].var == U->rg[u].var)
        {
          S.rg[s].var = T->rg[t].var;
          S.rg[s].deg = BA0_MIN (T->rg[t].deg, U->rg[u].deg);
          t++;
          u++;
          s++;
        }
      else
        {
          num_t = bav_R_variable_number (T->rg[t].var);
          num_u = bav_R_variable_number (U->rg[u].var);
          if (num_t > num_u)
            t++;
          else
            u++;
        }
    }
  S.size = s;
  ba0_pull_stack ();
  bav_set_term (R, &S);
  ba0_restore (&M);
}

/*
 * texinfo: bav_mul_term
 * Assign to @var{R} the product of @var{T} and @var{U}.
 */

BAV_DLL void
bav_mul_term (
    bav_term R,
    bav_term T,
    bav_term U)
{
  struct bav_term S;
  ba0_int_p t, u, s;
  bav_Inumber num_t, num_u;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  bav_init_term (&S);
  bav_realloc_term (&S, T->size + U->size);

  t = u = s = 0;
  while (t < T->size && u < U->size)
    {
      if (T->rg[t].var == U->rg[u].var)
        {
          S.rg[s].var = T->rg[t].var;
          S.rg[s].deg = T->rg[t].deg + U->rg[u].deg;
          t++;
          u++;
          s++;
        }
      else
        {
          num_t = bav_R_variable_number (T->rg[t].var);
          num_u = bav_R_variable_number (U->rg[u].var);
          S.rg[s++] = num_t > num_u ? T->rg[t++] : U->rg[u++];
        }
    }
  while (t < T->size)
    S.rg[s++] = T->rg[t++];
  while (u < U->size)
    S.rg[s++] = U->rg[u++];
  S.size = s;
  ba0_pull_stack ();
  bav_set_term (R, &S);
  ba0_restore (&M);
}

/*
 * texinfo: bav_mul_term_rank
 * Assign to @var{R} the product of @var{T} by @var{rg}.
 * Exception @code{BAV_ERRRGZ} is raised if @var{rg} is the rank of zero.
 */

BAV_DLL void
bav_mul_term_rank (
    bav_term R,
    bav_term T,
    bav_rank rg)
{
  struct bav_term S;
  ba0_int_p t, s;
  bav_Inumber num;
  struct ba0_mark M;

  if (bav_is_zero_rank (rg))
    BA0_RAISE_EXCEPTION (BAV_ERRRGZ);
  if (bav_is_constant_rank (rg))
    bav_set_term (R, T);
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);
      bav_init_term (&S);
      bav_realloc_term (&S, T->size + 1);
      num = bav_R_variable_number (rg->var);
      t = s = 0;
      while (t < T->size && bav_R_variable_number (T->rg[t].var) > num)
        S.rg[s++] = T->rg[t++];
      if (t < T->size && T->rg[t].var == rg->var)
        {
          S.rg[s].var = rg->var;
          S.rg[s].deg = T->rg[t].deg + rg->deg;
          t++;
        }
      else
        S.rg[s] = *rg;
      s++;
      while (t < T->size)
        S.rg[s++] = T->rg[t++];
      S.size = s;
      ba0_pull_stack ();
      bav_set_term (R, &S);
      ba0_restore (&M);
    }
}

/*
 * texinfo: bav_mul_term_variable
 * Assign to @var{T} the product of @math{U} by @math{v^d}.
 * If @var{d} is zero then assign @var{U} to @var{T}.
 */

BAV_DLL void
bav_mul_term_variable (
    bav_term T,
    bav_term U,
    bav_variable v,
    bav_Idegree d)
{
  struct bav_rank rg;

  rg.var = v;
  rg.deg = d;
  bav_mul_term_rank (T, U, &rg);
}

/*
 * texinfo: bav_pow_term
 * Assign to @var{T} the term @math{U^d}.
 * If @var{d} is zero then assign the term @math{1} to @var{T}.
 */

BAV_DLL void
bav_pow_term (
    bav_term T,
    bav_term U,
    bav_Idegree d)
{
  ba0_int_p i;

  if (d == 0)
    bav_set_term_one (T);
  else
    {
      bav_realloc_term (T, U->size);
      for (i = 0; i < U->size; i++)
        {
          T->rg[i].var = U->rg[i].var;
          T->rg[i].deg = U->rg[i].deg * d;
        }
      T->size = U->size;
    }
}

/*
 * texinfo: bav_is_factor_term
 * Return @code{true} if @var{U} is a factor of @var{T}.
 * If so and @var{R} is a nonzero pointer then assign @math{T/U} to @var{R}.
 */

BAV_DLL bool
bav_is_factor_term (
    bav_term T,
    bav_term U,
    bav_term R)
{
  struct bav_term S;
  ba0_int_p t, u, s;
  bool divisible;
  struct ba0_mark M;

  if (R != (bav_term) 0)
    {
      ba0_push_another_stack ();
      ba0_record (&M);
      bav_init_term (&S);
      bav_realloc_term (&S, T->size);
    }
  divisible = true;
  t = u = s = 0;
  while (divisible && u < U->size)
    {
      if (t == T->size)
        divisible = false;
      else if (T->rg[t].var == U->rg[u].var)
        {
          if (T->rg[t].deg < U->rg[u].deg)
            divisible = false;
          else if (T->rg[t].deg > U->rg[u].deg && R != (bav_term) 0)
            {
              S.rg[s].var = T->rg[t].var;
              S.rg[s].deg = T->rg[t].deg - U->rg[u].deg;
              s++;
            }
          t++;
          u++;
        }
      else if (bav_R_variable_number (T->rg[t].var) <
          bav_R_variable_number (U->rg[u].var))
        divisible = false;
      else if (R != (bav_term) 0)
        S.rg[s++] = T->rg[t++];
      else
        t++;
    }
  if (R != (bav_term) 0)
    {
      if (divisible)
        {
          while (t < T->size)
            S.rg[s++] = T->rg[t++];
          S.size = s;
          ba0_pull_stack ();
          bav_set_term (R, &S);
          ba0_restore (&M);
        }
      else
        {
          ba0_pull_stack ();
          ba0_restore (&M);
        }
    }
  return divisible;
}

/*
 * texinfo: bav_exquo_term
 * Assign @math{T/U} to @var{R}.
 * Raise the exception @code{BAV_EXEXQO} if @var{U} is not a factor of @var{T}.
 */

BAV_DLL void
bav_exquo_term (
    bav_term R,
    bav_term T,
    bav_term U)
{
  if (!bav_is_factor_term (T, U, R))
    BA0_RAISE_EXCEPTION (BAV_EXEXQO);
}

/*
 * texinfo: bav_exquo_term_variable
 * Assign @math{T/x^d} to @var{R}.
 * Raise the exception @code{BAV_EXEXQO} 
 * if @math{x^d} is not a factor of @var{T}.
 */

BAV_DLL void
bav_exquo_term_variable (
    bav_term R,
    bav_term T,
    bav_variable x,
    bav_Idegree d)
{
  ba0_int_p i;

  if (d == 0)
    {
      if (R != T)
        bav_set_term (R, T);
      return;
    }

  i = 0;
  while (i < T->size && T->rg[i].var != x)
    i++;
  if (i == T->size || T->rg[i].deg < d)
    BA0_RAISE_EXCEPTION (BAV_EXEXQO);
  if (R == T)
    {
      if (R->rg[i].deg > d)
        R->rg[i].deg -= d;
      else
        {
          memmove (R->rg + i, T->rg + i + 1,
              (T->size - i - 1) * sizeof (struct bav_rank));
          R->size--;
        }
    }
  else
    {
      bav_set_term_one (R);
      bav_realloc_term (R, T->rg[i].deg > d ? T->size : T->size - 1);
      memcpy (R->rg, T->rg, i * sizeof (struct bav_rank));
      if (T->rg[i].deg > d)
        {
          R->rg[i].var = T->rg[i].var;
          R->rg[i].deg = T->rg[i].deg - d;
          memcpy (R->rg + i + 1, T->rg + i + 1,
              (T->size - i - 1) * sizeof (struct bav_rank));
          R->size = T->size;
        }
      else
        {
          memcpy (R->rg + i, T->rg + i + 1,
              (T->size - i - 1) * sizeof (struct bav_rank));
          R->size = T->size - 1;
        }
    }
}

/*
 * texinfo: bav_diff_term
 * Assign to @var{R} a multiple of all the terms of the differential
 * polynomial obtained by differentiating @var{T} w.r.t. the independent
 * variable @var{x}. Derivatives of elements of @var{nulles} are omitted.
 */

BAV_DLL void
bav_diff_term (
    bav_term R,
    bav_term T,
    bav_symbol x,
    bav_tableof_variable nulles)
{
  bav_variable v;
  enum bav_typeof_symbol type;
  ba0_int_p t;

  if (T->size == 0)
    bav_set_term_one (R);
  else if (T->size == 1 && T->rg[0].deg == 1)
    {
      type = T->rg[0].var->root->type;
      if (type == bav_dependent_symbol || type == bav_operator_symbol)
        {
          v = bav_diff_variable (T->rg[0].var, x);
          if (bav_is_derivative2 (v, nulles))
            bav_set_term_one (R);
          else
            bav_set_term_variable (R, v, 1);
        }
      else
        bav_set_term_one (R);
    }
  else
    {
      for (t = 0; t < T->size; t++)
        {
          v = T->rg[t].var;
          type = T->rg[t].var->root->type;
          if (type == bav_dependent_symbol || type == bav_operator_symbol)
            bav_diff_variable (T->rg[t].var, x);
        }
      bav_R_mark_variables (0);
      for (t = 0; t < T->size; t++)
        T->rg[t].var->hack = T->rg[t].deg;
      for (t = 0; t < T->size; t++)
        {
          v = T->rg[t].var;
          type = T->rg[t].var->root->type;
          if (type == bav_dependent_symbol || type == bav_operator_symbol)
            {
              v = bav_diff_variable (v, x);
              if (!bav_is_derivative2 (v, nulles))
                v->hack += 1;
            }
        }
      bav_marked_ranks_term (R);
      bav_sort_term (R);
    }
}

/*
 * texinfo: bav_marked_ranks_term
 * Run over the set of all the variables.
 * Interpret their @code{hack} fields as degrees.
 * Assigns to @var{T} the product of all the so defined ranks.
 */

BAV_DLL void
bav_marked_ranks_term (
    bav_term T)
{
  ba0_int_p i, n;
  bav_variable v;

  for (i = 0, n = 0; i < bav_global.R.vars.size; i++)
    {
      v = bav_global.R.vars.tab[i];
      if (v->hack != 0)
        n++;
    }
  bav_realloc_term (T, n);
  for (i = 0, n = 0; i < bav_global.R.vars.size; i++)
    {
      v = bav_global.R.vars.tab[i];
      if (v->hack != 0)
        {
          T->rg[n].var = v;
          T->rg[n].deg = v->hack;
          n++;
        }
    }
  T->size = n;
}

/*
 * Readonly static data
 */

static char _struct_term[] = "struct bav_term";
static char _struct_term_rg[] = "bav_term->rg";

BAV_DLL ba0_int_p
bav_garbage1_term (
    void *U,
    enum ba0_garbage_code code)
{
  bav_term T = (bav_term) U;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (T, sizeof (struct bav_term), _struct_term);
  n += ba0_new_gc_info
      (T->rg, sizeof (struct bav_rank) * T->alloc, _struct_term_rg);
  return n;
}

BAV_DLL void *
bav_garbage2_term (
    void *U,
    enum ba0_garbage_code code)
{
  bav_term T;

  if (code == ba0_isolated)
    T = (bav_term) ba0_new_addr_gc_info (U, _struct_term);
  else
    T = (bav_term) U;

  T->rg = (struct bav_rank *) ba0_new_addr_gc_info (T->rg, _struct_term_rg);
  return T;
}

BAV_DLL void *
bav_copy_term (
    void *U)
{
  bav_term T = (bav_term) U;
  bav_term V;

  V = bav_new_term ();
  bav_set_term (V, T);
  return V;
}

/*
 * texinfo: bav_scanf_term
 * The parsing function for terms.
 * It is called by @code{ba0_scanf/%term}.
 * It may raise exception @code{BAV_ERRTER}.
 */

BAV_DLL void *
bav_scanf_term (
    void *U)
{
  bav_term R = (bav_term) U;
  struct bav_term T;
  struct bav_rank rg;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  bav_init_term (&T);
  bav_realloc_term (&T, 20);    /* optimisation heuristique */

  if (ba0_type_token_analex () == ba0_integer_token)
    {
      if (strcmp (ba0_value_token_analex (), "1") != 0)
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRTER);
    }
  else
    {
      for (;;)
        {
          bav_scanf_variable (&rg.var);
          ba0_get_token_analex ();
          if (ba0_sign_token_analex ("^"))
            {
              ba0_get_token_analex ();
              if (ba0_type_token_analex () != ba0_integer_token)
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRTER);
              rg.deg = (bav_Idegree) atoi (ba0_value_token_analex ());
              if (rg.deg <= 0)
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRTER);
            }
          else if (ba0_sign_token_analex ("*"))
            {
              ba0_get_token_analex ();
              if (ba0_sign_token_analex ("*"))
                {
                  ba0_get_token_analex ();
                  if (ba0_type_token_analex () != ba0_integer_token)
                    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRTER);
                  rg.deg = (bav_Idegree) atoi (ba0_value_token_analex ());
                  if (rg.deg <= 0)
                    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRTER);
                }
              else
                {
                  ba0_unget_token_analex (2);
                  rg.deg = 1;
                }
            }
          else
            {
              ba0_unget_token_analex (1);
              rg.deg = 1;
            }
          bav_mul_term_rank (&T, &T, &rg);
          ba0_get_token_analex ();
          if (!ba0_sign_token_analex ("*"))
            break;
          ba0_get_token_analex ();
        }
      ba0_unget_token_analex (1);
    }
  ba0_pull_stack ();
  if (R == (bav_term) 0)
    R = bav_new_term ();
  bav_set_term (R, &T);
  ba0_restore (&M);
  return R;
}

/*
 * texinfo: bav_printf_term
 * The printing function for terms.
 * It is called by @code{ba0_printf/%term}.
 */

BAV_DLL void
bav_printf_term (
    void *U)
{
  bav_term T = (bav_term) U;
  bool first = true;
  ba0_int_p i;

  if (T->size == 0)
    ba0_put_char ('1');

  for (i = 0; i < T->size; i++)
    {
      if (!first && !ba0_global.common.LaTeX)
        ba0_put_char ('*');
      else
        first = false;
      ba0_printf ("%rank", &T->rg[i]);
    }
}

/*
 * Assigns T mod point to value
 */

/*
 * texinfo: bav_term_at_point_int_p
 * Assign @var{T} mod @var{point} to @var{value}.
 * Raises the exception @code{BA0_ERRALG} if all variables do not get evaluated.
 */

BAV_DLL void
bav_term_at_point_int_p (
    ba0_mpz_t res,
    bav_term T,
    bav_point_int_p point)
{
  bav_value_int_p value;
  ba0_int_p t;
  bool zero;
  ba0_mpz_t val, pow;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_mpz_init (pow);
  ba0_mpz_init_set_ui (val, 1);
  zero = false;
  for (t = 0; !zero && t < T->size; t++)
    {
      value = (bav_value_int_p) ba0_bsearch_point
          (T->rg[t].var, (ba0_point) point, (ba0_int_p *) 0);

      if ((ba0_value) value == BA0_NOT_A_VALUE)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);

      zero = value->value == 0;
      ba0_mpz_set_si (pow, value->value);
      ba0_mpz_pow_ui (pow, pow, T->rg[t].deg);
      ba0_mpz_mul (val, val, pow);
    }
  ba0_pull_stack ();
  ba0_mpz_set (res, val);
  ba0_restore (&M);
}

/*
 * texinfo: bav_term_at_point_interval_mpq
 * Assign @var{T} mod @var{point} to @var{res}.
 * Exception @code{BA0_ERRALG} is raised if all variables do not get
 * evaluated.
 */

BAV_DLL void
bav_term_at_point_interval_mpq (
    ba0_interval_mpq res,
    bav_term T,
    bav_point_interval_mpq point)
{
  bav_value_interval_mpq value;
  struct ba0_interval_mpq pow;
  struct ba0_mark M;
  ba0_int_p i;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_interval_mpq (&pow);
  ba0_pull_stack ();

  ba0_set_interval_mpq_si (res, 1);
  for (i = 0; !ba0_is_zero_interval_mpq (res) && i < T->size; i++)
    {
      value = (bav_value_interval_mpq) ba0_bsearch_point
          (T->rg[i].var, (ba0_point) point, (ba0_int_p *) 0);

      if ((ba0_value) value == BA0_NOT_A_VALUE)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);

      ba0_push_another_stack ();
      ba0_pow_interval_mpq (&pow, value->value, (ba0_int_p) T->rg[i].deg);
      ba0_pull_stack ();
      ba0_mul_interval_mpq (res, res, &pow);
    }
  ba0_restore (&M);
}

/*
 * texinfo: bav_depends_on_zero_derivatives_of_parameter_term
 * Return @code{true} if @var{T} depends on a derivative of an element 
 * of @var{P} which turns out to be zero.
 */

BAV_DLL bool
bav_depends_on_zero_derivatives_of_parameter_term (
    bav_term T,
    bav_tableof_parameter P)
{
  ba0_int_p i;
  for (i = 0; i < T->size; i++)
    if (bav_is_zero_derivative_of_parameter (T->rg[i].var, P))
      return true;
  return false;
}
