#include "bav_symbol.h"
#include "bav_differential_ring.h"
#include "bav_global.h"

/*
 * texinfo: bav_set_settings_symbol
 * Assign @var{s} and @var{p} to the corresponding settings variables.
 * If these parameters are zero, the settings variables are reset to their
 * default values (indexed strings).
 */

BAV_DLL void
bav_set_settings_symbol (
    ba0_scanf_function *s,
    ba0_printf_function *p)
{
  bav_initialized_global.symbol.scanf = s ? s : &bav_scanf_default_symbol;
  bav_initialized_global.symbol.printf = p ? p : &bav_printf_default_symbol;
}

/*
 * texinfo: bav_get_settings_symbol
 * Assign the corresponding settings variables to *@var{s} and *@var{p}, 
 * if they are nonzero.
 */

BAV_DLL void
bav_get_settings_symbol (
    ba0_scanf_function **s,
    ba0_printf_function **p)
{
  if (s)
    *s = bav_initialized_global.symbol.scanf;
  if (p)
    *p = bav_initialized_global.symbol.printf;
}

/*
 * texinfo: bav_init_symbol
 * Constructor only used for allocating tables of symbols. 
 * There is no such thing as an empty symbol.
 * Symbols are actually constructed while constructing differential rings.
 */

BAV_DLL void
bav_init_symbol (
    bav_symbol s)
{
  s->ident = (char *) 0;
}

/*
 * texinfo: bav_new_symbol
 * New function only used for allocating tables of symbols.
 */

BAV_DLL bav_symbol
bav_new_symbol (
    void)
{
  bav_symbol s;

  s = (bav_symbol) ba0_alloc (sizeof (struct bav_symbol));
  bav_init_symbol (s);
  return s;
}

/*
 * texinfo: bav_not_a_symbol
 * Return the constant @code{BAV_NOT_A_SYMBOL}.
 */

BAV_DLL bav_symbol
bav_not_a_symbol (
    void)
{
  return BAV_NOT_A_SYMBOL;
}

/*
 * texinfo: bav_is_a_derivation
 * Return @code{true} if @var{string} is equal to the @code{ident}
 * field of an existing derivation.
 */

BAV_DLL bool
bav_is_a_derivation (
    char *string)
{
  return bav_R_string_to_derivation (string) != BAV_NOT_A_SYMBOL;
}

/*
 * texinfo: bav_switch_ring_symbol
 * Return the symbol of @var{R} which has the same index in 
 * @code{R->syms} as @var{s}. This low level function should be used 
 * in conjunction with @code{bav_set_differential_ring}: 
 * if @var{R} is a ring obtained by application of 
 * @code{bav_set_differential_ring} to the ring @var{s} refers to, 
 * then this function returns the element of @var{R} which corresponds 
 * to @var{s}.
 */

BAV_DLL bav_symbol
bav_switch_ring_symbol (
    bav_symbol s,
    bav_differential_ring R)
{
  return R->syms.tab[s->index];
}

/* 
 * texinfo: bav_scanf_default_symbol
 * The default function for parsing symbols, called by
 * @code{ba0_scanf/%y}. Indexed strings are allowed.
 * Exception @code{BAV_ERRUSY} is raised if the symbol does not exist.
 */

BAV_DLL void *
bav_scanf_default_symbol (
    void *z)
{
  char *s;
  ba0_indexed x;
  bav_symbol y;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  x = ba0_scanf_indexed (0, 0, 0);
  s = ba0_indexed_to_string (x);
  ba0_pull_stack ();

  y = bav_R_string_to_symbol (s);
  if (y == BAV_NOT_A_SYMBOL)
    {
      (*bav_initialized_global.common.unknown) (x);
      BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
    }
  if (z != (void *) 0)
    *(bav_symbol *) z = y;
  ba0_restore (&M);
  return y;
}

/* 
 * texinfo: bav_scanf_basic_symbol
 * A possible function for parsing symbols.
 * Indexed strings are not allowed.
 * Exception @code{BAV_ERRUSY} is raised if the symbol does not exist.
 */

BAV_DLL void *
bav_scanf_basic_symbol (
    void *z)
{
  char *s;
  bav_symbol y;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  s = ba0_scanf_string (0);
  ba0_pull_stack ();

  y = bav_R_string_to_symbol (s);
  if (y == BAV_NOT_A_SYMBOL)
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
  if (z != (void *) 0)
    *(bav_symbol *) z = y;
  ba0_restore (&M);
  return y;
}

/*
 * texinfo: bav_printf_default_symbol
 * The default function for printing symbols (the @code{ident} field
 * is printed).
 * It is called by @code{ba0_printf/%y}.
 */

BAV_DLL void
bav_printf_default_symbol (
    void *z)
{
  bav_symbol s = (bav_symbol) z;
  ba0_put_string (s->ident);
}

/*
 * texinfo: bav_printf_numbered_symbol
 * A possible function for printing symbols (an underscore
 * followed by the value of the @code{index} field of the symbol.
 */

BAV_DLL void
bav_printf_numbered_symbol (
    void *z)
{
  bav_symbol s = (bav_symbol) z;

  if (s->type == bav_independent_symbol || s->type == bav_dependent_symbol)
    ba0_printf ("%s%d", "_", s->index);
  else
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
}

BAV_DLL void *
bav_scanf_symbol (
    void *z)
{
  void *r = (void *) 0;

  if (bav_initialized_global.symbol.scanf != (ba0_scanf_function *) 0)
    r = (*bav_initialized_global.symbol.scanf) (z);
  else
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  return r;
}

BAV_DLL void
bav_printf_symbol (
    void *z)
{
  if (bav_initialized_global.symbol.printf != (ba0_printf_function *) 0)
    (*bav_initialized_global.symbol.printf) (z);
  else
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
}
