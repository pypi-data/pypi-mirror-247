#include "bmi_blad_eval.h"
#include "bmi_exported.h"
#include "bmi_mesgerr.h"
#include "bmi_indices.h"
#include "bmi_base_field_generators.h"

/*
 * BaseFieldGenerators (generators, relations, regchain | ring)
 */

ALGEB
bmi_base_field_generators (
    struct bmi_callback *callback)
{
  struct bad_base_field K;
  struct bad_regchain C, R;
  struct bav_tableof_variable T, G;
  struct bav_tableof_parameter P;
  ba0_int_p i, k;
  char *generators, *relations;
  bool differential;

  if (bmi_nops (callback) != 3)
    BA0_RAISE_EXCEPTION (BMI_ERRNOPS);
  else if (!bmi_is_table_op (3, callback))
    BA0_RAISE_EXCEPTION (BMI_ERRDRNG);

  if (bmi_is_regchain_op (3, callback))
    bmi_set_ordering_and_regchain (&R, 3, callback, __FILE__, __LINE__);
  else
    bmi_set_ordering (3, callback, __FILE__, __LINE__);

  differential = bav_global.R.ders.size > 0;
  generators = bmi_string_op (1, callback);
  relations = bmi_string_op (2, callback);

  ba0_init_table ((ba0_table) & G);
  bmi_scanf_generators (&G, generators);
/*
 * Remove the independent variables, which will raise an exception in BLAD
 * and belong to the base field anyway.
 */
  i = 0;
  while (i < G.size)
    {
      if (bav_symbol_type_variable (G.tab[i]) == bav_independent_symbol)
        ba0_delete_table ((ba0_table) & G, i);
      else
        i += 1;
    }

  bad_init_regchain (&C);
  ba0_sscanf2 (relations, "%pretend_regchain", &C);
/*
 * In the differential case, one assigns to P the generators of G
 * which are parameters. 
 */
  ba0_init_table ((ba0_table) & P);
  if (differential)
    {
      if (C.decision_system.size == 0)
        bad_set_property_attchain (&C.attrib, bad_differential_ideal_property);
      ba0_realloc_table ((ba0_table) & P, bav_global.parameters.size);
      for (i = 0; i < G.size; i++)
        {
          if (bav_is_a_parameter (G.tab[i]->root, &k, &bav_global.parameters))
            {
              P.tab[P.size] = bav_global.parameters.tab[k];
              P.size += 1;
            }
        }
    }
/*
 * Define the base field, then, get its list of generators
 */
  bad_init_base_field (&K);
  bad_set_base_field_generators_and_relations (&K, &G, &C, &P, false, false);
  bmi_forbid_base_field_implicit_generators (&K, &G, &C);
  ba0_init_table ((ba0_table) & T);
  bad_base_field_generators (&T, &K);
#if ! defined (BMI_BALSA)
/* 
 * MAPLE only. Perhaps this should be changed.
 *
 * Append the list of independent variables, which are omitted by
 * bad_base_field_generators.
 */
  ba0_realloc_table ((ba0_table) & T, T.size + bav_global.R.ders.size);
  for (i = 0; i < bav_global.R.ders.size; i++)
    {
      T.tab[T.size] = bav_global.R.vars.tab[bav_global.R.ders.tab[i]];
      T.size += 1;
    }
#endif
  {
    char *stres;
    ALGEB res;
#if ! defined (BMI_BALSA)
    bav_set_settings_symbol (0, &bav_printf_numbered_symbol);
#endif
    stres = ba0_new_printf ("%t[%v]", &T);
    bmi_push_maple_gmp_allocators ();
#if ! defined (BMI_BALSA)
    res = EvalMapleStatement (callback->kv, stres);
#else
    res = bmi_balsa_new_string (stres);
#endif
    bmi_pull_maple_gmp_allocators ();
    return res;
  }
}

/*
 * This function tests if some base field generators are not explicitly given.
 * In this case, an error is raised.
 *
 * Called by bmi_Rosenfeld_Groebner, bmi_base_field_generators,
 * 		bmi_field_element.
 */

void
bmi_forbid_base_field_implicit_generators (
    bad_base_field K,
    bav_tableof_variable generators,
    bad_regchain relations)
{
  struct bav_tableof_variable X;
  struct ba0_mark M;
  static char mesgerr[BMI_BUFSIZE];

  ba0_record (&M);
  ba0_init_table ((ba0_table) & X);
  bad_base_field_implicit_generators (&X, K, generators, relations);
  if (X.size > 0)
    {
      ba0_sprintf (mesgerr,
          "The following symbols should be listed among the base field generators: %t[%v]",
          &X);
      BA0_RAISE_EXCEPTION (mesgerr);
    }
  ba0_restore (&M);
}

/*
 * In principle, ba0_sscanf2 (s, "%t[%v]", T)
 *
 * If this fails, tries ba0_sscanf2 (s, "%t[%y]", T)
 */

void
bmi_scanf_generators (
    bav_tableof_variable T,
    char *s)
{
  struct bav_tableof_symbol Tsym;
  ba0_int_p i;

  BA0_TRY
  {
    ba0_sscanf2 (s, "%t[%v]", T);
/*
 * With "%t[%v]", it works !
 */
  }
  BA0_CATCH
  {
/*
 * With "%t[%v]", it did not work !
 */
    BA0_TRY
    {
      ba0_init_table ((ba0_table) & Tsym);
      ba0_sscanf2 (s, "%t[%y]", &Tsym);
/*
 * With "%t[%y]", it works !
 */
      ba0_init_table ((ba0_table) T);
      ba0_realloc_table ((ba0_table) T, Tsym.size);
      for (i = 0; i < Tsym.size; i++)
        {
          T->tab[T->size] = bav_R_symbol_to_variable (Tsym.tab[i]);
          T->size += 1;
        }
    }
    BA0_CATCH
    {
/*
 * Nothing works. Restart with "%t[%v]", to get the right error message.
 */
      ba0_init_table ((ba0_table) T);
      ba0_sscanf2 (s, "%t[%v]", T);
    }
    BA0_ENDTRY;
  }
  BA0_ENDTRY;
}
