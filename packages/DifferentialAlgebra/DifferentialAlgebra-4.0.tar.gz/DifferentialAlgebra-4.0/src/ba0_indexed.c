#include "ba0_global.h"
#include "ba0_exception.h"
#include "ba0_stack.h"
#include "ba0_garbage.h"
#include "ba0_string.h"
#include "ba0_basic_io.h"
#include "ba0_analex.h"
#include "ba0_gmp.h"
#include "ba0_scanf.h"
#include "ba0_printf.h"
#include "ba0_table.h"
#include "ba0_indexed.h"

/*
 * For parsing complicated (indexed) strings
 *
 * INDEXED ::= string INDICES ... INDICES              (*)
 *         ::= signed integer INDICES ... INDICES
 *         ::= INDICES ... INDICES
 *
 * INDICES ::= (INDEXED, ..., INDEXED)
 *         ::= [INDEXED, ..., INDEXED]
 *
 *
 * (*) At top level, this form is the only one accepted.
 *                   the last "INDICES" plays a special role.
 */

static void
ba0_init_indices (
    ba0_indices indices)
{
  indices->po = indices->pf = '\0';
  ba0_init_table ((ba0_table) & indices->Tindex);
}

static void
ba0_reset_indices (
    ba0_indices indices)
{
  indices->po = indices->pf = '\0';
  ba0_reset_table ((ba0_table) & indices->Tindex);
}

static ba0_indices
ba0_new_indices (
    void)
{
  ba0_indices indices;

  indices = (ba0_indices) ba0_alloc (sizeof (struct ba0_indices));
  ba0_init_indices (indices);
  return indices;
}

static void
ba0_realloc_indices (
    ba0_indices indices,
    ba0_int_p n)
{
  ba0_realloc2_table ((ba0_table) & indices->Tindex, n,
      (ba0_new_function *) & ba0_new_indexed);
}

static void
ba0_set_indices (
    ba0_indices dst,
    ba0_indices src)
{
  if (dst != src)
    {
      ba0_reset_indices (dst);
      ba0_realloc_indices (dst, src->Tindex.size);
      dst->po = src->po;
      dst->pf = src->pf;
      while (dst->Tindex.size < src->Tindex.size)
        {
          ba0_set_indexed (dst->Tindex.tab[dst->Tindex.size],
              src->Tindex.tab[dst->Tindex.size]);
          dst->Tindex.size += 1;
        }
    }
}

/*
 * Readonly static data
 */

static char _struct_indices[] = "struct indices";
static char _indices_Tindex[] = "indices Tindex";

static ba0_int_p
ba0_garbage1_indices (
    void *z,
    enum ba0_garbage_code code)
{
  ba0_indices ind = (ba0_indices) z;
  ba0_int_p i, n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (ind, sizeof (struct ba0_indices), _struct_indices);
  if (ind->Tindex.tab)
    {
      n += ba0_new_gc_info (ind->Tindex.tab,
          sizeof (ba0_indexed) * ind->Tindex.alloc, _indices_Tindex);
      for (i = 0; i < ind->Tindex.alloc; i++)
        n += ba0_garbage1_indexed (ind->Tindex.tab[i], ba0_isolated);
    }
  return n;
}

static void *
ba0_garbage2_indices (
    void *z,
    enum ba0_garbage_code code)
{
  ba0_indices ind;
  ba0_int_p i;

  if (code == ba0_isolated)
    ind = (ba0_indices) ba0_new_addr_gc_info (z, _struct_indices);
  else
    ind = (ba0_indices) z;

  if (ind->Tindex.tab)
    {
      ind->Tindex.tab = (ba0_indexed *) ba0_new_addr_gc_info
          (ind->Tindex.tab, _indices_Tindex);
      for (i = 0; i < ind->Tindex.alloc; i++)
        ind->Tindex.tab[i] = (ba0_indexed) ba0_garbage2_indexed
            (ind->Tindex.tab[i], ba0_isolated);
    }
  return ind;
}

BA0_DLL void
ba0_init_indexed (
    ba0_indexed indexed)
{
  indexed->string = (char *) 0;
  ba0_init_table ((ba0_table) & indexed->Tindic);
}

BA0_DLL void
ba0_reset_indexed (
    ba0_indexed indexed)
{
  indexed->string = (char *) 0;
  ba0_reset_table ((ba0_table) & indexed->Tindic);
}

