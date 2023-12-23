#include "bap_polynom_mpzm.h"
#include "bap_creator_mpzm.h"
#include "bap_itermon_mpzm.h"
#include "bap_itercoeff_mpzm.h"
#include "bap_add_polynom_mpzm.h"
#include "bap_mul_polynom_mpzm.h"
#include "bap__check_mpzm.h"
#include "bap_geobucket_mpzm.h"

#define BAD_FLAG_mpzm

/*
 * $R = - A$.
 * If $A$ and $R$ are identical then the operation just consists in
 * changing the sign of the coefficients.
*/

/*
 * texinfo: bap_neg_polynom_mpzm
 * Assign @math{- A} to @var{R}.
 */

BAP_DLL void
bap_neg_polynom_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A)
{
  struct bap_itermon_mpzm iter;
  struct bap_creator_mpzm crea;
  struct bap_polynom_mpzm S;
  struct bav_term T;
  ba0_int_p nbmon;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_zero_polynom_mpzm (A))
    bap_set_polynom_zero_mpzm (R);
  else if (R == A)
    {
      bap_begin_itermon_mpzm (&iter, A);
      while (!bap_outof_itermon_mpzm (&iter))
        {
          ba0_mpzm_neg (*bap_coeff_itermon_mpzm (&iter),
              *bap_coeff_itermon_mpzm (&iter));
          bap_next_itermon_mpzm (&iter);
        }
    }
  else
    {
      bap_begin_itermon_mpzm (&iter, A);

      nbmon = bap_nbmon_polynom_mpzm (A) - R->clot->alloc;
      nbmon = nbmon > 0 ? nbmon : 0;

      if (bap_are_disjoint_polynom_mpzm (R, A))
        {
          bap_begin_creator_mpzm
              (&crea, R, &A->total_rank, bap_exact_total_rank, nbmon);

          if (bap_is_write_allable_creator_mpzm (&crea, A))
            bap_write_neg_all_creator_mpzm (&crea, A);
          else
            {
              ba0_push_another_stack ();
              ba0_record (&M);
              bav_init_term (&T);
              bav_realloc_term (&T, A->total_rank.size);
              ba0_pull_stack ();

              while (!bap_outof_itermon_mpzm (&iter))
                {
                  bap_term_itermon_mpzm (&T, &iter);
                  bap_write_neg_creator_mpzm
                      (&crea, &T, *bap_coeff_itermon_mpzm (&iter));
                  bap_next_itermon_mpzm (&iter);
                }

              ba0_restore (&M);
            }
          bap_close_creator_mpzm (&crea);
        }
      else
        {
          ba0_push_another_stack ();
          ba0_record (&M);
          bav_init_term (&T);
          bav_realloc_term (&T, A->total_rank.size);

          bap_init_polynom_mpzm (&S);

          bap_begin_creator_mpzm
              (&crea, &S, &A->total_rank,
              bap_exact_total_rank, bap_nbmon_polynom_mpzm (A));
          while (!bap_outof_itermon_mpzm (&iter))
            {
              bap_term_itermon_mpzm (&T, &iter);
              bap_write_neg_creator_mpzm
                  (&crea, &T, *bap_coeff_itermon_mpzm (&iter));
              bap_next_itermon_mpzm (&iter);
            }

          bap_close_creator_mpzm (&crea);
          ba0_pull_stack ();

          bap_set_polynom_mpzm (R, &S);
          ba0_restore (&M);
        }
    }
}

/*
 * $R = c\,A$.
 * If $A$ and $R$ are identical then the operation just consists in multiplying
 * the coefficients by~$c$.
 */

