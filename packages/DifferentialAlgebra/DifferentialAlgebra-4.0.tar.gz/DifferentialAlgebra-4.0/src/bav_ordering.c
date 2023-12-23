#include "bav_ordering.h"
#include "bav_differential_ring.h"
#include "bav_global.h"

/*
 * texinfo: bav_set_settings_ordering
 * Set to @var{ordstring} the leading string used for parsing
 * nd printing orderings. If zero, this leading string is reset 
 * to its default value: @code{ordering}.
 */

BAV_DLL void
bav_set_settings_ordering (
    char *ordstring)
{
  bav_initialized_global.ordering.string = ordstring ? ordstring : "ordering";
}

/*
 * texinfo: bav_get_settings_ordering
 * Assign to @var{ordstring} the leading string used for 
 * printing orderings.
 */

BAV_DLL void
bav_get_settings_ordering (
    char **ordstring)
{
  if (ordstring)
    *ordstring = bav_initialized_global.ordering.string;
}

/*
 * texinfo: bav_init_ordering
 * Initialize @var{o} to the empty ordering.
 */

BAV_DLL void
bav_init_ordering (
    bav_ordering o)
{
  ba0_init_table ((ba0_table) & o->ders);
  ba0_init_table ((ba0_table) & o->blocks);
  bav_init_block (&o->operator_block);
  ba0_init_table ((ba0_table) & o->varmax);
}

/*
 * texinfo: bav_reset_ordering
 * Empty the ordering @var{o}.
 */

BAV_DLL void
bav_reset_ordering (
    bav_ordering o)
{
  ba0_reset_table ((ba0_table) & o->ders);
  ba0_reset_table ((ba0_table) & o->blocks);
  bav_reset_block (&o->operator_block);
  ba0_reset_table ((ba0_table) & o->varmax);
}

/*
 * texinfo: bav_new_ordering
 * Allocate a new ordering in the current stack, initialize it and
 * return it.
 */

BAV_DLL bav_ordering
bav_new_ordering (
    void)
{
  bav_ordering o;

  o = (bav_ordering) ba0_alloc (sizeof (struct bav_ordering));
  bav_init_ordering (o);
  return o;
}

/*
 * texinfo: bav_set_ordering
 * Assign @var{S} to @var{R}.
 */

BAV_DLL void
bav_set_ordering (
    bav_ordering R,
    bav_ordering S)
{
  ba0_int_p i;

  ba0_set_table ((ba0_table) & R->ders, (ba0_table) & S->ders);

  ba0_reset_table ((ba0_table) & R->blocks);
  ba0_realloc2_table ((ba0_table) & R->blocks, S->blocks.size,
      (ba0_new_function *) & bav_new_block);
  for (i = 0; i < S->blocks.size; i++)
    {
      R->blocks.tab[i]->subr = S->blocks.tab[i]->subr;
      ba0_set_table ((ba0_table) & R->blocks.tab[i]->strs,
          (ba0_table) & S->blocks.tab[i]->strs);
    }
  R->blocks.size = S->blocks.size;

  R->operator_block.subr = S->operator_block.subr;
  ba0_set_table ((ba0_table) & R->operator_block.strs,
      (ba0_table) & S->operator_block.strs);

  ba0_set_table ((ba0_table) & R->varmax, (ba0_table) & S->varmax);
}

/*
 * texinfo: bav_scanf_ordering
 * The function which parses orderings.
 * It is called by @code{ba0_scanf/%ordering}.
 * It may raise exception @code{BAV_ERRBOR}.
 */

