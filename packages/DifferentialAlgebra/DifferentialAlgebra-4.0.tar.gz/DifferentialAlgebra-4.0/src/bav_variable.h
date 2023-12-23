#ifndef BAV_VARIABLE_H
#   define BAV_VARIABLE_H 1

#   include "bav_common.h"
#   include "bav_symbol.h"

BEGIN_C_DECLS

struct bav_variable;

struct bav_tableof_variable
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_variable **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_variable *bav_tableof_variable;
#   endif

struct bav_tableof_tableof_variable
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_tableof_variable **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_tableof_variable *bav_tableof_tableof_variable;
#   endif

/*
 * texinfo: bav_variable
 * In most cases, a variable is a derivation or a derivative of a differential
 * indeterminate.
 * Variables are allocated in @code{ba0_global.stack.quiet}.
 * They are not duplicated. 
 * They are stored in the array @code{bav_global.R.vars}.
 * For each ordering, the numbers of all variables w.r.t. this ordering
 * are computed: the greater the number, the greater the variable, w.r.t.
 * the ordering. Numbers can change when new variables are created
 * (by differentiation of existing variables).
 */

struct bav_variable
{
  struct bav_symbol *root;      // the symbol at the root of the variable
  ba0_int_p hack;               // used locally
  ba0_int_p index;              // the index in bav_global.R.vars
  struct bav_tableof_Inumber number;    // the numbers w.r.t each ordering
  struct bav_tableof_Iorder order;      // the orders w.r.t. each derivation
  struct bav_tableof_variable derivative;       // the derivatives w.r.t. each der.
};

#   if defined (BA0_OLDDEF)
typedef struct bav_variable *bav_variable;
#   endif

#   define BAV_NOT_A_VARIABLE	BA0_NOT_A_VARIABLE
#   define BAV_TEMP_STRING		"_"
#   define BAV_JET0_STRING      "0"

struct bav_term;

struct bav_tableof_parameter;

extern BAV_DLL void bav_set_settings_variable (
    ba0_scanf_function *,
    ba0_printf_function *,
    char *,
    char *);

extern BAV_DLL void bav_get_settings_variable (
    ba0_scanf_function **,
    ba0_printf_function **,
    char **,
    char **);

extern BAV_DLL struct bav_variable *bav_new_variable (
    void);

extern BAV_DLL struct bav_variable *bav_not_a_variable (
    void);

extern BAV_DLL bav_Iorder bav_order_variable (
    struct bav_variable *,
    struct bav_symbol *);

extern BAV_DLL bav_Iorder bav_total_order_variable (
    struct bav_variable *);

extern BAV_DLL bool bav_is_constant_variable (
    struct bav_variable *,
    struct bav_symbol *,
    struct bav_tableof_parameter *);

extern BAV_DLL struct bav_variable *bav_diff_variable (
    struct bav_variable *,
    struct bav_symbol *);

extern BAV_DLL struct bav_variable *bav_diff2_variable (
    struct bav_variable *,
    struct bav_term *);

extern BAV_DLL struct bav_variable *bav_int_variable (
    struct bav_variable *,
    struct bav_symbol *);

extern BAV_DLL enum bav_typeof_symbol bav_symbol_type_variable (
    struct bav_variable *);

extern BAV_DLL struct bav_variable *bav_order_zero_variable (
    struct bav_variable *);

extern BAV_DLL struct bav_variable *bav_lcd_variable (
    struct bav_variable *,
    struct bav_variable *);

extern BAV_DLL bool bav_disjoint_variables (
    struct bav_variable *,
    struct bav_variable *);

extern BAV_DLL bool bav_is_derivative (
    struct bav_variable *,
    struct bav_variable *);

extern BAV_DLL bool bav_is_proper_derivative (
    struct bav_variable *,
    struct bav_variable *);

extern BAV_DLL bool bav_is_d_derivative (
    struct bav_variable *,
    struct bav_variable *,
    struct bav_symbol *);

extern BAV_DLL bool bav_is_derivative2 (
    struct bav_variable *,
    struct bav_tableof_variable *);

extern BAV_DLL struct bav_variable *bav_derivation_between_derivatives (
    struct bav_variable *,
    struct bav_variable *);

extern BAV_DLL void bav_operator_between_derivatives (
    struct bav_term *,
    struct bav_variable *,
    struct bav_variable *);

extern BAV_DLL struct bav_variable *bav_next_derivative (
    struct bav_variable *,
    struct bav_tableof_variable *);

extern BAV_DLL ba0_mint_hp bav_random_eval_variable_to_mint_hp (
    struct bav_variable *);

#   define BAV_jet_FLAG    1
#   define BAV_tjet_FLAG   2
#   define BAV_diff_FLAG   4
#   define BAV_Diff_FLAG   8
#   define BAV_D_FLAG     16

extern BAV_DLL ba0_scanf_function bav_scanf_jet_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_jet0_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_diff_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_Diff_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_sage_D_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_maple_D_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_sage_all_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_maple_all_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_sympy_Derivative_variable;

extern BAV_DLL void bav_reset_notations (
    void);

extern BAV_DLL ba0_int_p bav_get_notations (
    void);

extern BAV_DLL ba0_printf_function bav_printf_jet_variable;

extern BAV_DLL ba0_printf_function bav_printf_jet_wesb_variable;

extern BAV_DLL ba0_printf_function bav_printf_jet0_variable;

extern BAV_DLL ba0_printf_function bav_printf_LaTeX_variable;

extern BAV_DLL ba0_printf_function bav_printf_diff_variable;

extern BAV_DLL ba0_printf_function bav_printf_Diff_variable;

extern BAV_DLL ba0_printf_function bav_printf_maple_D_variable;

extern BAV_DLL ba0_printf_function bav_printf_sympy_Derivative_variable;

extern BAV_DLL ba0_scanf_function bav_scanf_variable;

extern BAV_DLL ba0_printf_function bav_printf_variable;

extern BAV_DLL ba0_cmp_function bav_gt_index_variable;

extern BAV_DLL ba0_cmp_function bav_gt_variable;

extern BAV_DLL void bav_sort_tableof_just_created_variable (
    struct bav_tableof_variable *);

extern BAV_DLL void bav_sort_tableof_variable (
    struct bav_tableof_variable *,
    enum ba0_sort_mode);

extern BAV_DLL void bav_independent_variables (
    struct bav_tableof_variable *);

struct bav_differential_ring;

extern BAV_DLL struct bav_variable *bav_switch_ring_variable (
    struct bav_variable *,
    struct bav_differential_ring *);

END_C_DECLS
#endif /* !BAV_VARIABLE_H */
