#include "bav_block.h"

/*
 * texinfo: bav_init_block
 * Initialize @var{b} to the empty block.
 */

BAV_DLL void
bav_init_block (
    bav_block b)
{
  b->subr = (struct bav_subranking *) 0;
  ba0_init_table ((ba0_table) & b->indices);
  ba0_init_table ((ba0_table) & b->strs);
}

/*
 * texinfo: bav_reset_block
 * Empty the block @var{b}.
 */

BAV_DLL void
bav_reset_block (
    bav_block b)
{
  b->subr = (struct bav_subranking *) 0;
  ba0_reset_table ((ba0_table) & b->indices);
  ba0_reset_table ((ba0_table) & b->strs);
}

/*
 * texinfo: bav_is_empty_block
 * Return @code{true} if @var{b} is empty.
 */

BAV_DLL bool
bav_is_empty_block (
    bav_block b)
{
  return b->strs.size == 0;
}

/*
 * texinfo: bav_new_block
 * Allocate a new block in the current stack, initialize it and
 * return it.
 */

BAV_DLL bav_block
bav_new_block (
    void)
{
  bav_block b;

  b = (bav_block) ba0_alloc (sizeof (struct bav_block));
  bav_init_block (b);
  return b;
}

/*
 * texinfo: bav_scanf_block
 * The parsing function for blocks.
 * It is called by @code{ba0_scanf/%b}.
 * The current stack should be the quiet stack if the block is read 
 * as part of an ordering but it can be any stack otherwise.
 * The field @code{indices} is left empty.
 * It will be filled by the calling function @code{bav_R_new_ranking}
 * if the block is read as part of an ordering.
 * Exception @code{BAV_ERRBLO} can be raised.
 */

BAV_DLL void *
bav_scanf_block (
    void *z)
{
  bav_block b;

  if (z == (void *) 0)
    b = bav_new_block ();
  else
    b = (bav_block) z;

  if (ba0_sign_token_analex ("["))
    {
      bav_is_subranking ("grlexA", &b->subr);
      ba0_scanf ("%t[%six]", &b->strs);
    }
  else if (ba0_type_token_analex () != ba0_string_token)
    {
      BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBLO);
    }
  else if (bav_is_subranking (ba0_value_token_analex (), &b->subr))
    {
      ba0_get_token_analex ();
      ba0_scanf ("%t[%six]", &b->strs);
    }
  else
    {
      bav_is_subranking ("grlexA", &b->subr);
      ba0_realloc_table ((ba0_table) & b->strs, 1);
      b->strs.tab[0] = (char *) ba0_scanf_indexed_string (0);
      b->strs.size = 1;
    }

  ba0_reset_table ((ba0_table) & b->indices);
  return b;
}

/*
 * texinfo: bav_printf_block
 * The printing function for blocks.
 * It is called by @code{ba0_printf/%b}.
 */

BAV_DLL void
bav_printf_block (
    void *z)
{
  bav_block b = (bav_block) z;

  ba0_printf ("%s%t[%s]", b->subr->ident, &b->strs);
}
