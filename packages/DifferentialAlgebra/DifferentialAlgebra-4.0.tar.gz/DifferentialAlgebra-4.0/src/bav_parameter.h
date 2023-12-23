#ifndef BAV_PARAMETER_H
#   define BAV_PARAMETER_H 1

#   include "bav_symbol.h"

BEGIN_C_DECLS

/*
 * texinfo: bav_parameter
 * A parameter is a variable some derivatives of which are zero.
 * The derivations / independent variables the parameter depends on
 * are listed in the field @code{dep}. The order of these derivations
 * in the table is followed when parsing and printing the parameter.
 * If the @code{dep} field is empty, all the derivatives of the
 * parameter are zero.
 * Parameters are stored in the global variable @code{bav_global.parameters}.
 * Defining parameters has side effects on some input / output notations
 * such as @code{diff} and on the behaviour of the differentiation
 * functions of the @code{bap} and @code{bad} libraries.
 */

struct bav_parameter
{
// the symbol at the root of the variable
  struct bav_symbol *root;
// the table of independent symbols the parameter depends on
  struct bav_tableof_symbol dep;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_parameter *bav_parameter;
#   endif

struct bav_tableof_parameter
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_parameter **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_parameter *bav_tableof_parameter;
#   endif

extern BAV_DLL void bav_init_parameters (
    struct bav_tableof_parameter *);

extern BAV_DLL struct bav_tableof_parameter *bav_new_parameters (
    void);

extern BAV_DLL void bav_reset_parameters (
    struct bav_tableof_parameter *);

extern BAV_DLL unsigned ba0_int_p bav_sizeof_parameters (
    struct bav_tableof_parameter *);

extern BAV_DLL void bav_set_parameters (
    struct bav_tableof_parameter *,
    struct bav_tableof_parameter *);

struct bav_differential_ring;

extern BAV_DLL void bav_switch_ring_parameters (
    struct bav_tableof_parameter *,
    struct bav_differential_ring *);

extern BAV_DLL void bav_init_parameter (
    struct bav_parameter *);

extern BAV_DLL struct bav_parameter *bav_new_parameter (
    void);

extern BAV_DLL void bav_set_parameter (
    struct bav_parameter *,
    struct bav_parameter *);

extern BAV_DLL void bav_set_parameter_symbol_table (
    struct bav_parameter *,
    struct bav_symbol *,
    struct bav_tableof_symbol *);

extern BAV_DLL bool bav_is_a_parameter (
    struct bav_symbol *,
    ba0_int_p *,
    struct bav_tableof_parameter *);

struct bav_variable;

extern BAV_DLL bool bav_is_zero_derivative_of_parameter (
    struct bav_variable *,
    struct bav_tableof_parameter *);

struct bav_tableof_variable;

extern BAV_DLL void bav_zero_derivatives_of_parameter (
    struct bav_tableof_variable *,
    struct bav_parameter *);

extern BAV_DLL void bav_zero_derivatives_of_tableof_parameter (
    struct bav_tableof_variable *,
    struct bav_tableof_parameter *);

extern BAV_DLL ba0_scanf_function bav_scanf_parameter;

extern BAV_DLL ba0_printf_function bav_printf_parameter;

END_C_DECLS
#endif /* ! BAV_PARAMETER_H */