BA0_DLL ba0_indexed
ba0_new_indexed (
    void)
{
  ba0_indexed indexed;

  indexed = (ba0_indexed) ba0_alloc (sizeof (struct ba0_indexed));
  ba0_init_indexed (indexed);
  return indexed;
}

static void
ba0_realloc_indexed (
    ba0_indexed indexed,
    ba0_int_p n)
{
  ba0_realloc2_table ((ba0_table) & indexed->Tindic, n,
      (ba0_new_function *) & ba0_new_indices);
}

BA0_DLL void
ba0_set_indexed (
    ba0_indexed dst,
    ba0_indexed src)
{
  if (dst != src)
    {
      ba0_reset_indexed (dst);
      dst->string = ba0_strdup (src->string);
      ba0_realloc_indexed (dst, src->Tindic.size);
      while (dst->Tindic.size < src->Tindic.size)
        {
          ba0_set_indices (dst->Tindic.tab[dst->Tindic.size],
              src->Tindic.tab[dst->Tindic.size]);
          dst->Tindic.size += 1;
        }
    }
}

BA0_DLL void *
ba0_copy_indexed (
    void *z)
{
  ba0_indexed src = (ba0_indexed) z;
  ba0_indexed dst;

  dst = ba0_new_indexed ();
  ba0_set_indexed (dst, src);
  return dst;
}

/*
 * Readonly static data
 */

static char _struct_indexed[] = "struct indexed";
static char _indexed_Tindic[] = "indexed Tindic";

BA0_DLL ba0_int_p
ba0_garbage1_indexed (
    void *z,
    enum ba0_garbage_code code)
{
  ba0_indexed ind = (ba0_indexed) z;
  ba0_int_p i, n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (ind, sizeof (struct ba0_indexed), _struct_indexed);
  if (ind->string)
    n += ba0_garbage1_string (ind->string, ba0_isolated);
  if (ind->Tindic.tab)
    {
      n += ba0_new_gc_info (ind->Tindic.tab,
          sizeof (ba0_indices) * ind->Tindic.alloc, _indexed_Tindic);
      for (i = 0; i < ind->Tindic.alloc; i++)
        n += ba0_garbage1_indices (ind->Tindic.tab[i], ba0_isolated);
    }
  return n;
}

BA0_DLL void *
ba0_garbage2_indexed (
    void *z,
    enum ba0_garbage_code code)
{
  ba0_indexed ind;
  ba0_int_p i;

  if (code == ba0_isolated)
    ind = (ba0_indexed) ba0_new_addr_gc_info (z, _struct_indexed);
  else
    ind = (ba0_indexed) z;

  if (ind->string)
    ind->string = (char *) ba0_garbage2_string (ind->string, ba0_isolated);
  if (ind->Tindic.tab)
    {
      ind->Tindic.tab = (ba0_indices *) ba0_new_addr_gc_info
          (ind->Tindic.tab, _indexed_Tindic);
      for (i = 0; i < ind->Tindic.alloc; i++)
        ind->Tindic.tab[i] = (ba0_indices) ba0_garbage2_indices
            (ind->Tindic.tab[i], ba0_isolated);
    }
  return ind;
}

/*
 * The important functions
 */

static void
ba0_printf_indices (
    void *z)
{
  ba0_indices indices = (ba0_indices) z;
  ba0_int_p i;

  if (indices->po)
    ba0_put_char (indices->po);
  for (i = 0; i < indices->Tindex.size; i++)
    {
      ba0_printf_indexed (indices->Tindex.tab[i]);
      if (i < indices->Tindex.size - 1)
        ba0_put_char (',');
    }
  if (indices->pf)
    ba0_put_char (indices->pf);
}

/*
 * texinfo: ba0_printf_indexed
 * Print the @code{ba0_indexed} @var{z}.
 */

BA0_DLL void
ba0_printf_indexed (
    void *z)
{
  ba0_indexed indexed = (ba0_indexed) z;
  ba0_int_p i;

  if (indexed->string)
    ba0_put_string (indexed->string);
  for (i = 0; i < indexed->Tindic.size; i++)
    ba0_printf_indices (indexed->Tindic.tab[i]);
}

/*
 * Prints an indexed in a string and returns it.
 * This string is not protected from garbage collection.
 */

