#ifndef BAV_COMMON_H
#   define BAV_COMMON_H 1

#   include <ba0.h>

/* 
 * The _MSC_VER flag is set if the code is compiled under WINDOWS
 * by using Microsoft Visual C (through Visual Studio 2008).
 *
 * In that case, some specific annotations must be added for DLL exports
 * Beware to the fact that this header file is going to be used either
 * for/while building BLAD or for using BLAD from an outer software.
 *
 * In the first case, functions are exported.
 * In the second one, they are imported.
 *
 * The flag BAV_BLAD_BUILDING must thus be set in the Makefile and passed
 * to the C preprocessor at BAV building time. Do not set it when using BAV.
 *
 * When compiling static libraries under Windows, set BA0_STATIC.
 */

#   if defined (_MSC_VER) && ! defined (BA0_STATIC)
#      if defined (BAV_BLAD_BUILDING)
#         define BAV_DLL  __declspec(dllexport)
#      else
#         define BAV_DLL  __declspec(dllimport)
#      endif
#   else
#      define BAV_DLL
#   endif

/* #   include "bav_mesgerr.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_Idegree
 * This is the integer type for degrees.
 */

typedef ba0_int_p bav_Idegree;

#   define BAV_MAX_IDEGRE BA0_MAX_INT_P

/*
 * texinfo: bav_Iordering
 * This is the integer type for ordering numbers.
 */

typedef ba0_int_p bav_Iordering;

/*
 * texinfo: bav_Inumber
 * This is the integer type for variable numbers.
 */

typedef ba0_int_p bav_Inumber;

/*
 * texinfo: bav_Iorder
 * This is the integer type for differentiation orders.
 */

typedef ba0_int_p bav_Iorder;

struct bav_tableof_Inumber
{
  ba0_int_p alloc;
  ba0_int_p size;
  bav_Inumber *tab;
};

struct bav_tableof_Iorder
{
  ba0_int_p alloc;
  ba0_int_p size;
  bav_Iorder *tab;
};

struct bav_tableof_Iordering
{
  ba0_int_p alloc;
  ba0_int_p size;
  bav_Iordering *tab;
};

struct bav_tableof_Idegree
{
  ba0_int_p alloc;
  ba0_int_p size;
  bav_Idegree *tab;
};

/* 
 * struct ba0_indexed* not recognized by parsers.
 * The function pointer, a buffer and the default value for the pointer
 */

extern BAV_DLL ba0_indexed_function bav_unknown_default;

extern BAV_DLL void bav_set_settings_common (
    ba0_indexed_function *);

extern BAV_DLL void bav_get_settings_common (
    ba0_indexed_function **);

extern BAV_DLL void bav_reset_all_settings (
    void);

extern BAV_DLL void bav_restart (
    ba0_int_p,
    ba0_int_p);

extern BAV_DLL void bav_terminate (
    enum ba0_restart_level);

END_C_DECLS
#endif /* !BAV_COMMON_H */
#ifndef BAV_MESGERR_H
#   define BAV_MESGERR_H 1

/* #   include "bav_common.h" */

BEGIN_C_DECLS

extern BAV_DLL char BAV_ERRUSY[];

extern BAV_DLL char BAV_ERRBSD[];

extern BAV_DLL char BAV_ERRPAO[];

extern BAV_DLL char BAV_ERRPAR[];

extern BAV_DLL char BAV_ERRDIF[];

extern BAV_DLL char BAV_ERRDVR[];

extern BAV_DLL char BAV_ERRSPY[];

extern BAV_DLL char BAV_ERRDFV[];

extern BAV_DLL char BAV_ERRBLO[];

extern BAV_DLL char BAV_ERRBOR[];

extern BAV_DLL char BAV_ERRTER[];

extern BAV_DLL char BAV_ERRRGZ[];

extern BAV_DLL char BAV_ERRTEU[];

extern BAV_DLL char BAV_EXEXQO[];

END_C_DECLS
#endif /* !BAV_MESGERR_H */
#ifndef BAV_SYMBOL_H
#   define BAV_SYMBOL_H 1

/* #   include "bav_common.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_typeof_symbol
 * Independent symbols are used to build derivations.
 * Dependent symbols are used to build differential indeterminates.
 */

