#include "bap_polynom_mpq.h"
#include "bap_creator_mpq.h"
#include "bap_itermon_mpq.h"
#include "bap_itercoeff_mpq.h"
#include "bap_add_polynom_mpq.h"
#include "bap_mul_polynom_mpq.h"
#include "bap__check_mpq.h"
#include "bap_geobucket_mpq.h"

#define BAD_FLAG_mpq

/*
 * $R = - A$.
 * If $A$ and $R$ are identical then the operation just consists in
 * changing the sign of the coefficients.
*/

/*
 * texinfo: bap_neg_polynom_mpq
 * Assign @math{- A} to @var{R}.
 */

BAP_DLL void
bap_neg_polynom_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A)
{
  struct bap_itermon_mpq iter;
  struct bap_creator_mpq crea;
  struct bap_polynom_mpq S;
  struct bav_term T;
  ba0_int_p nbmon;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_zero_polynom_mpq (A))
    bap_set_polynom_zero_mpq (R);
  else if (R == A)
    {
      bap_begin_itermon_mpq (&iter, A);
      while (!bap_outof_itermon_mpq (&iter))
        {
          ba0_mpq_neg (*bap_coeff_itermon_mpq (&iter),
              *bap_coeff_itermon_mpq (&iter));
          bap_next_itermon_mpq (&iter);
        }
    }
  else
    {
      bap_begin_itermon_mpq (&iter, A);

      nbmon = bap_nbmon_polynom_mpq (A) - R->clot->alloc;
      nbmon = nbmon > 0 ? nbmon : 0;

      if (bap_are_disjoint_polynom_mpq (R, A))
        {
          bap_begin_creator_mpq
              (&crea, R, &A->total_rank, bap_exact_total_rank, nbmon);

          if (bap_is_write_allable_creator_mpq (&crea, A))
            bap_write_neg_all_creator_mpq (&crea, A);
          else
            {
              ba0_push_another_stack ();
              ba0_record (&M);
              bav_init_term (&T);
              bav_realloc_term (&T, A->total_rank.size);
              ba0_pull_stack ();

              while (!bap_outof_itermon_mpq (&iter))
                {
                  bap_term_itermon_mpq (&T, &iter);
                  bap_write_neg_creator_mpq
                      (&crea, &T, *bap_coeff_itermon_mpq (&iter));
                  bap_next_itermon_mpq (&iter);
                }

              ba0_restore (&M);
            }
          bap_close_creator_mpq (&crea);
        }
      else
        {
          ba0_push_another_stack ();
          ba0_record (&M);
          bav_init_term (&T);
          bav_realloc_term (&T, A->total_rank.size);

          bap_init_polynom_mpq (&S);

          bap_begin_creator_mpq
              (&crea, &S, &A->total_rank,
              bap_exact_total_rank, bap_nbmon_polynom_mpq (A));
          while (!bap_outof_itermon_mpq (&iter))
            {
              bap_term_itermon_mpq (&T, &iter);
              bap_write_neg_creator_mpq
                  (&crea, &T, *bap_coeff_itermon_mpq (&iter));
              bap_next_itermon_mpq (&iter);
            }

          bap_close_creator_mpq (&crea);
          ba0_pull_stack ();

          bap_set_polynom_mpq (R, &S);
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
 * texinfo: bap_mul_polynom_numeric_mpq
 * Assign @math{c\,A} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_numeric_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    ba0_mpq_t c)
{
  struct bap_itermon_mpq iter;
  struct bap_creator_mpq crea;
  struct bap_polynom_mpq S;
  struct bav_term T;
  ba0_mpq_t prod, *lc;
  enum bap_typeof_total_rank type;
  ba0_int_p nbmon;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (ba0_mpq_is_zero (c))
    bap_set_polynom_zero_mpq (R);
  else if (ba0_mpq_is_one (c))
    {
      if (R != A)
        bap_set_polynom_mpq (R, A);
    }
  else if (R == A && ba0_domain_mpq ())
    {
      bap_begin_itermon_mpq (&iter, A);
      while (!bap_outof_itermon_mpq (&iter))
        {
          lc = bap_coeff_itermon_mpq (&iter);
          ba0_mpq_mul (*lc, *lc, c);
          if (ba0_mpq_is_zero (*lc))
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          bap_next_itermon_mpq (&iter);
        }
    }
  else
    {
      bap_begin_itermon_mpq (&iter, A);
      nbmon = bap_nbmon_polynom_mpq (A) - R->clot->alloc;
      nbmon = nbmon > 0 ? nbmon : 0;

      type = ba0_domain_mpq ()? bap_exact_total_rank : bap_approx_total_rank;

      if (bap_are_disjoint_polynom_mpq (R, A))
        {
          bap_begin_creator_mpq (&crea, R, &A->total_rank, type, nbmon);

          if (bap_is_write_allable_creator_mpq (&crea, A)
              && ba0_domain_mpq ())
            bap_write_mul_all_creator_mpq (&crea, A, c);
          else
            {
              ba0_push_another_stack ();
              ba0_record (&M);

              bav_init_term (&T);
              bav_realloc_term (&T, A->total_rank.size);

              ba0_mpq_init (prod);

              while (!bap_outof_itermon_mpq (&iter))
                {
                  lc = bap_coeff_itermon_mpq (&iter);
                  ba0_mpq_mul (prod, c, *lc);
                  if (!ba0_mpq_is_zero (prod))
                    {
                      bap_term_itermon_mpq (&T, &iter);
                      ba0_pull_stack ();
                      bap_write_creator_mpq (&crea, &T, prod);
                      ba0_push_another_stack ();
                    }
                  else if (ba0_domain_mpq ())
                    BA0_RAISE_EXCEPTION (BA0_ERRALG);
                  bap_next_itermon_mpq (&iter);
                }

              ba0_pull_stack ();
              ba0_restore (&M);
            }

          bap_close_creator_mpq (&crea);
        }
      else
        {
          ba0_push_another_stack ();
          ba0_record (&M);

          bap_init_polynom_mpq (&S);

          bav_init_term (&T);
          bav_realloc_term (&T, A->total_rank.size);

          ba0_mpq_init (prod);

          bap_begin_creator_mpq
              (&crea, &S, &A->total_rank, type, bap_nbmon_polynom_mpq (A));

          while (!bap_outof_itermon_mpq (&iter))
            {
              lc = bap_coeff_itermon_mpq (&iter);
              ba0_mpq_mul (prod, c, *lc);
              if (!ba0_mpq_is_zero (prod))
                {
                  bap_term_itermon_mpq (&T, &iter);
                  bap_write_creator_mpq (&crea, &T, prod);
                }
              else if (ba0_domain_mpq ())
                BA0_RAISE_EXCEPTION (BA0_ERRALG);
              bap_next_itermon_mpq (&iter);
            }

          bap_close_creator_mpq (&crea);

          ba0_pull_stack ();
          bap_set_polynom_mpq (R, &S);
          ba0_restore (&M);
        }
    }
}

/* $R = A \, (x - \alpha)$ where $\mbox{\em val} = (x, \alpha)$.  */

/*
 * texinfo: bap_mul_polynom_value_int_p_mpq
 * Assign @math{A \, (x - \alpha)} to @var{R}, where @math{(x,\, \alpha)}
 * denotes @var{val}.
 */

BAP_DLL void
bap_mul_polynom_value_int_p_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    bav_value_int_p val)
{
  struct bav_term T;
  struct bav_rank rg;
  ba0_mpq_t c;
  struct bap_creator_mpq crea;
  bap_polynom_mpq P;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&T);
  rg.var = val->var;
  rg.deg = 1;
  bav_set_term_rank (&T, &rg);
  P = bap_new_polynom_mpq ();
  bap_begin_creator_mpq (&crea, P, &T, bap_exact_total_rank, 2);
  ba0_mpq_init_set_ui (c, 1);
  bap_write_creator_mpq (&crea, &T, c);
  bav_set_term_one (&T);
  ba0_mpq_set_si (c, val->value);
  bap_write_neg_creator_mpq (&crea, &T, c);
  bap_close_creator_mpq (&crea);
  ba0_pull_stack ();
  bap_mul_polynom_mpq (R, A, P);
  ba0_restore (&M);
}