/*
 * texinfo: ba0_indexed_to_string
 * Print @var{indexed} in a string (allocated by @code{ba0_alloc})
 * and returns it.
 */

BA0_DLL char *
ba0_indexed_to_string (
    ba0_indexed indexed)
{
  char *string;
  ba0_record_output ();
  ba0_set_output_counter ();
  ba0_printf_indexed (indexed);
  string = (char *) ba0_alloc (ba0_output_counter () + 1);
  ba0_set_output_string (string);
  ba0_printf_indexed (indexed);
  ba0_restore_output ();
  return string;
}

static ba0_indexed ba0_scanf_general_indexed (
    ba0_indexed,
    bool *,
    bool (*)(char *));
/*
 * Reads one INDICES.
 *
 * lder = true if each INDEXED occuring in the INDICES satisfies isder.
 *
 * Typically, these parameters are used to check if INDICES is made
 * of a sequence of independent variables which might denote a derivation
 * operator.
 *
 * Parameters lder and isder may be zero.
 * isder is assumed nonzero whenever lder is nonzero.
 */

static ba0_indices
ba0_scanf_indices (
    ba0_indices indices,
    bool *lder,
    bool (*isder) (char *))
{
  ba0_indexed indexed;

  if (indices != (ba0_indices) 0)
    ba0_reset_indices (indices);
  else
    indices = ba0_new_indices ();

  if (!ba0_sign_token_analex ("[") && !ba0_sign_token_analex ("("))
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  if (ba0_sign_token_analex ("["))
    {
      indices->po = '[';
      indices->pf = ']';
    }
  else
    {
      indices->po = '(';
      indices->pf = ')';
    }
  ba0_get_token_analex ();
  for (;;)
    {
      if (indices->Tindex.size >= indices->Tindex.alloc)
        ba0_realloc_indices (indices, 2 * indices->Tindex.size + 1);
      indexed = ba0_scanf_general_indexed
          (indices->Tindex.tab[indices->Tindex.size], 0, 0);

      if (indexed == (ba0_indexed) 0)
        break;

      if (lder && *lder)
        {
          struct ba0_mark M;
          char *string;
          ba0_record (&M);
          string = ba0_indexed_to_string (indexed);
          *lder = (*isder) (string);
          ba0_restore (&M);
        }

      indices->Tindex.size += 1;
      ba0_get_token_analex ();
      if (!ba0_sign_token_analex (","))
        break;
      ba0_get_token_analex ();
    }
  if ((indices->po == '[' && !ba0_sign_token_analex ("]")) ||
      (indices->po == '(' && !ba0_sign_token_analex (")")))
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);
/*
 * An empty list is a derivation list
 */
  else if (indices->Tindex.size == 0 && lder)
    *lder = true;
  return indices;
}

/*
 * Reads INDICES ... INDICES
 *
 * If lder and isder are nonzero, they apply to the last INDICES
 */

static void
ba0_scanf_tableof_indices (
    ba0_indexed indexed,
    bool *lder,
    bool (*isder) (char *))
{
  bool once;

  once = false;
  if (lder)
    *lder = false;
  while ((ba0_sign_token_analex ("[") || ba0_sign_token_analex ("(")))
    {
      once = true;
      if (indexed->Tindic.size >= indexed->Tindic.alloc)
        ba0_realloc_indexed (indexed, 2 * indexed->Tindic.size + 1);
      if (lder)
        *lder = true;
      ba0_scanf_indices
          (indexed->Tindic.tab[indexed->Tindic.size], lder, isder);
      indexed->Tindic.size += 1;
      ba0_get_token_analex ();
    }
  if (once)
    ba0_unget_token_analex (1);
}

/*
 * Reads zero or one INDEXED.
 *
 * Returns the zero pointer if no INDEXED is read.
 *
 * lder = true if the last INDICES is a sequence of INDEXED satisfying
 * isder, surrounded by brackets or parentheses.
 */