enum bav_typeof_symbol
{
  bav_independent_symbol,
  bav_dependent_symbol,
  bav_operator_symbol,
  bav_temporary_symbol
};

/*
 * texinfo: bav_symbol
 * Symbols are used to create variables.
 * They are not duplicated. 
 * They are allocated in @code{ba0_global.stack.quiet}.
 * All symbols are stored in the array @code{bav_global.R.syms}.
 */

struct bav_symbol
{
  char *ident;
  enum bav_typeof_symbol type;
// the index in bav_global.R.syms
  ba0_int_p index;
// the index in bav_global.R.ders (if type = bav_independent_symbol)
  ba0_int_p derivation_index;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_symbol *bav_symbol;
#   endif

struct bav_tableof_symbol
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_symbol **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_symbol *bav_tableof_symbol;
#   endif

extern BAV_DLL void bav_set_settings_symbol (
    ba0_scanf_function *,
    ba0_printf_function *);

extern BAV_DLL void bav_get_settings_symbol (
    ba0_scanf_function **,
    ba0_printf_function **);

#   define BAV_NOT_A_SYMBOL	(struct bav_symbol*)0

extern BAV_DLL void bav_init_symbol (
    struct bav_symbol *);

extern BAV_DLL struct bav_symbol *bav_new_symbol (
    void);

extern BAV_DLL struct bav_symbol *bav_not_a_symbol (
    void);

extern BAV_DLL bool bav_is_a_derivation (
    char *);

extern BAV_DLL ba0_scanf_function bav_scanf_symbol;

extern BAV_DLL ba0_scanf_function bav_scanf_basic_symbol;

extern BAV_DLL ba0_scanf_function bav_scanf_default_symbol;

extern BAV_DLL ba0_printf_function bav_printf_symbol;

extern BAV_DLL ba0_printf_function bav_printf_default_symbol;

extern BAV_DLL ba0_printf_function bav_printf_numbered_symbol;

struct bav_differential_ring;

extern BAV_DLL struct bav_symbol *bav_switch_ring_symbol (
    struct bav_symbol *,
    struct bav_differential_ring *);

END_C_DECLS
#endif /* ! BAV_SYMBOL_H */
#ifndef BAV_PARAMETER_H
#   define BAV_PARAMETER_H 1

/* #   include "bav_symbol.h" */

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
#ifndef BAV_VARIABLE_H
#   define BAV_VARIABLE_H 1

/* #   include "bav_common.h" */
/* #   include "bav_symbol.h" */

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
#ifndef BAV_OPERATOR_H
#   define BAV_OPERATOR_H 1

/* #   include "bav_common.h" */
/* #   include "bav_variable.h" */


BEGIN_C_DECLS

END_C_DECLS
#endif /* !BAV_OPERATOR_H */
#ifndef BAV_SUBRANKING_H
#   define BAV_SUBRANKING_H 1

/* #   include "bav_common.h" */
/* #   include "bav_variable.h" */


BEGIN_C_DECLS

/*
 * texinfo: bav_subranking
 * This data type implements a subranking.
 */

struct bav_subranking
{
// the identifier of the subranking (grlexA, degrevlexB, ...)
  char *ident;
// a comparison function (*inf) (v, w, nv, nw, ders)
// Return true if v < w w.r.t. the subranking
// nv and nw are the indices of v and w in their block
// ders is the table of the derivations
  bool (
      *inf) (
      struct bav_variable *,
      struct bav_variable *,
      ba0_int_p,
      ba0_int_p,
      struct bav_tableof_symbol *);
};

extern BAV_DLL bool bav_is_subranking (
    char *,
    struct bav_subranking **);

END_C_DECLS
#endif /* !BAV_SUBRANKING_H */
#ifndef BAV_BLOCK_H
#   define BAV_BLOCK_H 1

/* #   include "bav_common.h" */
/* #   include "bav_symbol.h" */
/* #   include "bav_subranking.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_block
 * A block is a list of dependent symbols / differential indeterminates
 * ordered w.r.t. some common subranking.
 * Orderings mostly are lists of blocks.
 */

struct bav_block
{
// the subranking which applies to the block
  struct bav_subranking *subr;
// the identifiers of the symbols listed in the block
  struct ba0_tableof_string strs;
// the indices in bav_global.R.syms of the corresponding symbols
// or the empty table if the block is built independently of
// any ranking
  struct ba0_tableof_int_p indices;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_block *bav_block;
#   endif

#   define BAV_NOT_A_BLOCK (struct bav_block*)0

struct bav_tableof_block
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_block **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_block *bav_tableof_block;
#   endif

extern BAV_DLL void bav_init_block (
    struct bav_block *);

extern BAV_DLL void bav_reset_block (
    struct bav_block *);

extern BAV_DLL struct bav_block *bav_new_block (
    void);

extern BAV_DLL bool bav_is_empty_block (
    struct bav_block *);

extern BAV_DLL ba0_scanf_function bav_scanf_block;

extern BAV_DLL ba0_printf_function bav_printf_block;

END_C_DECLS
#endif /* !BAV_BLOCK_H */
#ifndef BAV_ORDERING_H
#   define BAV_ORDERING_H 1

/* #   include "bav_common.h" */
/* #   include "bav_symbol.h" */
/* #   include "bav_block.h" */
/* #   include "bav_variable.h" */
/* #   include "bav_operator.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_ordering
 * This data type is a subtype of @code{bav_differential_ring}
 * used to describe orderings. In each table, leftmost elements
 * are considered greater than rightmost ones.
 */

struct bav_ordering
{
  struct bav_tableof_symbol ders;       // the table of derivations
  struct bav_tableof_block blocks;      // the table of blocks
  struct bav_block operator_block;      // the block for operators
// the variables set as maximal variables
  struct bav_tableof_variable varmax;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_ordering *bav_ordering;
#   endif

struct bav_tableof_ordering
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_ordering **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_ordering *bav_tableof_ordering;
#   endif

extern BAV_DLL void bav_set_settings_ordering (
    char *);

extern BAV_DLL void bav_get_settings_ordering (
    char **);

extern BAV_DLL void bav_init_ordering (
    struct bav_ordering *);

extern BAV_DLL void bav_reset_ordering (
    struct bav_ordering *);

extern BAV_DLL struct bav_ordering *bav_new_ordering (
    void);

extern BAV_DLL void bav_set_ordering (
    struct bav_ordering *,
    struct bav_ordering *);

extern BAV_DLL ba0_scanf_function bav_scanf_ordering;

extern BAV_DLL ba0_printf_function bav_printf_ordering;

END_C_DECLS
#endif /* !BAV_ORDERING_H */
#ifndef BAV_DIFFERENTIAL_RING_H
#   define BAV_DIFFERENTIAL_RING_H 1

/* #   include "bav_common.h" */
/* #   include "bav_block.h" */
/* #   include "bav_symbol.h" */
/* #   include "bav_variable.h" */
/* #   include "bav_operator.h" */
/* #   include "bav_ordering.h" */

#   define BAV_NOT_AN_OPINDEX	-1

/* 
 * ders [i] = the index in vars of the independent variable which has
 * root->derivation_index = i. 
 */

BEGIN_C_DECLS

/*
 * texinfo: bav_differential_ring
 * This data type implements one mathematical differential ring
 * endowed with many different orderings. It is completely
 * stored in @code{ba0_global.stack.quiet}.
 */

struct bav_differential_ring
{
  bool empty;                   // true if the structure is empty
  struct ba0_tableof_string strs;       // all identifiers
  struct bav_tableof_symbol syms;       // all symbols
  struct bav_tableof_variable vars;     // all variables
// the indices of derivations a.k.a. independent variables
// these indices are valid for both syms and vars
  struct ba0_tableof_int_p ders;
// the indices of the differential indeterminates (dependent variables)
// these indices are valid for both syms and vars
  struct ba0_tableof_int_p deps;
// the indices of the temporary variables in vars
  struct ba0_tableof_int_p tmps;
// tmps_in_use[i] is nonzero iff tmps[i] is in use
  struct ba0_tableof_int_p tmps_in_use;
//  -1 or the index in syms of the symbol used for differential operators
  ba0_int_p opra;
// all defined orderings
  struct bav_tableof_ordering ords;
// a stack of indices in ords
// the top element is the index of the current ordering
  struct bav_tableof_Iordering ord_stack;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_differential_ring *bav_differential_ring;
#   endif

extern BAV_DLL void bav_init_differential_ring (
    struct bav_differential_ring *);

extern BAV_DLL struct bav_differential_ring *bav_new_differential_ring (
    void);

extern BAV_DLL unsigned ba0_int_p bav_sizeof_differential_ring (
    struct bav_differential_ring *);

extern BAV_DLL void bav_set_differential_ring (
    struct bav_differential_ring *,
    struct bav_differential_ring *);

extern BAV_DLL void bav_R_init (
    void);

extern BAV_DLL bool bav_R_is_empty (
    void);

extern BAV_DLL void bav_R_create (
    struct ba0_tableof_string *,
    struct bav_tableof_block *,
    struct bav_block *);

extern BAV_DLL bav_Iordering bav_R_new_ranking (
    struct ba0_tableof_string *,
    struct bav_tableof_block *,
    struct bav_block *);

extern BAV_DLL bool bav_R_ambiguous_symbols (
    void);

extern BAV_DLL bav_Iordering bav_R_copy_ordering (
    bav_Iordering);

extern BAV_DLL struct bav_variable *bav_R_new_temporary_variable (
    void);

extern BAV_DLL void bav_R_free_temporary_variable (
    struct bav_variable *);

extern BAV_DLL void bav_R_set_maximal_variable (
    struct bav_variable *);

extern BAV_DLL void bav_R_swap_ordering (
    bav_Iordering,
    bav_Iordering);

extern BAV_DLL void bav_R_free_ordering (
    bav_Iordering);

extern BAV_DLL void bav_R_restore_ords_size (
    ba0_int_p);

extern BAV_DLL void bav_R_push_ordering (
    bav_Iordering);

extern BAV_DLL void bav_R_pull_ordering (
    void);

extern BAV_DLL bav_Iordering bav_R_Iordering (
    void);

extern BAV_DLL struct bav_ordering *bav_R_ordering (
    void);

extern BAV_DLL bav_Inumber bav_R_variable_number (
    struct bav_variable *);

extern BAV_DLL bav_Inumber bav_R_symbol_block_number (
    struct bav_symbol *,
    ba0_int_p *);

extern BAV_DLL struct bav_variable *bav_R_derivative (
    struct bav_variable *,
    struct bav_symbol *);

extern BAV_DLL struct bav_variable *bav_R_symbol_to_variable (
    struct bav_symbol *);

extern BAV_DLL struct bav_symbol *bav_R_string_to_symbol (
    char *);

extern BAV_DLL struct bav_symbol *bav_R_string_to_derivation (
    char *);

extern BAV_DLL struct bav_variable *bav_R_string_to_variable (
    char *);

extern BAV_DLL struct bav_variable *bav_R_derivation_index_to_derivation (
    ba0_int_p);

extern BAV_DLL void bav_R_mark_variables (
    ba0_int_p);

extern BAV_DLL void bav_R_marked_variables (
    struct bav_tableof_variable *,
    ba0_int_p);

END_C_DECLS
#endif /* !BAV_DIFFERENTIAL_RING_H */
#ifndef BAV_POINT_INT_P_H
#   define BAV_POINT_INT_P_H 1

/* #   include "bav_common.h" */
/* #   include "bav_variable.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_value_int_p
 * This data type permits to associate a @code{ba0_int_p} value
 * to a variable.
 */

struct bav_value_int_p
{
  struct bav_variable *var;
  ba0_int_p value;
};

extern BAV_DLL int bav_inv_comp_value_int_p (
    const void *,
    const void *);

#   if defined (BA0_OLDDEF)
typedef struct bav_value_int_p *bav_value_int_p;
#   endif

/*
 * texinfo: bav_point_int_p
 * This data type permits to associate @code{ba0_int_p} values to
 * many different variables. The variables in the @code{tab} field
 * should be sorted by increasing addresses.
 */

struct bav_point_int_p
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_value_int_p **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_point_int_p *bav_point_int_p;
#   endif

extern BAV_DLL void bav_sort_point_int_p (
    struct bav_point_int_p *);

END_C_DECLS
#endif /* !BAV_POINT_INT_P_H */
#ifndef BAV_POINT_INTERVAL_MPQ_H
#   define BAV_POINT_INTERVAL_MPQ_H 1

/* #   include "bav_common.h" */
/* #   include "bav_variable.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_value_interval_mpq
 * This data type associates an interval with @code{mpq_t} ends
 * to a variable.
 */

struct bav_value_interval_mpq
{
  struct bav_variable *var;
  struct ba0_interval_mpq *value;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_value_interval_mpq *bav_value_interval_mpq;
#   endif

/* In the next one, all variables might be equal */

struct bav_tableof_value_interval_mpq
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_value_interval_mpq **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_value_interval_mpq *bav_tableof_value_interval_mpq;
#   endif


/*
 * texinfo: bav_point_interval_mpq
 * This data type permits to associate interval with @code{mpq_t} ends
 * to many different variables. The array @code{tab} should be sorted
 * by increasing addresses.
 */

struct bav_point_interval_mpq
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_value_interval_mpq **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_point_interval_mpq *bav_point_interval_mpq;
#   endif

struct bav_tableof_point_interval_mpq
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_point_interval_mpq **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_point_interval_mpq *bav_tableof_point_interval_mpq;
#   endif

extern BAV_DLL struct bav_value_interval_mpq *bav_new_value_interval_mpq (
    void);

extern BAV_DLL void bav_set_value_interval_mpq (
    struct bav_value_interval_mpq *,
    struct bav_value_interval_mpq *);

extern BAV_DLL void bav_init_point_interval_mpq (
    struct bav_point_interval_mpq *);

extern BAV_DLL struct bav_point_interval_mpq *bav_new_point_interval_mpq (
    void);

extern BAV_DLL void bav_realloc_point_interval_mpq (
    struct bav_point_interval_mpq *,
    ba0_int_p);

extern BAV_DLL void bav_set_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *);

extern BAV_DLL void bav_set_coord_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_variable *,
    struct ba0_interval_mpq *);

extern BAV_DLL void bav_intersect_coord_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *,
    struct bav_variable *,
    struct ba0_interval_mpq *);

extern BAV_DLL void bav_intersect_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *);

extern BAV_DLL bool bav_is_empty_point_interval_mpq (
    struct bav_point_interval_mpq *);

extern BAV_DLL void bav_bisect_point_interval_mpq (
    struct bav_tableof_point_interval_mpq *,
    struct bav_point_interval_mpq *,
    ba0_int_p);

extern BAV_DLL void bav_set_tableof_point_interval_mpq (
    struct bav_tableof_point_interval_mpq *,
    struct bav_tableof_point_interval_mpq *);

END_C_DECLS
#endif /* !BAV_POINT_INTERVAL_MPQ_H */
#ifndef BAV_RANK_H
#   define BAV_RANK_H 1

/* #   include "bav_common.h" */
/* #   include "bav_variable.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_rank
 * A rank is a variable raised to some degree.
 * Observe that some special ranks are also defined such as the
 * rank of zero and the one of nonzero constants.
 * The rank of zero is encoded by 
 * (@code{BAV_NOT_A_VARIABLE}, @math{-1}).
 * The rank of nonzero constants is encoded by a field @code{deg}
 * equal to @math{0} (the field @code{var} is unspecified).
 * Ranks are stored in the main and second stacks.
 */

struct bav_rank
{
  struct bav_variable *var;     // possibly BAV_NOT_A_VARIABLE
  bav_Idegree deg;              // possibly 0 or negative
};

#   if defined (BA0_OLDDEF)
typedef struct bav_rank *bav_rank;
#   endif

extern BAV_DLL void bav_init_rank (
    struct bav_rank *);

extern BAV_DLL struct bav_rank *bav_new_rank (
    void);

extern BAV_DLL bool bav_is_zero_rank (
    struct bav_rank *);

extern BAV_DLL bool bav_is_constant_rank (
    struct bav_rank *);

extern BAV_DLL bool bav_lt_rank (
    struct bav_rank *,
    struct bav_rank *);

extern BAV_DLL bool bav_gt_rank (
    struct bav_rank *,
    struct bav_rank *);

extern BAV_DLL bool bav_equal_rank (
    struct bav_rank *,
    struct bav_rank *);

extern BAV_DLL int bav_inv_comp_rank (
    const void *,
    const void *);

extern BAV_DLL struct bav_rank bav_zero_rank (
    void);

extern BAV_DLL struct bav_rank bav_constant_rank (
    void);

extern BAV_DLL struct bav_rank bav_constant_rank2 (
    struct bav_variable *);

extern BAV_DLL void bav_set_settings_rank (
    ba0_printf_function *);

extern BAV_DLL void bav_get_settings_rank (
    ba0_printf_function **);

extern BAV_DLL ba0_scanf_function bav_scanf_rank;

extern BAV_DLL ba0_printf_function bav_printf_rank;

extern BAV_DLL ba0_printf_function bav_printf_default_rank;

extern BAV_DLL ba0_printf_function bav_printf_stars_rank;

extern BAV_DLL ba0_printf_function bav_printf_list_rank;

struct bav_tableof_rank
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_rank **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_rank *bav_tableof_rank;
#   endif

END_C_DECLS
#endif /* !BAV_RANK_H */
#ifndef BAV_TERM_H
#   define BAV_TERM_H 1

/* #   include "bav_common.h" */
/* #   include "bav_rank.h" */
/* #   include "bav_point_int_p.h" */
/* #   include "bav_parameter.h" */
/* #   include "bav_point_interval_mpq.h" */

BEGIN_C_DECLS

/*
 * texinfo: bav_term
 * A term is a product of ranks (the ranks of zero and of nonzero
 * constants are forbidden) sorted by decreasing order w.r.t. the
 * current ordering.
 * The empty product encodes the term @math{1}.
 * The leading rank of a nonempty product is the leading rank 
 * of the term.
 */

struct bav_term
{
  ba0_int_p alloc;              // number of entries allocated to rg
  ba0_int_p size;               // number of entries used in rg
  struct bav_rank *rg;          // the array of ranks
};

#   if defined (BA0_OLDDEF)
typedef struct bav_term *bav_term;
#   endif

struct bav_listof_term
{
  struct bav_term *value;
  struct bav_listof_term *next;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_listof_term *bav_listof_term;
#   endif

struct bav_tableof_term
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_term **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_term *bav_tableof_term;
#   endif

extern BAV_DLL void bav_realloc_term (
    struct bav_term *,
    ba0_int_p);

extern BAV_DLL void bav_init_term (
    struct bav_term *);

extern BAV_DLL struct bav_term *bav_new_term (
    void);

extern BAV_DLL void bav_set_term_one (
    struct bav_term *);

extern BAV_DLL void bav_set_term_variable (
    struct bav_term *,
    struct bav_variable *,
    bav_Idegree);

extern BAV_DLL void bav_set_term_rank (
    struct bav_term *,
    struct bav_rank *);

extern BAV_DLL void bav_set_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_shift_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_strip_term (
    struct bav_term *,
    struct bav_term *,
    bav_Inumber);

extern BAV_DLL bool bav_is_one_term (
    struct bav_term *);

extern BAV_DLL struct bav_variable *bav_leader_term (
    struct bav_term *);

extern BAV_DLL bav_Idegree bav_leading_degree_term (
    struct bav_term *);

extern BAV_DLL bav_Idegree bav_total_degree_term (
    struct bav_term *);

extern BAV_DLL bav_Idegree bav_degree_term (
    struct bav_term *,
    struct bav_variable *);

extern BAV_DLL bav_Iorder bav_total_order_term (
    struct bav_term *);

extern BAV_DLL bav_Idegree bav_maximal_degree_term (
    struct bav_term *);

extern BAV_DLL struct bav_rank bav_leading_rank_term (
    struct bav_term *);

extern BAV_DLL bool bav_disjoint_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL bool bav_equal_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL bool bav_gt_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL bool bav_lt_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_sort_term (
    struct bav_term *);

extern BAV_DLL void bav_lcm_term (
    struct bav_term *,
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_gcd_term (
    struct bav_term *,
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_mul_term (
    struct bav_term *,
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_mul_term_rank (
    struct bav_term *,
    struct bav_term *,
    struct bav_rank *);

extern BAV_DLL void bav_mul_term_variable (
    struct bav_term *,
    struct bav_term *,
    struct bav_variable *,
    bav_Idegree);

extern BAV_DLL void bav_pow_term (
    struct bav_term *,
    struct bav_term *,
    bav_Idegree);

extern BAV_DLL void bav_exquo_term (
    struct bav_term *,
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_exquo_term_variable (
    struct bav_term *,
    struct bav_term *,
    struct bav_variable *,
    bav_Idegree);

extern BAV_DLL bool bav_is_factor_term (
    struct bav_term *,
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL void bav_diff_term (
    struct bav_term *,
    struct bav_term *,
    struct bav_symbol *,
    struct bav_tableof_variable *);

extern BAV_DLL void bav_marked_ranks_term (
    struct bav_term *);

extern BAV_DLL void bav_term_at_point_int_p (
    ba0_mpz_t,
    struct bav_term *,
    struct bav_point_int_p *);

extern BAV_DLL void bav_term_at_point_interval_mpq (
    struct ba0_interval_mpq *,
    struct bav_term *,
    struct bav_point_interval_mpq *);

extern BAV_DLL ba0_garbage1_function bav_garbage1_term;

extern BAV_DLL ba0_garbage2_function bav_garbage2_term;

extern BAV_DLL ba0_scanf_function bav_scanf_term;

extern BAV_DLL ba0_printf_function bav_printf_term;

extern BAV_DLL ba0_copy_function bav_copy_term;

struct bav_differential_ring;

extern BAV_DLL void bav_switch_ring_term (
    struct bav_term *,
    struct bav_differential_ring *);

extern BAV_DLL bool bav_depends_on_zero_derivatives_of_parameter_term (
    struct bav_term *,
    struct bav_tableof_parameter *);

END_C_DECLS
#endif /* !BAV_TERM_H */
#ifndef BAV_TERM_ORDERING_H
#   define BAV_TERM_ORDERING_H 1

/* #   include "bav_term.h" */

BEGIN_C_DECLS

extern BAV_DLL enum ba0_compare_code bav_compare_term (
    struct bav_term *,
    struct bav_term *);

extern BAV_DLL enum ba0_compare_code bav_compare_stripped_term (
    struct bav_term *,
    struct bav_term *,
    bav_Inumber);

extern BAV_DLL void bav_set_term_ordering (
    char *);

END_C_DECLS
#endif /* !BAV_TERM_ORDERING_H */
#ifndef BAV_GLOBAL_H
#   define BAV_GLOBAL_H 1

/* #   include "bav_common.h" */
/* #   include "bav_differential_ring.h" */
/* #   include "bav_parameter.h" */
/* #   include "bav_term.h" */


BEGIN_C_DECLS

struct bav_global
{
  struct
  {
/* 
 * Receives the faulty string when an unknown variable/symbol is parsed
 */
    char unknown[BA0_BUFSIZE];
  } common;
  struct bav_differential_ring R;
  struct
  {
/*
 * Flags indicating which input notation was used
 */
    ba0_int_p notations;
/* 
 * "diff" or "Diff" to display derivatives
 */
    char *diff_string;
  } variable;
/* 
 * Variables some derivatives of which are zero
 */
  struct bav_tableof_parameter parameters;
  struct
  {
/* 
 * Comparison functions w.r.t. term orderings
 */
    enum ba0_compare_code (
        *compare) (
        struct bav_term *,
        struct bav_term *);
    enum ba0_compare_code (
        *compare_stripped) (
        struct bav_term *,
        struct bav_term *,
        bav_Inumber);
  } term_ordering;
};

struct bav_initialized_global
{
  struct
  {
/* 
 * Function called when an unknown symbol/variable/parameter is parsed
 */
    ba0_indexed_function *unknown;
  } common;
  struct
  {
/* 
 * Functions pointers for customizing symbol parsing and printing
 */
    ba0_scanf_function *scanf;
    ba0_printf_function *printf;
  } symbol;
  struct
  {
/* 
 * Functions pointers for customizing variable parsing and printing
 */
    ba0_scanf_function *scanf;
    ba0_printf_function *printf;
/*
 * The string which stands for no derivation in the jet0 notation
 */
    char *jet0_string;
/* 
 * The prefix of temporary variables
 */
    char *temp_string;
  } variable;
  struct
  {
/* 
 * Function pointer for customizing the way ranks are printed.
 */
    ba0_printf_function *printf;
  } rank;
  struct
  {
/* 
 * The string for displaying orderings
 */
    char *string;
  } ordering;
};

extern BAV_DLL struct bav_global bav_global;

extern BAV_DLL struct bav_initialized_global bav_initialized_global;

END_C_DECLS
#endif /* !BAV_GLOBAL_H */
