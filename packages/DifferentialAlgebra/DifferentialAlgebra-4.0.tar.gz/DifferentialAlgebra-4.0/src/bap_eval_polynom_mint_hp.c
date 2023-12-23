#include "bap_polynom_mint_hp.h"
#include "bap_creator_mint_hp.h"
#include "bap_itermon_mint_hp.h"
#include "bap_itercoeff_mint_hp.h"
#include "bap_add_polynom_mint_hp.h"
#include "bap_mul_polynom_mint_hp.h"
#include "bap_eval_polynom_mint_hp.h"
#include "bap_geobucket_mint_hp.h"
#include "bap__check_mint_hp.h"

#define BAD_FLAG_mint_hp
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpzm) || defined (BAD_FLAG_mpq)

/*
 * Sets to point an evaluation point the variables of which being
 * that of A and the values of which being zero.
 * Variables appear by decreasing order.
 */

/*
 * texinfo: bap_set_point_polynom_mint_hp
 * Assign to @var{point} an evaluation point the variables of which being
 * that of @var{A} and the values of which being zero.
 * Variables appear by decreasing order.
 */

BAP_DLL void
bap_set_point_polynom_mint_hp (
    ba0_point point,
    bap_polynom_mint_hp A,
    bool withld)
{
  ba0_int_p i;

  point->size = 0;
  ba0_realloc2_table ((ba0_table) point, A->total_rank.size,
      (ba0_new_function *) & ba0_new_value);
  for (i = withld ? 0 : 1; i < A->total_rank.size; i++)
    {
      point->tab[point->size]->var = A->total_rank.rg[i].var;
      point->tab[point->size]->value = 0;
      point->size += 1;
    }
  ba0_sort_point ((ba0_point) point, (ba0_point) point);
}

/*
 * Sets R to the polynomial obtained by evaluating A at v = c.
 */

/*
 * texinfo: bap_eval_polynom_numeric_mint_hp
 * Assign to @var{R} the polynomial obtained by evaluating @var{A} at @math{v=c}.
 */

BAP_DLL void
bap_eval_polynom_numeric_mint_hp (
    bap_polynom_mint_hp R,
    bap_polynom_mint_hp A,
    bav_variable v,
    ba0_mint_hp_t c)
{
  struct bap_polynom_mint_hp B, C, E;
  struct bap_itercoeff_mint_hp iter;
  struct bav_term T;
  bav_Idegree d;
  bav_Iordering r;
  struct ba0_mark M;

  bap__check_ordering_mint_hp (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);
  bav_R_set_maximal_variable (v);

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&T);

  bap_init_polynom_mint_hp (&B);
  bap_init_polynom_mint_hp (&C);
  bap_init_polynom_mint_hp (&E);
  bap_sort_polynom_mint_hp (&B, A);

  if (!bap_is_numeric_polynom_mint_hp (&B) && bap_leader_polynom_mint_hp (&B) == v)
    {
      bap_begin_itercoeff_mint_hp (&iter, &B, v);
      bap_coeff_itercoeff_mint_hp (&C, &iter);
      bap_term_itercoeff_mint_hp (&T, &iter);
      bap_set_polynom_mint_hp (&E, &C);
/*
   Horner scheme
*/
      for (d = bav_degree_term (&T, v) - 1; d >= 0; d--)
        {
          bap_mul_polynom_numeric_mint_hp (&E, &E, c);
          bav_set_term_variable (&T, v, d);
          bap_seek_coeff_itercoeff_mint_hp (&C, &iter, &T);
          if (!bap_is_zero_polynom_mint_hp (&C))
            bap_add_polynom_mint_hp (&E, &E, &C);
        }
      bap_close_itercoeff_mint_hp (&iter);
      ba0_pull_stack ();
      bap_set_polynom_mint_hp (R, &E);
    }
  else
    {
      ba0_pull_stack ();
      if (R != A)
        bap_set_polynom_mint_hp (R, A);
    }
  ba0_restore (&M);
  bav_R_pull_ordering ();
  bav_R_free_ordering (r);
  bap_physort_polynom_mint_hp (R);
}

/*
 * texinfo: bap_eval_polynom_polynom_mint_hp
 * Assign to @var{R} the polynomial obtained by evaluating @var{A} at @math{v=value}.
 */