static ba0_indexed
ba0_scanf_general_indexed (
    ba0_indexed indexed,
    bool *lder,
    bool (*isder) (char *))
{
  struct ba0_mark M;
  ba0_mpz_t n;

  if (indexed != (ba0_indexed) 0)
    ba0_reset_indexed (indexed);
  else
    indexed = ba0_new_indexed ();

  if (ba0_type_token_analex () == ba0_string_token)
    {
      indexed->string = ba0_scanf_string (0);
      ba0_get_token_analex ();
      if (ba0_sign_token_analex ("[") || ba0_sign_token_analex ("("))
        ba0_scanf_tableof_indices (indexed, lder, isder);
      else
        {
          ba0_unget_token_analex (1);
          if (lder)
            *lder = false;
        }
    }
  else if (ba0_type_token_analex () == ba0_integer_token ||
      ba0_sign_token_analex ("-"))
    {
      ba0_push_another_stack ();
      ba0_record (&M);
      ba0_mpz_init (n);
      ba0_scanf ("%z", n);
      ba0_record_output ();
      ba0_set_output_counter ();
      ba0_printf ("%z", n);
      ba0_pull_stack ();
      indexed->string = (char *) ba0_alloc (ba0_output_counter () + 1);
      ba0_restore_output ();
      ba0_sprintf (indexed->string, "%z", n);
      ba0_restore (&M);
      if (lder)
        *lder = false;
    }
  else if (ba0_sign_token_analex ("[") || ba0_sign_token_analex ("("))
    {
      ba0_scanf_tableof_indices (indexed, (bool *) 0, 0);
      if (lder)
        *lder = false;
    }
  else
    indexed = (ba0_indexed) 0;

  return indexed;
}

/*
 * texinfo: ba0_scanf_indexed
 * Read one @code{INDEXED} starting by a string and stores it in @var{indexed}.
 * *@var{lder} is set to @code{true} if the last @code{INDICES} is itself
 * a sequence of @code{INDEXED} satisfying the function pointed to by
 * @var{isder} (the sequence being surrounded by square brackets or
 * parentheses). Parameters @var{lder} and @var{isder} may be zero.
 * They can be used to determine if the last @code{INDICES} is a sequence
 * of independent variables denoting a derivation operator (see the @code{bav}
 * library). Exception @code{BA0_ERRSYN} can be raised.
 */

BA0_DLL ba0_indexed
ba0_scanf_indexed (
    ba0_indexed indexed,
    bool *lder,
    bool (*isder) (char *))
{
  ba0_indexed result = (ba0_indexed) 0;
  bool b;

  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  b = ba0_initialized_global.gmp.protect_from_evaluation;
  ba0_initialized_global.gmp.protect_from_evaluation = false;
  BA0_TRY
  {
    result = ba0_scanf_general_indexed (indexed, lder, isder);
    ba0_initialized_global.gmp.protect_from_evaluation = b;
  }
  BA0_CATCH
  {
    ba0_initialized_global.gmp.protect_from_evaluation = b;
    BA0_RE_RAISE_EXCEPTION;
  }
  BA0_ENDTRY;
  return result;
}

/*
 * texinfo: ba0_scanf_raw_indexed
 * Call the above function with @var{lder} and @var{isder} being zero.
 * Returns the result as a @code{ba0_indexed}.
 * Stores it in *@var{z} if this parameter is nonzero.
 */

BA0_DLL void *
ba0_scanf_raw_indexed (
    void *z)
{
  ba0_indexed ind;

  if (z == (void *) 0)
    ind = ba0_new_indexed ();
  else
    ind = (ba0_indexed) z;
  ba0_scanf_indexed (ind, (bool *) 0, 0);
  return ind;
}

/*
 * Reads an INDEXED.
 *
 * Calls the above function with lder = isder = 0.
 * The current token is a string.
 *
 * The result is a string.
 */

/*
 * texinfo: ba0_scanf_indexed_string
 * Call the above function with @var{lder} and @var{isder} being zero.
 * Returns the result as a string. 
 * Stores it in *@var{z} if this parameter is nonzero.
 */

BA0_DLL void *
ba0_scanf_indexed_string (
    void *z)
{
  char *result;
  ba0_indexed indexed;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  indexed = ba0_scanf_indexed ((ba0_indexed) 0, (bool *) 0, 0);
  ba0_pull_stack ();

  if (z != (void *) 0)
    result = (char *) z;
  else
    {
      ba0_record_output ();
      ba0_set_output_counter ();
      ba0_printf_indexed (indexed);
      result = (char *) ba0_alloc (ba0_output_counter () + 1);
      ba0_restore_output ();
    }
  ba0_record_output ();
  ba0_set_output_string (result);
  ba0_printf_indexed (indexed);
  ba0_restore_output ();
  ba0_restore (&M);
  return result;
}