/*
 * texinfo: bap_mul_polynom_numeric_mpzm
 * Assign @math{c\,A} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_numeric_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    ba0_mpzm_t c)
{
  struct bap_itermon_mpzm iter;
  struct bap_creator_mpzm crea;
  struct bap_polynom_mpzm S;
  struct bav_term T;
  ba0_mpzm_t prod, *lc;
  enum bap_typeof_total_rank type;
  ba0_int_p nbmon;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (ba0_mpzm_is_zero (c))
    bap_set_polynom_zero_mpzm (R);
  else if (ba0_mpzm_is_one (c))
    {
      if (R != A)
        bap_set_polynom_mpzm (R, A);
    }
  else if (R == A && ba0_domain_mpzm ())
    {
      bap_begin_itermon_mpzm (&iter, A);
      while (!bap_outof_itermon_mpzm (&iter))
        {
          lc = bap_coeff_itermon_mpzm (&iter);
          ba0_mpzm_mul (*lc, *lc, c);
          if (ba0_mpzm_is_zero (*lc))
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          bap_next_itermon_mpzm (&iter);
        }
    }
  else
    {
      bap_begin_itermon_mpzm (&iter, A);
      nbmon = bap_nbmon_polynom_mpzm (A) - R->clot->alloc;
      nbmon = nbmon > 0 ? nbmon : 0;

      type = ba0_domain_mpzm ()? bap_exact_total_rank : bap_approx_total_rank;

      if (bap_are_disjoint_polynom_mpzm (R, A))
        {
          bap_begin_creator_mpzm (&crea, R, &A->total_rank, type, nbmon);

          if (bap_is_write_allable_creator_mpzm (&crea, A)
              && ba0_domain_mpzm ())
            bap_write_mul_all_creator_mpzm (&crea, A, c);
          else
            {
              ba0_push_another_stack ();
              ba0_record (&M);

              bav_init_term (&T);
              bav_realloc_term (&T, A->total_rank.size);

              ba0_mpzm_init (prod);

              while (!bap_outof_itermon_mpzm (&iter))
                {
                  lc = bap_coeff_itermon_mpzm (&iter);
                  ba0_mpzm_mul (prod, c, *lc);
                  if (!ba0_mpzm_is_zero (prod))
                    {
                      bap_term_itermon_mpzm (&T, &iter);
                      ba0_pull_stack ();
                      bap_write_creator_mpzm (&crea, &T, prod);
                      ba0_push_another_stack ();
                    }
                  else if (ba0_domain_mpzm ())
                    BA0_RAISE_EXCEPTION (BA0_ERRALG);
                  bap_next_itermon_mpzm (&iter);
                }

              ba0_pull_stack ();
              ba0_restore (&M);
            }

          bap_close_creator_mpzm (&crea);
        }
      else
        {
          ba0_push_another_stack ();
          ba0_record (&M);

          bap_init_polynom_mpzm (&S);

          bav_init_term (&T);
          bav_realloc_term (&T, A->total_rank.size);

          ba0_mpzm_init (prod);

          bap_begin_creator_mpzm
              (&crea, &S, &A->total_rank, type, bap_nbmon_polynom_mpzm (A));

          while (!bap_outof_itermon_mpzm (&iter))
            {
              lc = bap_coeff_itermon_mpzm (&iter);
              ba0_mpzm_mul (prod, c, *lc);
              if (!ba0_mpzm_is_zero (prod))
                {
                  bap_term_itermon_mpzm (&T, &iter);
                  bap_write_creator_mpzm (&crea, &T, prod);
                }
              else if (ba0_domain_mpzm ())
                BA0_RAISE_EXCEPTION (BA0_ERRALG);
              bap_next_itermon_mpzm (&iter);
            }

          bap_close_creator_mpzm (&crea);

          ba0_pull_stack ();
          bap_set_polynom_mpzm (R, &S);
          ba0_restore (&M);
        }
    }
}

/* $R = A \, (x - \alpha)$ where $\mbox{\em val} = (x, \alpha)$.  */

/*
 * texinfo: bap_mul_polynom_value_int_p_mpzm
 * Assign @math{A \, (x - \alpha)} to @var{R}, where @math{(x,\, \alpha)}
 * denotes @var{val}.
 */