/* $R = A \, T$.  */

/*
 * texinfo: bap_mul_polynom_term_mpq
 * Assign @math{A \, T} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_term_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    bav_term T)
{
  struct bap_itermon_mpq iter;
  struct bap_creator_mpq crea;
  bap_polynom_mpq P;
  struct bav_term U;
  struct ba0_mark M;

  bap__check_ordering_mpq (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bav_is_one_term (T))
    {
      if (R != A)
        bap_set_polynom_mpq (R, A);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&U);
  bav_set_term (&U, &A->total_rank);
  bav_mul_term (&U, &U, T);
  bap_begin_itermon_mpq (&iter, A);
  P = bap_new_polynom_mpq ();
  bap_begin_creator_mpq
      (&crea, P, &U, bap_exact_total_rank, bap_nbmon_polynom_mpq (A));
  while (!bap_outof_itermon_mpq (&iter))
    {
      bap_term_itermon_mpq (&U, &iter);
      bav_mul_term (&U, &U, T);
      bap_write_creator_mpq (&crea, &U, *bap_coeff_itermon_mpq (&iter));
      bap_next_itermon_mpq (&iter);
    }
  bap_close_creator_mpq (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mpq (R, P);
  ba0_restore (&M);
}

/*
 * texinfo: bap_mul_polynom_variable_mpq
 * Assign @math{A \, v^d} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_variable_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
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
  bap_mul_polynom_term_mpq (R, A, &term);
  ba0_restore (&M);
}

/* $R = A \, c\,T$.  */

