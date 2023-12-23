#ifndef BAD_SPLITTING_CONTROL_H
#   define BAD_SPLITTING_CONTROL_H 1

#   include "bad_common.h"
#   include "bad_attchain.h"

BEGIN_C_DECLS

/*
 * texinfo: bad_typeof_dimension_lower_bound
 * This data type permits to specify to differential elimination
 * algorithms the type of dimension lower bound to be applied.
 * Such a lower bound permits to cut any branch of the splitting
 * tree leading to regular chains of differential dimension
 * strictly less than the number of input equations.
 * Note that such a strategy is proved in the algebraic case
 * and in the case of a single differential equation.
 * The other cases are conjectural.
 */

enum bad_typeof_dimension_lower_bound
{
// do not take into account any dimension lower bound
  bad_no_dimension_lower_bound,
// apply it in the case of a non-differential system
  bad_algebraic_dimension_lower_bound,
// apply it in the case of an ordinary differential system
  bad_ode_dimension_lower_bound,
// apply it in the case of a partial differential system
  bad_pde_dimension_lower_bound
};

/* 
 * texinfo: bad_splitting_control
 * This data type permits to specify a splitting control strategy
 * to differential elimination algorithms.
 */

struct bad_splitting_control
{
// Stop at the first consistent regular chain (if any)
  bool first_leaf_only;
// Should a dimension lower bound be taken into account ?
  enum bad_typeof_dimension_lower_bound dimlb;
// Assuming dimlb is different than bad_no_dimension_lower_bound,
// cut branches leading to regular chains of differential 
// dimension strictly less than the number of input equations
// provided that the number of input equations is one.
  bool apply_dimlb_one_eq;
};

#   if defined (BA0_OLDDEF)
typedef struct bad_splitting_control *bad_splitting_control;
#   endif

extern BAD_DLL void bad_init_splitting_control (
    struct bad_splitting_control *);

extern BAD_DLL struct bad_splitting_control *bad_new_splitting_control (
    void);

extern BAD_DLL void bad_set_splitting_control (
    struct bad_splitting_control *,
    struct bad_splitting_control *);

extern BAD_DLL void bad_set_first_leaf_only_splitting_control (
    struct bad_splitting_control *,
    bool);

extern BAD_DLL void bad_set_dimension_lower_bound_splitting_control (
    struct bad_splitting_control *,
    enum bad_typeof_dimension_lower_bound,
    bool);

extern BAD_DLL bool bad_apply_dimension_lower_bound_splitting_control (
    struct bad_splitting_control *,
    struct bap_listof_polynom_mpz *,
    struct bad_attchain *);

END_C_DECLS
#endif /* !BAD_SPLITTING_CONTROL_H */
