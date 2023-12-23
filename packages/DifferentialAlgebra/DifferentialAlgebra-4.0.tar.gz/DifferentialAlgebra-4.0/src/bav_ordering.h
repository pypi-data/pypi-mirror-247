#ifndef BAV_ORDERING_H
#   define BAV_ORDERING_H 1

#   include "bav_common.h"
#   include "bav_symbol.h"
#   include "bav_block.h"
#   include "bav_variable.h"
#   include "bav_operator.h"

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
