#include "bmi_exported.h"
#include "bmi_mesgerr.h"
#include "bmi_indices.h"
#include "bmi_differential_ring.h"


/**********************************************************************
 * DIFFERENTIAL RING
 **********************************************************************/

/*
 * EXPORTED
 * DifferentialRing 
 * DifferentialRing (derivations, blocks, parameters)
 *     ordering (derivations, blocks) must be valid
 *     parameters must be a list of dependent symbols.
 * Returns the ordering.
 */

ALGEB
bmi_differential_ring (
    struct bmi_callback *callback)
{
  char *derivations, *blocks, *parameters;
  bav_Iordering r;
  struct bav_tableof_parameter T;
  ba0_int_p i, j, k;

  bmi_check_blad_gmp_allocators (__FILE__, __LINE__);

  if (bmi_nops (callback) != 3)
    BA0_RAISE_EXCEPTION (BMI_ERRNOPS);

  bmi_check_blad_gmp_allocators (__FILE__, __LINE__);

  derivations = bmi_string_op (1, callback);
  blocks = bmi_string_op (2, callback);
  parameters = bmi_string_op (3, callback);

  bmi_check_blad_gmp_allocators (__FILE__, __LINE__);

  ba0_scanf_printf
      ("%ordering", "ranking (derivations = %s, blocks = %s)",
      &r, derivations, blocks);
  if (bav_R_ambiguous_symbols ())
    BA0_RAISE_EXCEPTION (BAV_ERRPAO);
  bmi_check_blad_gmp_allocators (__FILE__, __LINE__);

/*
 * Sets the ordering but does not set bav_global.parameters
 */
  bav_R_push_ordering (r);
/*
 * Checks the consistency of the parameters list
 * A parameter must have the form: dep var(non duplicated indep vars)
 */
  bmi_check_blad_gmp_allocators (__FILE__, __LINE__);

  ba0_init_table ((ba0_table) & T);
  ba0_sscanf2 (parameters, "%t[%param]", &T);
  for (i = 0; i < T.size; i++)
    {
      if (T.tab[i]->root->type != bav_dependent_symbol)
        BA0_RAISE_EXCEPTION (BMI_ERRPARS);
      for (j = 0; j < T.tab[i]->dep.size; j++)
        {
          if (T.tab[i]->dep.tab[j]->type != bav_independent_symbol)
            BA0_RAISE_EXCEPTION (BMI_ERRPARS);
          for (k = 0; k < j; k++)
            if (T.tab[i]->dep.tab[j] == T.tab[i]->dep.tab[k])
              BA0_RAISE_EXCEPTION (BMI_ERRPARS);
        }
    }
  bav_set_parameters (&bav_global.parameters, &T);

  {
    ALGEB res;
    res = bmi_rtable_differential_ring (callback->kv, __FILE__, __LINE__);
#if defined (BMI_BALSA)
/*
 * In BALSA, we return the whole table, not the mere rtable !
 */
    res = bmi_balsa_new_differential_ring (res);
#endif
    return res;
  }
}