BAV_DLL void *
bav_scanf_ordering (
    void *z)
{
  volatile ba0_tableof_string D;
  volatile bav_tableof_block B;
  bav_block O;
  bav_tableof_variable V;
  bav_Iordering r;
  struct ba0_mark M;
  ba0_int_p i;


  D = (ba0_tableof_string) 0;
  B = (bav_tableof_block) 0;

  ba0_push_another_stack ();
  ba0_record (&M);
  if (ba0_type_token_analex () != ba0_string_token ||
      (ba0_strcasecmp (ba0_value_token_analex (),
              bav_initialized_global.ordering.string) != 0))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();
  if (!ba0_sign_token_analex ("("))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();
/*
   ordering (
              ^
*/
  if (ba0_type_token_analex () != ba0_string_token ||
      ba0_strcasecmp (ba0_value_token_analex (), "derivations") != 0)
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();
  if (!ba0_sign_token_analex ("="))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();

  BA0_TRY
  {
    D = (ba0_tableof_string) ba0_new_table ();
    ba0_scanf ("%t[%six]", D);
  }
  BA0_CATCH
  {
    if (ba0_global.exception.raised == BA0_ERROOM ||
        ba0_global.exception.raised == BA0_ERRALR)
      BA0_RE_RAISE_EXCEPTION;
    BA0_RAISE_EXCEPTION (BAV_ERRBOR);
  }
  BA0_ENDTRY;
  ba0_get_token_analex ();
/*
   ordering (derivations = %t[%s]
                                  ^
*/
  if (!ba0_sign_token_analex (","))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();
  if (ba0_type_token_analex () != ba0_string_token ||
      (ba0_strcasecmp (ba0_value_token_analex (), "blocks") != 0 &&
          ba0_strcasecmp (ba0_value_token_analex (), "ranking") != 0))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();
  if (!ba0_sign_token_analex ("="))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
  ba0_get_token_analex ();

  BA0_TRY
  {
    B = (bav_tableof_block) ba0_new_table ();
    ba0_scanf ("%t[%b]", B);
  }
  BA0_CATCH
  {
    if (ba0_global.exception.raised == BA0_ERROOM ||
        ba0_global.exception.raised == BA0_ERRALR)
      BA0_RE_RAISE_EXCEPTION;
    BA0_RAISE_EXCEPTION (BAV_ERRBOR);
  }
  BA0_ENDTRY;

  i = 0;
  while (i < B->size)
    {
      if (bav_is_empty_block (B->tab[i]))
        ba0_delete_table ((ba0_table) B, i);
      else
        i += 1;
    }
  ba0_get_token_analex ();
/*
   ordering (derivations = %t[%s], blocks = %t[%b]
                                                   ^
*/
  O = bav_new_block ();
  if (ba0_sign_token_analex (","))
    {
      ba0_get_token_analex ();
      if (ba0_type_token_analex () == ba0_string_token &&
          ba0_strcasecmp (ba0_value_token_analex (), "operator") == 0)
        {
          ba0_get_token_analex ();
          if (!ba0_sign_token_analex ("="))
            BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
          ba0_get_token_analex ();

          BA0_TRY
          {
            ba0_scanf ("%b", O);
          }
          BA0_CATCH
          {
            if (ba0_global.exception.raised == BA0_ERROOM ||
                ba0_global.exception.raised == BA0_ERRALR)
              BA0_RE_RAISE_EXCEPTION;
            BA0_RAISE_EXCEPTION (BAV_ERRBOR);
          }
          BA0_ENDTRY;

          ba0_get_token_analex ();
        }
      else
        ba0_unget_token_analex (1);
    }
/*
   ordering (derivations = %t[%s], blocks = %t[%b] {, operator = %b }
                                                                      ^
*/
  if (bav_R_is_empty ())
    {
      BA0_TRY
      {
        bav_R_create (D, B, O);
      }
      BA0_CATCH
      {
        bav_R_init ();
        if (ba0_global.exception.raised == BA0_ERROOM ||
            ba0_global.exception.raised == BA0_ERRALR)
          BA0_RE_RAISE_EXCEPTION;
        BA0_RAISE_EXCEPTION (BAV_ERRBOR);
      }
      BA0_ENDTRY;
    }
  r = bav_R_new_ranking (D, B, O);
/*
   The differential ring bav_R is not empty here.
*/
  V = (bav_tableof_variable) ba0_new_table ();
  if (ba0_sign_token_analex (","))
    {
      ba0_get_token_analex ();
      if (ba0_type_token_analex () == ba0_string_token &&
          ba0_strcasecmp (ba0_value_token_analex (), "varmax") == 0)
        {
          ba0_get_token_analex ();
          if (!ba0_sign_token_analex ("="))
            BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);
          ba0_get_token_analex ();

          BA0_TRY
          {
            ba0_scanf ("%t[%v]", V);
          }
          BA0_CATCH
          {
            if (ba0_global.exception.raised == BA0_ERROOM ||
                ba0_global.exception.raised == BA0_ERRALR)
              BA0_RE_RAISE_EXCEPTION;
            BA0_RAISE_EXCEPTION (BAV_ERRBOR);
          }
          BA0_ENDTRY;
          ba0_get_token_analex ();
        }
      else
        ba0_unget_token_analex (1);
    }
/*
   ordering ( ... blocks = %t[%b] {, operator = %b } {, varmax = %t[%v] }
                                                                          ^
*/
  if (!ba0_sign_token_analex (")"))
    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBOR);

  bav_R_push_ordering (r);
  for (i = V->size - 1; i >= 0; i--)
    bav_R_set_maximal_variable (V->tab[i]);
  bav_R_pull_ordering ();

  ba0_restore (&M);
  ba0_pull_stack ();

  if (z != (void *) 0)
    *(bav_Iordering *) z = r;

  return (void *) r;
}

/*
 * texinfo: bav_printf_ordering
 * The printing function for orderings.
 * It is called by @code{ba0_printf/%ordering}.
 */

BAV_DLL void
bav_printf_ordering (
    void *z)
{
  bav_Iordering r = (bav_Iordering) z;
  bav_ordering O;
  struct ba0_mark M;

  ba0_record (&M);

  bav_R_push_ordering (r);

  O = bav_R_ordering ();

  ba0_printf ("%s ", bav_initialized_global.ordering.string);

  ba0_put_char ('(');
  ba0_printf ("derivations = %t[%y]", &O->ders);
  ba0_printf (", blocks = %t[%b]", &O->blocks);
  if (O->operator_block.strs.size > 0)
    ba0_printf (", operator = %b", &O->operator_block);
  if (O->varmax.size != 0)
    ba0_printf (", varmax = %t[%v]", &O->varmax);
  ba0_put_char (')');

  bav_R_pull_ordering ();
  ba0_restore (&M);
}
