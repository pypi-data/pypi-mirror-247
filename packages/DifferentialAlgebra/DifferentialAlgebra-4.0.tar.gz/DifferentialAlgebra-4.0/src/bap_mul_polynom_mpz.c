#include "bap_polynom_mpz.h"
#include "bap_creator_mpz.h"
#include "bap_itermon_mpz.h"
#include "bap_itercoeff_mpz.h"
#include "bap_add_polynom_mpz.h"
#include "bap_mul_polynom_mpz.h"
#include "bap__check_mpz.h"
#include "bap_geobucket_mpz.h"

#define BAD_FLAG_mpz

/*
 * $R = - A$.
 * If $A$ and $R$ are identical then the operation just consists in
 * changing the sign of the coefficients.
*/

/*
 * texinfo: bap_neg_polynom_mpz
 * Assign @math{- A} to @var{R}.
 */

BAP_DLL void
bap_neg_polynom_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A)
{
  struct bap_itermon_mpz iter;
  struct bap_creator_mpz crea;
  struct bap_polynom_mpz S;
  struct bav_term T;
  ba0_int_p nbmon;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_zero_polynom_mpz (A))
    bap_set_polynom_zero_mpz (R);
  else if (R == A)
    {
      bap_begin_itermon_mpz (&iter, A);
      while (!bap_outof_itermon_mpz (&iter))
        {
          ba0_mpz_neg (*bap_coeff_itermon_mpz (&iter),
              *bap_coeff_itermon_mpz (&iter));
          bap_next_itermon_mpz (&iter);
        }
    }
  else
    {
      bap_begin_itermon_mpz (&iter, A);

      nbmon = bap_nbmon_polynom_mpz (A) - R->clot->alloc;
      nbmon = nbmon > 0 ? nbmon : 0;

      if (bap_are_disjoint_polynom_mpz (R, A))
        {
          bap_begin_creator_mpz
              (&crea, R, &A->total_rank, bap_exact_total_rank, nbmon);

          if (bap_is_write_allable_creator_mpz (&crea, A))
            bap_write_neg_all_creator_mpz (&crea, A);
          else
            {
              ba0_push_another_stack ();
              ba0_record (&M);
              bav_init_term (&T);
              bav_realloc_term (&T, A->total_rank.size);
              ba0_pull_stack ();

              while (!bap_outof_itermon_mpz (&iter))
                {
                  bap_term_itermon_mpz (&T, &iter);
                  bap_write_neg_creator_mpz
                      (&crea, &T, *bap_coeff_itermon_mpz (&iter));
                  bap_next_itermon_mpz (&iter);
                }

              ba0_restore (&M);
            }
          bap_close_creator_mpz (&crea);
        }
      else
        {
          ba0_push_another_stack ();
          ba0_record (&M);
          bav_init_term (&T);
          bav_realloc_term (&T, A->total_rank.size);

          bap_init_polynom_mpz (&S);

          bap_begin_creator_mpz
              (&crea, &S, &A->total_rank,
              bap_exact_total_rank, bap_nbmon_polynom_mpz (A));
          while (!bap_outof_itermon_mpz (&iter))
            {
              bap_term_itermon_mpz (&T, &iter);
              bap_write_neg_creator_mpz
                  (&crea, &T, *bap_coeff_itermon_mpz (&iter));
              bap_next_itermon_mpz (&iter);
            }

          bap_close_creator_mpz (&crea);
          ba0_pull_stack ();

          bap_set_polynom_mpz (R, &S);
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
 * texinfo: bap_mul_polynom_numeric_mpz
 * Assign @math{c\,A} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_numeric_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    ba0_mpz_t c)
{
  struct bap_itermon_mpz iter;
  struct bap_creator_mpz crea;
  struct bap_polynom_mpz S;
  struct bav_term T;
  ba0_mpz_t prod, *lc;
  enum bap_typeof_total_rank type;
  ba0_int_p nbmon;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (ba0_mpz_is_zero (c))
    bap_set_polynom_zero_mpz (R);
  else if (ba0_mpz_is_one (c))
    {
      if (R != A)
        bap_set_polynom_mpz (R, A);
    }
  else if (R == A && ba0_domain_mpz ())
    {
      bap_begin_itermon_mpz (&iter, A);
      while (!bap_outof_itermon_mpz (&iter))
        {
          lc = bap_coeff_itermon_mpz (&iter);
          ba0_mpz_mul (*lc, *lc, c);
          if (ba0_mpz_is_zero (*lc))
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          bap_next_itermon_mpz (&iter);
        }
    }
  else
    {
      bap_begin_itermon_mpz (&iter, A);
      nbmon = bap_nbmon_polynom_mpz (A) - R->clot->alloc;
      nbmon = nbmon > 0 ? nbmon : 0;

      type = ba0_domain_mpz ()? bap_exact_total_rank : bap_approx_total_rank;

      if (bap_are_disjoint_polynom_mpz (R, A))
        {
          bap_begin_creator_mpz (&crea, R, &A->total_rank, type, nbmon);

          if (bap_is_write_allable_creator_mpz (&crea, A)
              && ba0_domain_mpz ())
            bap_write_mul_all_creator_mpz (&crea, A, c);
          else
            {
              ba0_push_another_stack ();
              ba0_record (&M);

              bav_init_term (&T);
              bav_realloc_term (&T, A->total_rank.size);

              ba0_mpz_init (prod);

              while (!bap_outof_itermon_mpz (&iter))
                {
                  lc = bap_coeff_itermon_mpz (&iter);
                  ba0_mpz_mul (prod, c, *lc);
                  if (!ba0_mpz_is_zero (prod))
                    {
                      bap_term_itermon_mpz (&T, &iter);
                      ba0_pull_stack ();
                      bap_write_creator_mpz (&crea, &T, prod);
                      ba0_push_another_stack ();
                    }
                  else if (ba0_domain_mpz ())
                    BA0_RAISE_EXCEPTION (BA0_ERRALG);
                  bap_next_itermon_mpz (&iter);
                }

              ba0_pull_stack ();
              ba0_restore (&M);
            }

          bap_close_creator_mpz (&crea);
        }
      else
        {
          ba0_push_another_stack ();
          ba0_record (&M);

          bap_init_polynom_mpz (&S);

          bav_init_term (&T);
          bav_realloc_term (&T, A->total_rank.size);

          ba0_mpz_init (prod);

          bap_begin_creator_mpz
              (&crea, &S, &A->total_rank, type, bap_nbmon_polynom_mpz (A));

          while (!bap_outof_itermon_mpz (&iter))
            {
              lc = bap_coeff_itermon_mpz (&iter);
              ba0_mpz_mul (prod, c, *lc);
              if (!ba0_mpz_is_zero (prod))
                {
                  bap_term_itermon_mpz (&T, &iter);
                  bap_write_creator_mpz (&crea, &T, prod);
                }
              else if (ba0_domain_mpz ())
                BA0_RAISE_EXCEPTION (BA0_ERRALG);
              bap_next_itermon_mpz (&iter);
            }

          bap_close_creator_mpz (&crea);

          ba0_pull_stack ();
          bap_set_polynom_mpz (R, &S);
          ba0_restore (&M);
        }
    }
}

/* $R = A \, (x - \alpha)$ where $\mbox{\em val} = (x, \alpha)$.  */

/*
 * texinfo: bap_mul_polynom_value_int_p_mpz
 * Assign @math{A \, (x - \alpha)} to @var{R}, where @math{(x,\, \alpha)}
 * denotes @var{val}.
 */

BAP_DLL void
bap_mul_polynom_value_int_p_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bav_value_int_p val)
{
  struct bav_term T;
  struct bav_rank rg;
  ba0_mpz_t c;
  struct bap_creator_mpz crea;
  bap_polynom_mpz P;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&T);
  rg.var = val->var;
  rg.deg = 1;
  bav_set_term_rank (&T, &rg);
  P = bap_new_polynom_mpz ();
  bap_begin_creator_mpz (&crea, P, &T, bap_exact_total_rank, 2);
  ba0_mpz_init_set_ui (c, 1);
  bap_write_creator_mpz (&crea, &T, c);
  bav_set_term_one (&T);
  ba0_mpz_set_si (c, val->value);
  bap_write_neg_creator_mpz (&crea, &T, c);
  bap_close_creator_mpz (&crea);
  ba0_pull_stack ();
  bap_mul_polynom_mpz (R, A, P);
  ba0_restore (&M);
}

