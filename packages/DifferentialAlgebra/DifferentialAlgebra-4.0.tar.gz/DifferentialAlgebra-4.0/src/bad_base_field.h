#ifndef BAD_BASE_FIELD_H
#   define BAD_BASE_FIELD_H 1

#   include "bad_common.h"
#   include "bad_regchain.h"

BEGIN_C_DECLS

/*
 * texinfo: bad_base_field
 * This data structure implements base fields for polynomials, regular
 * chains and so on.
 * Base fields may be presented by generators and relations.
 * The base field generators, which are encoded by variables, must lie
 * at the bottom of the ordering, and be eliminated by the other variables.
 * Moreover, if @var{C} is a regular chain whose elements have coefficients
 * in a base field @var{K} then the defining equations of @var{K}
 * must appear among the polynomials of @var{C}.
 */

struct bad_base_field
{
// Indicate if the base field is differential or not
  bool differential;
// Indicate if the base field equations form an autoreduced set.
// If so, some computations are faster. Default value is false.
  bool assume_reduced;
// The highest variable among the base field generators
  struct bav_variable *varmax;
// The base field defining equations.
// The corresponding ideal must be prime.
  struct bad_regchain relations;
};

#   if defined (BA0_OLDDEF)
typedef struct bad_base_field *bad_base_field;
#   endif

extern BAD_DLL void bad_init_base_field (
    struct bad_base_field *);

extern BAD_DLL struct bad_base_field *bad_new_base_field (
    void);

extern BAD_DLL void bad_set_base_field (
    struct bad_base_field *,
    struct bad_base_field *);

extern BAD_DLL void bad_force_algebraic_base_field (
    struct bad_base_field *);

extern BAD_DLL void bad_base_field_generators (
    struct bav_tableof_variable *,
    struct bad_base_field *);

extern BAD_DLL void bad_move_base_field_generator (
    struct bad_base_field *,
    struct bav_variable *);

extern BAD_DLL void bad_set_base_field_generators_and_relations (
    struct bad_base_field *,
    struct bav_tableof_variable *,
    struct bad_regchain *,
    struct bav_tableof_parameter *,
    bool,
    bool);

extern BAD_DLL void bad_base_field_implicit_generators (
    struct bav_tableof_variable *,
    struct bad_base_field *,
    struct bav_tableof_variable *,
    struct bad_regchain *);

extern BAD_DLL bool bad_is_a_compatible_base_field (
    struct bad_base_field *,
    struct bad_attchain *);

extern BAD_DLL bool bad_member_variable_base_field (
    struct bav_variable *,
    struct bad_base_field *);

extern BAD_DLL bool bad_member_nonzero_polynom_base_field (
    struct bap_polynom_mpz *,
    struct bad_base_field *);

extern BAD_DLL bool bad_member_polynom_base_field (
    struct bap_polynom_mpz *,
    struct bad_base_field *);

extern BAD_DLL ba0_scanf_function bad_scanf_base_field;

extern BAD_DLL ba0_printf_function bad_printf_base_field;

END_C_DECLS
#endif /* ! BAD_BASE_FIELD_H */