BAP_DLL void
bap_mul_polynom_value_int_p_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    bav_value_int_p val)
{
  struct bav_term T;
  struct bav_rank rg;
  ba0_mpzm_t c;
  struct bap_creator_mpzm crea;
  bap_polynom_mpzm P;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&T);
  rg.var = val->var;
  rg.deg = 1;
  bav_set_term_rank (&T, &rg);
  P = bap_new_polynom_mpzm ();
  bap_begin_creator_mpzm (&crea, P, &T, bap_exact_total_rank, 2);
  ba0_mpzm_init_set_ui (c, 1);
  bap_write_creator_mpzm (&crea, &T, c);
  bav_set_term_one (&T);
  ba0_mpzm_set_si (c, val->value);
  bap_write_neg_creator_mpzm (&crea, &T, c);
  bap_close_creator_mpzm (&crea);
  ba0_pull_stack ();
  bap_mul_polynom_mpzm (R, A, P);
  ba0_restore (&M);
}

/* $R = A \, T$.  */

/*
 * texinfo: bap_mul_polynom_term_mpzm
 * Assign @math{A \, T} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_term_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    bav_term T)
{
  struct bap_itermon_mpzm iter;
  struct bap_creator_mpzm crea;
  bap_polynom_mpzm P;
  struct bav_term U;
  struct ba0_mark M;

  bap__check_ordering_mpzm (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bav_is_one_term (T))
    {
      if (R != A)
        bap_set_polynom_mpzm (R, A);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&U);
  bav_set_term (&U, &A->total_rank);
  bav_mul_term (&U, &U, T);
  bap_begin_itermon_mpzm (&iter, A);
  P = bap_new_polynom_mpzm ();
  bap_begin_creator_mpzm
      (&crea, P, &U, bap_exact_total_rank, bap_nbmon_polynom_mpzm (A));
  while (!bap_outof_itermon_mpzm (&iter))
    {
      bap_term_itermon_mpzm (&U, &iter);
      bav_mul_term (&U, &U, T);
      bap_write_creator_mpzm (&crea, &U, *bap_coeff_itermon_mpzm (&iter));
      bap_next_itermon_mpzm (&iter);
    }
  bap_close_creator_mpzm (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mpzm (R, P);
  ba0_restore (&M);
}

/*
 * texinfo: bap_mul_polynom_variable_mpzm
 * Assign @math{A \, v^d} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_variable_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    bav_variable v,
    bav_Idegree d)
{
  struct bav_term term;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  bav_init_term (&term);
  bav_set_term_variable (&term, v, d);
  ba0_pull_stack ();
  bap_mul_polynom_term_mpzm (R, A, &term);
  ba0_restore (&M);
}

/* $R = A \, c\,T$.  */

/*
 * texinfo: bap_mul_polynom_monom_mpzm
 * Assign @math{A \, c\, T} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_monom_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    ba0_mpzm_t c,
    bav_term T)
{
  struct bap_itermon_mpzm iter;
  struct bap_creator_mpzm crea;
  bap_polynom_mpzm P;
  struct bav_term U;
  ba0_mpzm_t d;
  struct ba0_mark M;

  bap__check_ordering_mpzm (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (ba0_mpzm_is_zero (c))
    {
      bap_set_polynom_zero_mpzm (R);
      return;
    }
  else if (ba0_mpzm_is_one (c))
    {
      bap_mul_polynom_term_mpzm (R, A, T);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&U);
  bav_set_term (&U, &A->total_rank);
  bav_mul_term (&U, &U, T);
  bap_begin_itermon_mpzm (&iter, A);

  P = bap_new_polynom_mpzm ();
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpq)
  bap_begin_creator_mpzm
      (&crea, P, &U, bap_exact_total_rank, bap_nbmon_polynom_mpzm (A));
#else
  bap_begin_creator_mpzm
      (&crea, P, &U, bap_approx_total_rank, bap_nbmon_polynom_mpzm (A));
#endif

  ba0_mpzm_init (d);

  while (!bap_outof_itermon_mpzm (&iter))
    {
      bap_term_itermon_mpzm (&U, &iter);
      bav_mul_term (&U, &U, T);
      ba0_mpzm_mul (d, c, *bap_coeff_itermon_mpzm (&iter));
      bap_write_creator_mpzm (&crea, &U, d);
      bap_next_itermon_mpzm (&iter);
    }
  bap_close_creator_mpzm (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mpzm (R, P);
  ba0_restore (&M);
}

/*****************************************************************************
 MULTIPLICATION
 *****************************************************************************/