/* $R = A \, T$.  */

/*
 * texinfo: bap_mul_polynom_term_mpz
 * Assign @math{A \, T} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_term_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bav_term T)
{
  struct bap_itermon_mpz iter;
  struct bap_creator_mpz crea;
  bap_polynom_mpz P;
  struct bav_term U;
  struct ba0_mark M;

  bap__check_ordering_mpz (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bav_is_one_term (T))
    {
      if (R != A)
        bap_set_polynom_mpz (R, A);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&U);
  bav_set_term (&U, &A->total_rank);
  bav_mul_term (&U, &U, T);
  bap_begin_itermon_mpz (&iter, A);
  P = bap_new_polynom_mpz ();
  bap_begin_creator_mpz
      (&crea, P, &U, bap_exact_total_rank, bap_nbmon_polynom_mpz (A));
  while (!bap_outof_itermon_mpz (&iter))
    {
      bap_term_itermon_mpz (&U, &iter);
      bav_mul_term (&U, &U, T);
      bap_write_creator_mpz (&crea, &U, *bap_coeff_itermon_mpz (&iter));
      bap_next_itermon_mpz (&iter);
    }
  bap_close_creator_mpz (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mpz (R, P);
  ba0_restore (&M);
}

/*
 * texinfo: bap_mul_polynom_variable_mpz
 * Assign @math{A \, v^d} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_variable_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
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
  bap_mul_polynom_term_mpz (R, A, &term);
  ba0_restore (&M);
}

/* $R = A \, c\,T$.  */

