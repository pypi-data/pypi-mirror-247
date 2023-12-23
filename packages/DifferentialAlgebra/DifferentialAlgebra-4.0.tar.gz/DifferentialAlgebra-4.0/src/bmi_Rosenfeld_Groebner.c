#include "bmi_exported.h"
#include "bmi_mesgerr.h"
#include "bmi_indices.h"
#include "bmi_Rosenfeld_Groebner.h"
#include "bmi_base_field_generators.h"

/*
 * EXPORTED
 * RosenfeldGroebner (equations, inequations, 
 * 			generators, relations, 
 * 			properties, differential ring, 
 * 			singsol,
 * 			dimlb,
 * 			called from RosenfeldGroebner)
 *
 * equations and inequations are lists of differential polynomials
 * generators, relations are for the base field
 * properties are lists of attributes
 * differential ring is a table
 * singsol is a string, which controls splittings.
 *     Values = "all", "none", "essential"
 * dimlb is a string, which controls splittings by means of the
 *     dimension lower bound of the components. 
 *     Values = "nocase", "safecase", "odecase", "pdecase"
 * called from RosenfeldGroebner is a bool. If true, the call comes from
 *     RosenfeldGroebner else, it comes from EssentialComponents.
 */

ALGEB
bmi_Rosenfeld_Groebner (
    struct bmi_callback *callback)
{
  struct bad_splitting_control control;
  struct bad_base_field K;
  struct bad_intersectof_regchain T;
  struct bad_regchain C;
  struct bap_tableof_polynom_mpz eqns, ineqs, nulles;
  struct bav_tableof_variable G;
  ba0_int_p i;
  char *equations;
  char *inequations;
  char *generators;
  char *relations;
  char *properties;
  char *singsol;
  char *dimlb;
  bool called_from_RG;

#define RG_DEBUG 1
#undef RG_DEBUG
#if defined (RG_DEBUG)
  ba0_printf ("entering bmi_Rosenfeld_Groebner\n");
#endif

  if (bmi_nops (callback) != 9)
    BA0_RAISE_EXCEPTION (BMI_ERRNOPS);
  if (!bmi_is_table_op (6, callback))
    BA0_RAISE_EXCEPTION (BMI_ERRDRNG);

  bmi_set_ordering (6, callback, __FILE__, __LINE__);

  equations = bmi_string_op (1, callback);
  inequations = bmi_string_op (2, callback);
  generators = bmi_string_op (3, callback);
  relations = bmi_string_op (4, callback);
  properties = bmi_string_op (5, callback);
  singsol = bmi_string_op (7, callback);
  dimlb = bmi_string_op (8, callback);
  called_from_RG = bmi_bool_op (9, callback);

#if defined (RG_DEBUG)
  ba0_printf ("before equations and inequations\n");
#endif
/*
 * The equations and inequations
 */
  ba0_init_table ((ba0_table) & eqns);
  ba0_init_table ((ba0_table) & ineqs);
#if ! defined (BMI_BALSA)
  ba0_sscanf2 (equations, "%t[%careful_expanded_Az]", &eqns);
  ba0_sscanf2 (inequations, "%t[%careful_expanded_Az]", &ineqs);
#else
  ba0_sscanf2 (equations, "%t[%Az]", &eqns);
  ba0_sscanf2 (inequations, "%t[%Az]", &ineqs);
#endif
/*
 * When called_from_RG is false, the call comes from EssentialComponents. 
 *
 * Then singsol = "essential"
 * 
 * If the call comes from EssentialComponents and the conditions for
 * applying the Low Power Theorem are not met, then an error is raised.
 *
 * If the call comes from RosenfeldGroebner and the conditions for
 * applying the Low Power Theorem are not met, then the option is
 * just ignored. This permits to set systematically this option when
 * calling RosenfeldGroebner.
 */
#if defined (RG_DEBUG)
  ba0_printf ("before BMI_ERRLPT\n");
#endif
  if ((!called_from_RG) && (eqns.size != 1 || ineqs.size != 0))
    BA0_RAISE_EXCEPTION (BMI_ERRLPT);
/*
 * Zero derivatives of all parameters are appended to the equations.
 * Do not try to avoid redundancies.
 */
  ba0_init_table ((ba0_table) & nulles);
  bap_zero_derivatives_of_tableof_parameter_mpz (&nulles,
      &bav_global.parameters);
  ba0_concat_table ((ba0_table) & eqns, (ba0_table) & eqns,
      (ba0_table) & nulles);
/*
 * Initialize the intersection
 * Sets the automatic properties
 */
  bad_init_intersectof_regchain (&T);
  ba0_scanf_printf ("%intersectof_regchain",
      "intersectof_regchain ([], %s)", &T, properties);
  bad_set_automatic_properties_attchain (&T.attrib);
/*
 * Process the base field.
 * generators  = generators of the base field
 * relations = a regular chain (in printed form) or an empty string.
 *
 * If the elimination is differential then, for each parameter present 
 * in generators, the equations which state that its derivatives are zero 
 * are put in relations.
 */
#if defined (RG_DEBUG)
  ba0_printf ("before processing the base field\n");
  ba0_printf ("generators = %s\n", generators);
  ba0_printf ("relations = %s\n", relations);
#endif
  ba0_init_table ((ba0_table) & G);
  bmi_scanf_generators (&G, generators);