static void
bap_mul_elem_polynom_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    bap_polynom_mpzm B)
{
  struct bap_creator_mpzm crea;
  struct bap_itermon_mpzm iterA, iterB;
  struct bap_polynom_mpzm R1;
  struct bap_geobucket_mpzm geo;
  ba0_mpzm_t cz, *ca, *cb;
  struct bav_term TA, TB, TTB;
  enum bap_typeof_total_rank type;
  struct ba0_mark M;

  if (bap_nbmon_polynom_mpzm (A) > bap_nbmon_polynom_mpzm (B))
    BA0_SWAP (bap_polynom_mpzm, A, B);

  type = ba0_domain_mpzm ()? bap_exact_total_rank : bap_approx_total_rank;

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_mpzm_init (cz);

  bav_init_term (&TTB);
  bav_set_term (&TTB, &B->total_rank);

  bav_init_term (&TA);
  bav_init_term (&TB);

  bap_init_geobucket_mpzm (&geo);
  bap_init_polynom_mpzm (&R1);

  bap_begin_itermon_mpzm (&iterA, A);
  while (!bap_outof_itermon_mpzm (&iterA))
    {
      ca = bap_coeff_itermon_mpzm (&iterA);
      bap_term_itermon_mpzm (&TA, &iterA);
      bav_mul_term (&TB, &TTB, &TA);
      bap_begin_creator_mpzm
          (&crea, &R1, &TB, type, bap_nbmon_polynom_mpzm (B));
      bap_begin_itermon_mpzm (&iterB, B);
      while (!bap_outof_itermon_mpzm (&iterB))
        {
          cb = bap_coeff_itermon_mpzm (&iterB);
          ba0_mpzm_mul (cz, *ca, *cb);
          bap_term_itermon_mpzm (&TB, &iterB);
          bav_mul_term (&TB, &TB, &TA);
          bap_write_creator_mpzm (&crea, &TB, cz);
          bap_next_itermon_mpzm (&iterB);
        }
      bap_close_creator_mpzm (&crea);
      bap_add_geobucket_mpzm (&geo, &R1);
      bap_next_itermon_mpzm (&iterA);
    }
  ba0_pull_stack ();
  bap_set_polynom_geobucket_mpzm (R, &geo);
  ba0_restore (&M);
}

/* $R = A \, B$.  */

/*
 * texinfo: bap_mul_polynom_mpzm
 * Assign @math{A\,B} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    bap_polynom_mpzm B)
{
  struct bap_itercoeff_mpzm iterA, iterB;
  struct bap_itermon_mpzm iter;
  struct bap_creator_mpzm crea;
  struct bap_polynom_mpzm C, CA, CB;
  bap_polynom_mpzm AA, BB, P;
  struct bav_term T, U, TA, TB;
  bav_variable xa, xb, v;
  bav_Iordering r;
  ba0_int_p i;
  struct ba0_mark M;

  bap__check_compatible_mpzm (A, B);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_numeric_polynom_mpzm (B))
    BA0_SWAP (bap_polynom_mpzm, A, B);
/*
   Si l'un des deux polynomes est constant, A est constant
*/
  if (bap_is_numeric_polynom_mpzm (A))
    {
      if (bap_is_zero_polynom_mpzm (A) || bap_is_zero_polynom_mpzm (B))
        bap_set_polynom_zero_mpzm (R);
      else
        {
          ba0_mpzm_t c;            /* Sinon bug quand A == R */
          ba0_push_another_stack ();
          ba0_record (&M);
          ba0_mpzm_init_set (c, *bap_numeric_initial_polynom_mpzm (A));
          ba0_pull_stack ();
          bap_mul_polynom_numeric_mpzm (R, B, c);
          ba0_restore (&M);
        }
      return;
    }

  if (bap_nbmon_polynom_mpzm (B) == 1)
    {
      BA0_SWAP (bap_polynom_mpzm, A, B);
    }