/*
 * texinfo: bap_mul_polynom_monom_mpz
 * Assign @math{A \, c\, T} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_monom_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    ba0_mpz_t c,
    bav_term T)
{
  struct bap_itermon_mpz iter;
  struct bap_creator_mpz crea;
  bap_polynom_mpz P;
  struct bav_term U;
  ba0_mpz_t d;
  struct ba0_mark M;

  bap__check_ordering_mpz (A);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (ba0_mpz_is_zero (c))
    {
      bap_set_polynom_zero_mpz (R);
      return;
    }
  else if (ba0_mpz_is_one (c))
    {
      bap_mul_polynom_term_mpz (R, A, T);
      return;
    }

  ba0_push_another_stack ();
  ba0_record (&M);

  bav_init_term (&U);
  bav_set_term (&U, &A->total_rank);
  bav_mul_term (&U, &U, T);
  bap_begin_itermon_mpz (&iter, A);

  P = bap_new_polynom_mpz ();
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpq)
  bap_begin_creator_mpz
      (&crea, P, &U, bap_exact_total_rank, bap_nbmon_polynom_mpz (A));
#else
  bap_begin_creator_mpz
      (&crea, P, &U, bap_approx_total_rank, bap_nbmon_polynom_mpz (A));
#endif

  ba0_mpz_init (d);

  while (!bap_outof_itermon_mpz (&iter))
    {
      bap_term_itermon_mpz (&U, &iter);
      bav_mul_term (&U, &U, T);
      ba0_mpz_mul (d, c, *bap_coeff_itermon_mpz (&iter));
      bap_write_creator_mpz (&crea, &U, d);
      bap_next_itermon_mpz (&iter);
    }
  bap_close_creator_mpz (&crea);
  ba0_pull_stack ();
  bap_set_polynom_mpz (R, P);
  ba0_restore (&M);
}

/*****************************************************************************
 MULTIPLICATION
 *****************************************************************************/

static void
bap_mul_elem_polynom_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bap_polynom_mpz B)
{
  struct bap_creator_mpz crea;
  struct bap_itermon_mpz iterA, iterB;
  struct bap_polynom_mpz R1;
  struct bap_geobucket_mpz geo;
  ba0_mpz_t cz, *ca, *cb;
  struct bav_term TA, TB, TTB;
  enum bap_typeof_total_rank type;
  struct ba0_mark M;

  if (bap_nbmon_polynom_mpz (A) > bap_nbmon_polynom_mpz (B))
    BA0_SWAP (bap_polynom_mpz, A, B);

  type = ba0_domain_mpz ()? bap_exact_total_rank : bap_approx_total_rank;

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_mpz_init (cz);

  bav_init_term (&TTB);
  bav_set_term (&TTB, &B->total_rank);

  bav_init_term (&TA);
  bav_init_term (&TB);

  bap_init_geobucket_mpz (&geo);
  bap_init_polynom_mpz (&R1);

  bap_begin_itermon_mpz (&iterA, A);
  while (!bap_outof_itermon_mpz (&iterA))
    {
      ca = bap_coeff_itermon_mpz (&iterA);
      bap_term_itermon_mpz (&TA, &iterA);
      bav_mul_term (&TB, &TTB, &TA);
      bap_begin_creator_mpz
          (&crea, &R1, &TB, type, bap_nbmon_polynom_mpz (B));
      bap_begin_itermon_mpz (&iterB, B);
      while (!bap_outof_itermon_mpz (&iterB))
        {
          cb = bap_coeff_itermon_mpz (&iterB);
          ba0_mpz_mul (cz, *ca, *cb);
          bap_term_itermon_mpz (&TB, &iterB);
          bav_mul_term (&TB, &TB, &TA);
          bap_write_creator_mpz (&crea, &TB, cz);
          bap_next_itermon_mpz (&iterB);
        }
      bap_close_creator_mpz (&crea);
      bap_add_geobucket_mpz (&geo, &R1);
      bap_next_itermon_mpz (&iterA);
    }
  ba0_pull_stack ();
  bap_set_polynom_geobucket_mpz (R, &geo);
  ba0_restore (&M);
}

