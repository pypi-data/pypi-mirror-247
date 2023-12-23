#ifndef BAV_SYMBOL_H
#   define BAV_SYMBOL_H 1

#   include "bav_common.h"

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