/*
 * texinfo: bap_mul_polynom_monom_mpq
 * Assign @math{A \, c\, T} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_monom_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    ba0_mpq_t c,
    bav_term T)
{
  struct bap_itermon_mpq iter;
  struct bap_creator_mpq crea;
  bap_polynom_mpq P;
  struct bav_term U;
  ba0_mpq_t d;
  struct ba0_mark M;

  bap__check_ordering_mpq (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (ba0_mpq_is_zero (c))
    {
      bap_set_polynom_zero_mpq (R);
      return;
    }
  else if (ba0_mpq_is_one (c))
    {
      bap_mul_polynom_term_mpq (R, A, T);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&U);
  bav_set_term (&U, &A->total_rank);
  bav_mul_term (&U, &U, T);
  bap_begin_itermon_mpq (&iter, A);

  P = bap_new_polynom_mpq ();
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpq)
  bap_begin_creator_mpq
      (&crea, P, &U, bap_exact_total_rank, bap_nbmon_polynom_mpq (A));
#else
  bap_begin_creator_mpq
      (&crea, P, &U, bap_approx_total_rank, bap_nbmon_polynom_mpq (A));
#endif

  ba0_mpq_init (d);

  while (!bap_outof_itermon_mpq (&iter))
    {
      bap_term_itermon_mpq (&U, &iter);
      bav_mul_term (&U, &U, T);
      ba0_mpq_mul (d, c, *bap_coeff_itermon_mpq (&iter));
      bap_write_creator_mpq (&crea, &U, d);
      bap_next_itermon_mpq (&iter);
    }
  bap_close_creator_mpq (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mpq (R, P);
  ba0_restore (&M);
}

/*****************************************************************************
 MULTIPLICATION
 *****************************************************************************/

static void
bap_mul_elem_polynom_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    bap_polynom_mpq B)
{
  struct bap_creator_mpq crea;
  struct bap_itermon_mpq iterA, iterB;
  struct bap_polynom_mpq R1;
  struct bap_geobucket_mpq geo;
  ba0_mpq_t cz, *ca, *cb;
  struct bav_term TA, TB, TTB;
  enum bap_typeof_total_rank type;
  struct ba0_mark M;

  if (bap_nbmon_polynom_mpq (A) > bap_nbmon_polynom_mpq (B))
    BA0_SWAP (bap_polynom_mpq, A, B);

  type = ba0_domain_mpq ()? bap_exact_total_rank : bap_approx_total_rank;

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_mpq_init (cz);

  bav_init_term (&TTB);
  bav_set_term (&TTB, &B->total_rank);

  bav_init_term (&TA);
  bav_init_term (&TB);

  bap_init_geobucket_mpq (&geo);
  bap_init_polynom_mpq (&R1);

  bap_begin_itermon_mpq (&iterA, A);
  while (!bap_outof_itermon_mpq (&iterA))
    {
      ca = bap_coeff_itermon_mpq (&iterA);
      bap_term_itermon_mpq (&TA, &iterA);
      bav_mul_term (&TB, &TTB, &TA);
      bap_begin_creator_mpq
          (&crea, &R1, &TB, type, bap_nbmon_polynom_mpq (B));
      bap_begin_itermon_mpq (&iterB, B);
      while (!bap_outof_itermon_mpq (&iterB))
        {
          cb = bap_coeff_itermon_mpq (&iterB);
          ba0_mpq_mul (cz, *ca, *cb);
          bap_term_itermon_mpq (&TB, &iterB);
          bav_mul_term (&TB, &TB, &TA);
          bap_write_creator_mpq (&crea, &TB, cz);
          bap_next_itermon_mpq (&iterB);
        }
      bap_close_creator_mpq (&crea);
      bap_add_geobucket_mpq (&geo, &R1);
      bap_next_itermon_mpq (&iterA);
    }
  ba0_pull_stack ();
  bap_set_polynom_geobucket_mpq (R, &geo);
  ba0_restore (&M);
}

