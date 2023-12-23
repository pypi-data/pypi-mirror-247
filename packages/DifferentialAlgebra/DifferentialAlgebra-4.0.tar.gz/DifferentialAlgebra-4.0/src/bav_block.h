#ifndef BAV_BLOCK_H
#   define BAV_BLOCK_H 1

#   include "bav_common.h"
#   include "bav_symbol.h"
#   include "bav_subranking.h"

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