/*
   Si l'un des deux polynomes est reduit a un monome alors A l'est.
   Optimisation mais non necessaire.
*/
  if (bap_nbmon_polynom_mpzm (A) == 1)
    {
      ba0_mpzm_t c;

      ba0_push_another_stack ();
      ba0_record (&M);
      bap_begin_itermon_mpzm (&iter, A);
      bav_init_term (&T);
      bap_term_itermon_mpzm (&T, &iter);
      ba0_mpzm_init_set (c, *bap_coeff_itermon_mpzm (&iter));
      ba0_pull_stack ();
      bap_mul_polynom_monom_mpzm (R, B, c, &T);
      ba0_restore (&M);
      return;
    }
/*
   Ni A ni B n'est constant
   On marque a 2 les variables communes aux deux polynomes et a 1 les autres
*/
  for (i = 0; i < A->total_rank.size; i++)
    A->total_rank.rg[i].var->hack = 0;
  for (i = 0; i < B->total_rank.size; i++)
    B->total_rank.rg[i].var->hack = 0;
  for (i = 0; i < A->total_rank.size; i++)
    A->total_rank.rg[i].var->hack++;
  for (i = 0; i < B->total_rank.size; i++)
    B->total_rank.rg[i].var->hack++;
/*
   Dans le bav_type_ordering r, les variables non communes sont plus grandes
	que les autres.
   xa = la plus petite bav_variable de A non commune a B (ou nulle)
   xb = la plus petite bav_variable de B non commune a A (ou nulle)
*/

  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);

  xa = BAV_NOT_A_VARIABLE;
  for (i = A->total_rank.size - 1; i >= 0; i--)
    {
      v = A->total_rank.rg[i].var;
      if (v->hack == 1)
        {
          if (xa == BAV_NOT_A_VARIABLE)
            xa = v;
          bav_R_set_maximal_variable (v);
        }
    }
  xb = BAV_NOT_A_VARIABLE;
  for (i = B->total_rank.size - 1; i >= 0; i--)
    {
      v = B->total_rank.rg[i].var;
      if (v->hack == 1)
        {
          if (xb == BAV_NOT_A_VARIABLE)
            xb = v;
          bav_R_set_maximal_variable (v);
        }
    }
/*
   Si l'un des deux polynomes a toutes ses variables dans l'autre alors
	c'est le cas pour B.
*/
  if (xa == BAV_NOT_A_VARIABLE)
    {
      BA0_SWAP (bap_polynom_mpzm, A, B);
      BA0_SWAP (bav_variable, xa, xb);
    }
/*
   Exit le cas de deux polynomes sur le meme alphabet
*/
  if (xa == BAV_NOT_A_VARIABLE)
    {
      bav_R_pull_ordering ();
      bav_R_free_ordering (r);
      bap_mul_elem_polynom_mpzm (R, A, B);
      return;
    }
/*
   A depend de variables non communes avec B
*/
  ba0_push_another_stack ();
  ba0_record (&M);

  {
    bap_polynom_mpzm AA0 = bap_new_readonly_polynom_mpzm ();
    bap_sort_polynom_mpzm (AA0, A);
    AA = bap_new_polynom_mpzm ();
    bap_set_polynom_mpzm (AA, AA0);
  }

  bap_begin_itercoeff_mpzm (&iterA, AA, xa);

  if (xb != BAV_NOT_A_VARIABLE)
    {
      bap_polynom_mpzm BB0 = bap_new_readonly_polynom_mpzm ();
      bap_sort_polynom_mpzm (BB0, B);
      BB = bap_new_polynom_mpzm ();
      bap_set_polynom_mpzm (BB, BB0);
    }
  else
    BB = B;

  bap_init_polynom_mpzm (&C);
  bap_init_polynom_mpzm (&CA);
  bap_init_polynom_mpzm (&CB);
  bav_init_term (&T);
  bav_init_term (&TA);
  bav_init_term (&TB);
  bav_init_term (&U);

  bav_mul_term (&T, &AA->total_rank, &BB->total_rank);
  i = BA0_MAX (bap_nbmon_polynom_mpzm (AA), bap_nbmon_polynom_mpzm (BB));