/* $R = A \, B$.  */

/*
 * texinfo: bap_mul_polynom_mpq
 * Assign @math{A\,B} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    bap_polynom_mpq B)
{
  struct bap_itercoeff_mpq iterA, iterB;
  struct bap_itermon_mpq iter;
  struct bap_creator_mpq crea;
  struct bap_polynom_mpq C, CA, CB;
  bap_polynom_mpq AA, BB, P;
  struct bav_term T, U, TA, TB;
  bav_variable xa, xb, v;
  bav_Iordering r;
  ba0_int_p i;
  struct ba0_mark M;

  bap__check_compatible_mpq (A, B);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_numeric_polynom_mpq (B))
    BA0_SWAP (bap_polynom_mpq, A, B);
/*
   Si l'un des deux polynomes est constant, A est constant
*/
  if (bap_is_numeric_polynom_mpq (A))
    {
      if (bap_is_zero_polynom_mpq (A) || bap_is_zero_polynom_mpq (B))
        bap_set_polynom_zero_mpq (R);
      else
        {
          ba0_mpq_t c;            /* Sinon bug quand A == R */
          ba0_push_another_stack ();
          ba0_record (&M);
          ba0_mpq_init_set (c, *bap_numeric_initial_polynom_mpq (A));
          ba0_pull_stack ();
          bap_mul_polynom_numeric_mpq (R, B, c);
          ba0_restore (&M);
        }
      return;
    }

  if (bap_nbmon_polynom_mpq (B) == 1)
    {
      BA0_SWAP (bap_polynom_mpq, A, B);
    }
/*
   Si l'un des deux polynomes est reduit a un monome alors A l'est.
   Optimisation mais non necessaire.
*/
  if (bap_nbmon_polynom_mpq (A) == 1)
    {
      ba0_mpq_t c;

      ba0_push_another_stack ();
      ba0_record (&M);
      bap_begin_itermon_mpq (&iter, A);
      bav_init_term (&T);
      bap_term_itermon_mpq (&T, &iter);
      ba0_mpq_init_set (c, *bap_coeff_itermon_mpq (&iter));
      ba0_pull_stack ();
      bap_mul_polynom_monom_mpq (R, B, c, &T);
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
      BA0_SWAP (bap_polynom_mpq, A, B);
      BA0_SWAP (bav_variable, xa, xb);
    }
/*
   Exit le cas de deux polynomes sur le meme alphabet
*/
  if (xa == BAV_NOT_A_VARIABLE)
    {
      bav_R_pull_ordering ();
      bav_R_free_ordering (r);
      bap_mul_elem_polynom_mpq (R, A, B);
      return;
    }
/*
   A depend de variables non communes avec B
*/
  ba0_push_another_stack ();
  ba0_record (&M);

  {
    bap_polynom_mpq AA0 = bap_new_readonly_polynom_mpq ();
    bap_sort_polynom_mpq (AA0, A);
    AA = bap_new_polynom_mpq ();
    bap_set_polynom_mpq (AA, AA0);
  }

  bap_begin_itercoeff_mpq (&iterA, AA, xa);

  if (xb != BAV_NOT_A_VARIABLE)
    {
      bap_polynom_mpq BB0 = bap_new_readonly_polynom_mpq ();
      bap_sort_polynom_mpq (BB0, B);
      BB = bap_new_polynom_mpq ();
      bap_set_polynom_mpq (BB, BB0);
    }
  else
    BB = B;

  bap_init_polynom_mpq (&C);
  bap_init_polynom_mpq (&CA);
  bap_init_polynom_mpq (&CB);
  bav_init_term (&T);
  bav_init_term (&TA);
  bav_init_term (&TB);
  bav_init_term (&U);

  bav_mul_term (&T, &AA->total_rank, &BB->total_rank);
  i = BA0_MAX (bap_nbmon_polynom_mpq (AA), bap_nbmon_polynom_mpq (BB));
