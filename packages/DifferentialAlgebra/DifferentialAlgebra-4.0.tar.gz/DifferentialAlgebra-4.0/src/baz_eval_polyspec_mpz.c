#include "baz_eval_polyspec_mpz.h"

/*
 * texinfo: baz_eval_polynom_point_interval_mpq_mpz
 * Evaluate @var{A} at @var{point}.
 * Result in @var{res}.
 * All the variables of @var{A} must be assigned a value a value.
 */

BAZ_DLL void
baz_eval_polynom_point_interval_mpq_mpz (
    ba0_interval_mpq res,
    bap_polynom_mpz A,
    bav_point_interval_mpq point)
{
  struct bap_itermon_mpz iter;
  struct bav_term T;
  struct ba0_interval_mpq X, S;
  struct ba0_mark M;
  ba0_mpq_t q;


  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_interval_mpq (&S);
  ba0_init_interval_mpq (&X);
  bav_init_term (&T);
  ba0_mpq_init (q);
  ba0_set_interval_mpq_si (&S, 0);
  bap_begin_itermon_mpz (&iter, A);
  while (!bap_outof_itermon_mpz (&iter))
    {
      bap_term_itermon_mpz (&T, &iter);
      bav_term_at_point_interval_mpq (&X, &T, point);
      ba0_mpz_set (ba0_mpq_numref (q), *bap_coeff_itermon_mpz (&iter));
      ba0_mul_interval_mpq_mpq (&X, &X, q);
      ba0_add_interval_mpq (&S, &S, &X);
      bap_next_itermon_mpz (&iter);
    }

  ba0_pull_stack ();
  ba0_set_interval_mpq (res, &S);
  ba0_restore (&M);
}