/*
 * Note: the monomials of P will temporarily not be sorted
 */
  P = bap_new_polynom_mpzm ();
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpq)
  bap_begin_creator_mpzm (&crea, P, &T, bap_exact_total_rank, i);
#else
  bap_begin_creator_mpzm (&crea, P, &T, bap_approx_total_rank, i);
#endif

  while (!bap_outof_itercoeff_mpzm (&iterA))
    {
      bap_coeff_itercoeff_mpzm (&CA, &iterA);
      bap_term_itercoeff_mpzm (&TA, &iterA);
      bap_begin_itercoeff_mpzm
          (&iterB, BB, xb == BAV_NOT_A_VARIABLE ? xa : xb);
      while (!bap_outof_itercoeff_mpzm (&iterB))
        {
          bap_coeff_itercoeff_mpzm (&CB, &iterB);
          bap_term_itercoeff_mpzm (&TB, &iterB);

          bav_mul_term (&T, &TA, &TB);
          bap_mul_elem_polynom_mpzm (&C, &CA, &CB);

          bap_begin_itermon_mpzm (&iter, &C);
          while (!bap_outof_itermon_mpzm (&iter))
            {
              ba0_mpzm_t *c;

              c = bap_coeff_itermon_mpzm (&iter);
              bap_term_itermon_mpzm (&U, &iter);
              bav_mul_term (&U, &U, &T);
              bap_write_creator_mpzm (&crea, &U, *c);
              bap_next_itermon_mpzm (&iter);
            }
          bap_next_itercoeff_mpzm (&iterB);
        }
      bap_next_itercoeff_mpzm (&iterA);
    }
  bap_close_creator_mpzm (&crea);
  bav_R_pull_ordering ();
/*
 * Now, the monomials get sorted
 */
  bap_physort_polynom_mpzm (P);

  bav_R_free_ordering (r);
  ba0_pull_stack ();

  i = BA0_MAX (bap_nbmon_polynom_mpzm (A), bap_nbmon_polynom_mpzm (B));

  bap_set_polynom_mpzm (R, P);

  ba0_restore (&M);
}

/* $R = A^n$.  */

/*
 * texinfo: bap_pow_polynom_mpzm
 * Assign @math{A^d} to @var{R}.
 */

BAP_DLL void
bap_pow_polynom_mpzm (
    bap_polynom_mpzm R,
    bap_polynom_mpzm A,
    bav_Idegree n)
{
  struct bap_polynom_mpzm E, F;
  bav_Idegree p;
  bool E_vaut_un;
  struct ba0_mark M;

  if (n == 0)
    bap_set_polynom_one_mpzm (R);
  else if (n == 1)
    {
      if (R != A)
        bap_set_polynom_mpzm (R, A);
    }
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      if (n % 2 == 1)
        {
          bap_init_polynom_mpzm (&E);
          bap_set_polynom_mpzm (&E, A);
          E_vaut_un = false;
        }
      else
        E_vaut_un = true;

      bap_init_polynom_mpzm (&F);
      bap_mul_polynom_mpzm (&F, A, A);

      for (p = n / 2; p != 1; p /= 2)
        {
          if (p % 2 == 1)
            {
              if (E_vaut_un)
                {
                  bap_init_polynom_mpzm (&E);
                  bap_set_polynom_mpzm (&E, &F);
                  E_vaut_un = false;
                }
              else
                bap_mul_polynom_mpzm (&E, &F, &E);
            }
          bap_mul_polynom_mpzm (&F, &F, &F);
        }
      ba0_pull_stack ();
      if (E_vaut_un)
        bap_set_polynom_mpzm (R, &F);
      else
        bap_mul_polynom_mpzm (R, &E, &F);
      ba0_restore (&M);
    }
}

#undef BAD_FLAG_mpzm