/*
 * Note: the monomials of P will temporarily not be sorted
 */
  P = bap_new_polynom_mpq ();
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpq)
  bap_begin_creator_mpq (&crea, P, &T, bap_exact_total_rank, i);
#else
  bap_begin_creator_mpq (&crea, P, &T, bap_approx_total_rank, i);
#endif

  while (!bap_outof_itercoeff_mpq (&iterA))
    {
      bap_coeff_itercoeff_mpq (&CA, &iterA);
      bap_term_itercoeff_mpq (&TA, &iterA);
      bap_begin_itercoeff_mpq
          (&iterB, BB, xb == BAV_NOT_A_VARIABLE ? xa : xb);
      while (!bap_outof_itercoeff_mpq (&iterB))
        {
          bap_coeff_itercoeff_mpq (&CB, &iterB);
          bap_term_itercoeff_mpq (&TB, &iterB);

          bav_mul_term (&T, &TA, &TB);
          bap_mul_elem_polynom_mpq (&C, &CA, &CB);

          bap_begin_itermon_mpq (&iter, &C);
          while (!bap_outof_itermon_mpq (&iter))
            {
              ba0_mpq_t *c;

              c = bap_coeff_itermon_mpq (&iter);
              bap_term_itermon_mpq (&U, &iter);
              bav_mul_term (&U, &U, &T);
              bap_write_creator_mpq (&crea, &U, *c);
              bap_next_itermon_mpq (&iter);
            }
          bap_next_itercoeff_mpq (&iterB);
        }
      bap_next_itercoeff_mpq (&iterA);
    }
  bap_close_creator_mpq (&crea);
  bav_R_pull_ordering ();
/*
 * Now, the monomials get sorted
 */
  bap_physort_polynom_mpq (P);

  bav_R_free_ordering (r);
  ba0_pull_stack ();

  i = BA0_MAX (bap_nbmon_polynom_mpq (A), bap_nbmon_polynom_mpq (B));

  bap_set_polynom_mpq (R, P);

  ba0_restore (&M);
}

/* $R = A^n$.  */

/*
 * texinfo: bap_pow_polynom_mpq
 * Assign @math{A^d} to @var{R}.
 */

BAP_DLL void
bap_pow_polynom_mpq (
    bap_polynom_mpq R,
    bap_polynom_mpq A,
    bav_Idegree n)
{
  struct bap_polynom_mpq E, F;
  bav_Idegree p;
  bool E_vaut_un;
  struct ba0_mark M;

  if (n == 0)
    bap_set_polynom_one_mpq (R);
  else if (n == 1)
    {
      if (R != A)
        bap_set_polynom_mpq (R, A);
    }
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      if (n % 2 == 1)
        {
          bap_init_polynom_mpq (&E);
          bap_set_polynom_mpq (&E, A);
          E_vaut_un = false;
        }
      else
        E_vaut_un = true;

      bap_init_polynom_mpq (&F);
      bap_mul_polynom_mpq (&F, A, A);

      for (p = n / 2; p != 1; p /= 2)
        {
          if (p % 2 == 1)
            {
              if (E_vaut_un)
                {
                  bap_init_polynom_mpq (&E);
                  bap_set_polynom_mpq (&E, &F);
                  E_vaut_un = false;
                }
              else
                bap_mul_polynom_mpq (&E, &F, &E);
            }
          bap_mul_polynom_mpq (&F, &F, &F);
        }
      ba0_pull_stack ();
      if (E_vaut_un)
        bap_set_polynom_mpq (R, &F);
      else
        bap_mul_polynom_mpq (R, &E, &F);
      ba0_restore (&M);
    }
}

#undef BAD_FLAG_mpq