  bad_init_regchain (&C);
  ba0_sscanf2 (relations, "%pretend_regchain", &C);
/*
 * The differential prop. is important for the base field compatibility test.
 * It would not be present if the user had not specified any relations.
 */
  if (bad_has_property_attchain (&T.attrib, bad_differential_ideal_property))
    {
      if (C.decision_system.size == 0)
        bad_set_property_attchain (&C.attrib, bad_differential_ideal_property);
    }

  bad_init_base_field (&K);
  bad_set_base_field_generators_and_relations
      (&K, &G, &C, &bav_global.parameters, false, false);
  bmi_forbid_base_field_implicit_generators (&K, &G, &C);
/*
 * Splitting control
 */
#if defined (RG_DEBUG)
  ba0_printf ("before processing the splitting control\n");
#endif
  bad_init_splitting_control (&control);
  if (strcmp (singsol, BMI_IX_none) == 0)
#define BEFORE_RG_3_8
#undef BEFORE_RG_3_8
#if defined (BEFORE_RG_3_8)
    bad_set_first_branch_only_splitting_control (&control, true);
#else
    bad_set_first_leaf_only_splitting_control (&control, true);
#endif

  if (strcmp (dimlb, BMI_IX_nocase) == 0)
    bad_set_dimension_lower_bound_splitting_control
        (&control, bad_no_dimension_lower_bound, false);
  else if (strcmp (dimlb, BMI_IX_safecase) == 0)
    bad_set_dimension_lower_bound_splitting_control
        (&control, bad_algebraic_dimension_lower_bound, true);
  else if (strcmp (dimlb, BMI_IX_odecase) == 0)
    bad_set_dimension_lower_bound_splitting_control
        (&control, bad_ode_dimension_lower_bound, true);
  else
    bad_set_dimension_lower_bound_splitting_control
        (&control, bad_pde_dimension_lower_bound, true);
/*
 * Call to RosenfeldGroebner
    bad_set_settings_reduction (0, bad_probabilistic_redzero_strategy, 0);
 */
#if defined (DEBUG)
  ba0_printf ("before bad_Rosenfeld_Groebner\n");
  ba0_printf ("T = %intersectof_regchain\n", &T);
  ba0_printf ("eqns = %t[%Az]\n", &eqns);
  ba0_printf ("ineqs = %t[%Az]\n", &ineqs);
  ba0_printf ("K = %base_field\n", &K);
#endif
  bad_Rosenfeld_Groebner (&T, &eqns, &ineqs, &K, &control);
/*
 * The redundancy processing.
 * The Low Power Theorem processing
 */
  if (strcmp (singsol, BMI_IX_essential) == 0)
    {
      if (T.inter.size > 0 &&
          T.inter.tab[0]->decision_system.size ==
          K.relations.decision_system.size + 1)
        bad_low_power_theorem_simplify_intersectof_regchain (&T, &T, &K);
      else if (called_from_RG)
#if defined (BEFORE_RG_3_8)
        bad_remove_redundant_components_intersectof_regchain (&T, &T);
#else
        bad_remove_redundant_components_intersectof_regchain (&T, &T, &K);
#endif
      else
        BA0_RAISE_EXCEPTION (BMI_ERRLPT);
    }
  else
    {
      bad_set_settings_reduction (0, bad_probabilistic_redzero_strategy, 0);
#if defined (BEFORE_RG_3_8)
      bad_remove_redundant_components_intersectof_regchain (&T, &T);
#else
      bad_remove_redundant_components_intersectof_regchain (&T, &T, &K);
#endif

    }
/*
 * The result
 */
  {
    ALGEB L, cell;

    bmi_push_maple_gmp_allocators ();
    L = MapleListAlloc (callback->kv, T.inter.size);
    MapleGcProtect (callback->kv, L);
    for (i = 0; i < T.inter.size; i++)
      {
        bmi_pull_maple_gmp_allocators ();
        cell = bmi_rtable_regchain
            (callback->kv, T.inter.tab[i], __FILE__, __LINE__);
#if defined (BMI_BALSA)
/*
 * In BALSA, one computes the whole table, not just the rtable
 */
        cell = bmi_balsa_new_regchain (cell);
#endif
        bmi_push_maple_gmp_allocators ();
        MapleListAssign (callback->kv, L, i + 1, cell);
      }
    MapleGcAllow (callback->kv, L);
    bmi_pull_maple_gmp_allocators ();

    return L;
  }
}