BAP_DLL void
bap_eval_polynom_polynom_mint_hp (
    bap_polynom_mint_hp R,
    bap_polynom_mint_hp A,
    bav_variable v,
    bap_polynom_mint_hp val)
{
  struct bap_polynom_mint_hp G, B, coeff, value;
  struct bap_itercoeff_mint_hp iter;
  struct bav_term T;
  bav_Idegree d;
  bav_Iordering r;
  struct ba0_mark M;

  bap__check_ordering_mint_hp (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);
  bav_R_set_maximal_variable (v);

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&T);

  bap_init_readonly_polynom_mint_hp (&B);
  bap_init_readonly_polynom_mint_hp (&coeff);
  bap_init_readonly_polynom_mint_hp (&value);
  bap_init_polynom_mint_hp (&G);
  bap_sort_polynom_mint_hp (&B, A);
  bap_sort_polynom_mint_hp (&value, val);

  if (!bap_is_numeric_polynom_mint_hp (&B) && bap_leader_polynom_mint_hp (&B) == v)
    {
      bap_begin_itercoeff_mint_hp (&iter, &B, v);
      bap_coeff_itercoeff_mint_hp (&coeff, &iter);
      bap_term_itercoeff_mint_hp (&T, &iter);
      bap_set_polynom_mint_hp (&G, &coeff);
/*
   Horner scheme
*/
      for (d = bav_degree_term (&T, v) - 1; d >= 0; d--)
        {
          bap_mul_polynom_mint_hp (&G, &G, &value);
          bav_set_term_variable (&T, v, d);
          bap_seek_coeff_itercoeff_mint_hp (&coeff, &iter, &T);
          if (!bap_is_zero_polynom_mint_hp (&coeff))
            bap_add_polynom_mint_hp (&G, &G, &coeff);
        }
      bap_close_itercoeff_mint_hp (&iter);
      ba0_pull_stack ();
      bap_set_polynom_mint_hp (R, &G);
    }
  else
    {
      ba0_pull_stack ();
      if (R != A)
        bap_set_polynom_mint_hp (R, A);
    }
  ba0_restore (&M);
  bav_R_pull_ordering ();
  bav_R_free_ordering (r);
  bap_physort_polynom_mint_hp (R);
}
#endif

#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpzm)
/*
 * Assigns A mod (x = alpha) to R
 */

/*
 * texinfo: bap_eval_polynom_value_int_p_mint_hp
 * Assign to @var{R} the polynomial obtained by evaluating @var{A} at 
 * @math{x = \alpha} where @math{(x, \alpha)} denotes @var{val}.
 */

BAP_DLL void
bap_eval_polynom_value_int_p_mint_hp (
    bap_polynom_mint_hp R,
    bap_polynom_mint_hp A,
    bav_value_int_p val)
{
  ba0_mint_hp_t c;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_mint_hp_init_set_si (c, val->value);
  ba0_pull_stack ();

  bap_eval_polynom_numeric_mint_hp (R, A, val->var, c);
  ba0_restore (&M);
}

/*
 * Assigns A mod point to *value
 */

/*
 * texinfo: bap_eval_polynom_point_int_p_mint_hp
 * Assign *@var{value} to @var{A} modulo @var{point}.
 */

BAP_DLL void
bap_eval_polynom_point_int_p_mint_hp (
    ba0_mint_hp_t *res,
    bap_polynom_mint_hp A,
    bav_point_int_p point)
{
  struct bap_itermon_mint_hp iter;
  ba0_mint_hp_t v, p;
  struct bav_term T;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&T);
  ba0_mint_hp_init (v);
  ba0_mint_hp_init (p);

  bap_begin_itermon_mint_hp (&iter, A);
  while (!bap_outof_itermon_mint_hp (&iter))
    {
      bap_term_itermon_mint_hp (&T, &iter);
      bav_term_at_point_int_p (p, &T, point);
      ba0_mint_hp_mul (p, *bap_coeff_itermon_mint_hp (&iter), p);
      ba0_mint_hp_add (v, v, p);
      bap_next_itermon_mint_hp (&iter);
    }
  ba0_pull_stack ();
  ba0_mint_hp_set (*res, v);
  ba0_restore (&M);
}

/*
 * Assigns A mod point to R.
 * It is assumed that point gives values to all the variables of A
 * apart the leader.
 */

/*
 * texinfo: bap_evalcoeff_polynom_point_int_p_mint_hp
 * Assign to @var{R} the polynomial @var{A} modulo @var{point}.
 * It is assumed that @var{point} gives values to all the variables of @var{A}
 * apart its leading one.
 */

BAP_DLL void
bap_evalcoeff_polynom_point_int_p_mint_hp (
    bap_polynom_mint_hp R,
    bap_polynom_mint_hp A,
    bav_point_int_p point)
{
  struct bap_creator_mint_hp crea;
  struct bap_itercoeff_mint_hp iter;
  struct bap_polynom_mint_hp C;
  bap_polynom_mint_hp P;
  struct bav_term T;
  ba0_mint_hp_t c;
  struct bav_rank rg;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_numeric_polynom_mint_hp (A))
    {
      if (A != R)
        bap_set_polynom_mint_hp (R, A);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bap_init_polynom_mint_hp (&C);
  ba0_mint_hp_init (c);

  rg = bap_rank_polynom_mint_hp (A);
  bav_init_term (&T);
  bav_set_term_rank (&T, &rg);
  P = bap_new_polynom_mint_hp ();
  bap_begin_creator_mint_hp (&crea, P, &T, bap_approx_total_rank, rg.deg);
  bap_begin_itercoeff_mint_hp (&iter, A, rg.var);
  while (!bap_outof_itercoeff_mint_hp (&iter))
    {
      bap_coeff_itercoeff_mint_hp (&C, &iter);
      bap_term_itercoeff_mint_hp (&T, &iter);
      bap_eval_polynom_point_int_p_mint_hp (&c, &C, point);
      if (!ba0_mint_hp_is_zero (c))
        bap_write_creator_mint_hp (&crea, &T, c);
      bap_next_itercoeff_mint_hp (&iter);
    }
  bap_close_creator_mint_hp (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mint_hp (R, P);
  ba0_restore (&M);
}

#endif
#undef BAD_FLAG_mint_hp