/* $R = A \, B$.  */

/*
 * texinfo: bap_mul_polynom_mpz
 * Assign @math{A\,B} to @var{R}.
 */

BAP_DLL void
bap_mul_polynom_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bap_polynom_mpz B)
{
  struct bap_itercoeff_mpz iterA, iterB;
  struct bap_itermon_mpz iter;
  struct bap_creator_mpz crea;
  struct bap_polynom_mpz C, CA, CB;
  bap_polynom_mpz AA, BB, P;
  struct bav_term T, U, TA, TB;
  bav_variable xa, xb, v;
  bav_Iordering r;
  ba0_int_p i;
  struct ba0_mark M;

  bap__check_compatible_mpz (A, B);
  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_is_numeric_polynom_mpz (B))
    BA0_SWAP (bap_polynom_mpz, A, B);
/*
   Si l'un des deux polynomes est constant, A est constant
*/
  if (bap_is_numeric_polynom_mpz (A))
    {
      if (bap_is_zero_polynom_mpz (A) || bap_is_zero_polynom_mpz (B))
        bap_set_polynom_zero_mpz (R);
      else
        {
          ba0_mpz_t c;            /* Sinon bug quand A == R */
          ba0_push_another_stack ();
          ba0_record (&M);
          ba0_mpz_init_set (c, *bap_numeric_initial_polynom_mpz (A));
          ba0_pull_stack ();
          bap_mul_polynom_numeric_mpz (R, B, c);
          ba0_restore (&M);
        }
      return;
    }

  if (bap_nbmon_polynom_mpz (B) == 1)
    {
      BA0_SWAP (bap_polynom_mpz, A, B);
    }
/*
   Si l'un des deux polynomes est reduit a un monome alors A l'est.
   Optimisation mais non necessaire.
*/
  if (bap_nbmon_polynom_mpz (A) == 1)
    {
      ba0_mpz_t c;

      ba0_push_another_stack ();
      ba0_record (&M);
      bap_begin_itermon_mpz (&iter, A);
      bav_init_term (&T);
      bap_term_itermon_mpz (&T, &iter);
      ba0_mpz_init_set (c, *bap_coeff_itermon_mpz (&iter));
      ba0_pull_stack ();
      bap_mul_polynom_monom_mpz (R, B, c, &T);
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
      BA0_SWAP (bap_polynom_mpz, A, B);
      BA0_SWAP (bav_variable, xa, xb);
    }
/*
   Exit le cas de deux polynomes sur le meme alphabet
*/
  if (xa == BAV_NOT_A_VARIABLE)
    {
      bav_R_pull_ordering ();
      bav_R_free_ordering (r);
      bap_mul_elem_polynom_mpz (R, A, B);
      return;
    }
/*
   A depend de variables non communes avec B
*/
  ba0_push_another_stack ();
  ba0_record (&M);

  {
    bap_polynom_mpz AA0 = bap_new_readonly_polynom_mpz ();
    bap_sort_polynom_mpz (AA0, A);
    AA = bap_new_polynom_mpz ();
    bap_set_polynom_mpz (AA, AA0);
  }

  bap_begin_itercoeff_mpz (&iterA, AA, xa);

  if (xb != BAV_NOT_A_VARIABLE)
    {
      bap_polynom_mpz BB0 = bap_new_readonly_polynom_mpz ();
      bap_sort_polynom_mpz (BB0, B);
      BB = bap_new_polynom_mpz ();
      bap_set_polynom_mpz (BB, BB0);
    }
  else
    BB = B;

  bap_init_polynom_mpz (&C);
  bap_init_polynom_mpz (&CA);
  bap_init_polynom_mpz (&CB);
  bav_init_term (&T);
  bav_init_term (&TA);
  bav_init_term (&TB);
  bav_init_term (&U);

  bav_mul_term (&T, &AA->total_rank, &BB->total_rank);
  i = BA0_MAX (bap_nbmon_polynom_mpz (AA), bap_nbmon_polynom_mpz (BB));
/*
 * Note: the monomials of P will temporarily not be sorted
 */
  P = bap_new_polynom_mpz ();
#if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpq)
  bap_begin_creator_mpz (&crea, P, &T, bap_exact_total_rank, i);
#else
  bap_begin_creator_mpz (&crea, P, &T, bap_approx_total_rank, i);
#endif

  while (!bap_outof_itercoeff_mpz (&iterA))
    {
      bap_coeff_itercoeff_mpz (&CA, &iterA);
      bap_term_itercoeff_mpz (&TA, &iterA);
      bap_begin_itercoeff_mpz
          (&iterB, BB, xb == BAV_NOT_A_VARIABLE ? xa : xb);
      while (!bap_outof_itercoeff_mpz (&iterB))
        {
          bap_coeff_itercoeff_mpz (&CB, &iterB);
          bap_term_itercoeff_mpz (&TB, &iterB);

          bav_mul_term (&T, &TA, &TB);
          bap_mul_elem_polynom_mpz (&C, &CA, &CB);

          bap_begin_itermon_mpz (&iter, &C);
          while (!bap_outof_itermon_mpz (&iter))
            {
              ba0_mpz_t *c;

              c = bap_coeff_itermon_mpz (&iter);
              bap_term_itermon_mpz (&U, &iter);
              bav_mul_term (&U, &U, &T);
              bap_write_creator_mpz (&crea, &U, *c);
              bap_next_itermon_mpz (&iter);
            }
          bap_next_itercoeff_mpz (&iterB);
        }
      bap_next_itercoeff_mpz (&iterA);
    }
  bap_close_creator_mpz (&crea);
  bav_R_pull_ordering ();
/*
 * Now, the monomials get sorted
 */
  bap_physort_polynom_mpz (P);

  bav_R_free_ordering (r);
  ba0_pull_stack ();

  i = BA0_MAX (bap_nbmon_polynom_mpz (A), bap_nbmon_polynom_mpz (B));

  bap_set_polynom_mpz (R, P);

  ba0_restore (&M);
}

/* $R = A^n$.  */

/*
 * texinfo: bap_pow_polynom_mpz
 * Assign @math{A^d} to @var{R}.
 */

BAP_DLL void
bap_pow_polynom_mpz (
    bap_polynom_mpz R,
    bap_polynom_mpz A,
    bav_Idegree n)
{
  struct bap_polynom_mpz E, F;
  bav_Idegree p;
  bool E_vaut_un;
  struct ba0_mark M;

  if (n == 0)
    bap_set_polynom_one_mpz (R);
  else if (n == 1)
    {
      if (R != A)
        bap_set_polynom_mpz (R, A);
    }
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      if (n % 2 == 1)
        {
          bap_init_polynom_mpz (&E);
          bap_set_polynom_mpz (&E, A);
          E_vaut_un = false;
        }
      else
        E_vaut_un = true;

      bap_init_polynom_mpz (&F);
      bap_mul_polynom_mpz (&F, A, A);

      for (p = n / 2; p != 1; p /= 2)
        {
          if (p % 2 == 1)
            {
              if (E_vaut_un)
                {
                  bap_init_polynom_mpz (&E);
                  bap_set_polynom_mpz (&E, &F);
                  E_vaut_un = false;
                }
              else
                bap_mul_polynom_mpz (&E, &F, &E);
            }
          bap_mul_polynom_mpz (&F, &F, &F);
        }
      ba0_pull_stack ();
      if (E_vaut_un)
        bap_set_polynom_mpz (R, &F);
      else
        bap_mul_polynom_mpz (R, &E, &F);
      ba0_restore (&M);
    }
}

#undef BAD_FLAG_mpz
