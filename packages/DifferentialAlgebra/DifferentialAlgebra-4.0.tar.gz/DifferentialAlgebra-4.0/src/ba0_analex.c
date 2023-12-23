#include "ba0_exception.h"
#include "ba0_stack.h"
#include "ba0_basic_io.h"
#include "ba0_analex.h"
#include "ba0_global.h"
#include "ba0_int_p.h"

#define ba0_analex_save_full ba0_global.analex.analex_save_full
#define ba0_analex	     ba0_global.analex.analex
#define ba0_analex_save	     ba0_global.analex.analex_save
#define ba0_nbtokens	     ba0_initialized_global.analex.nb_tokens
#define ba0_context_analex   ba0_global.analex.context

/*
 * A zero value restores the setting.
 * The parser of doubles requires a fifo of at least 7 tokens.
 */

/*
 * texinfo: ba0_set_settings_analex
 * Set to @var{nbtokens} the length of the fifo used by the lexical analyzer.
 * This number is not allowed to be less than @math{10}.
 * A zero value resets the length to its default value.
 * This function must be called outside sequences of calls to the library.
 */

BA0_DLL void
ba0_set_settings_analex (
    ba0_int_p nbtokens)
{
  ba0_nbtokens = nbtokens >= BA0_NBTOKENS ? nbtokens : BA0_NBTOKENS;
}

/*
 * texinfo: ba0_get_settings_analex
 * Assign to *@var{nbtokens} the length of the fifo used by the lexical analyzer.
 * Pointers are allowed to be zero.
 */

BA0_DLL void
ba0_get_settings_analex (
    ba0_int_p *nbtokens)
{
  if (nbtokens)
    *nbtokens = ba0_nbtokens;
}

/*
 * texinfo: ba0_get_context_analex
 * Return the address of the global variable @code{ba0_context_analex}.
 */

BA0_DLL char *
ba0_get_context_analex (
    void)
{
  return ba0_context_analex;
}

/*
 * Writes the content of the fifo in ba0_context_analex
 * The current token is enclosed between --> and <--
 */

/*
 * texinfo: ba0_write_context_analex
 * Print the current token in the global variable @code{ba0_context_analex}.
 * The token is enclosed between @code{-->} and @code{<--}.
 * Some previous tokens are printed before.
 * If the input is not a @emph{tty}, some next tokens are printed
 * afterwards.
 * The string @code{ba0_context_analex} can be used for printing
 * helpful messages when an error occurs at parsing time.
 * This function is called by @code{BA0_RAISE_PARSER_EXCEPTION}.
 */

BA0_DLL void
ba0_write_context_analex (
    void)
{
  ba0_int_p l, l_unget, n_unget, n_get;

  ba0_context_analex[0] = '\0';

  if (ba0_type_token_analex () == ba0_no_token)
    return;

  l = strlen (ba0_value_token_analex ()) + strlen (" -->  <-- ");
  if (l >= BA0_CONTEXT_LMAX - 1)
    return;

  n_unget = 0;
  l_unget = 0;
  for (;;)
    {
      if (ba0_analex.first == (ba0_analex.last + 1) % ba0_nbtokens)
        break;
      ba0_unget_token_analex (1);
      n_unget += 1;
      if (ba0_type_token_analex () == ba0_no_token)
        {
          ba0_get_token_analex ();
          n_unget -= 1;
          break;
        }
      l_unget += strlen (ba0_value_token_analex ());
      if (ba0_analex.fifo[ba0_analex.first].spaces_before)
        l_unget += 1;
      if (l + l_unget >= 2 * BA0_CONTEXT_LMAX / 3 - 1)
        {
          ba0_get_token_analex ();
          n_unget -= 1;
          break;
        }
    }
  while (n_unget > 0)
    {
      if (ba0_analex.fifo[ba0_analex.first].spaces_before)
        strcat (ba0_context_analex, " ");
      strcat (ba0_context_analex, ba0_value_token_analex ());
      ba0_get_token_analex ();
      n_unget -= 1;
    }
  strcat (ba0_context_analex, " --> ");
  strcat (ba0_context_analex, ba0_value_token_analex ());
  strcat (ba0_context_analex, " <-- ");
  if (ba0_isatty_input ())
    return;
  n_get = 0;
  for (;;)
    {
      if (n_get == ba0_nbtokens - 1)
        break;
      ba0_get_token_analex ();
      n_get += 1;
      if (ba0_type_token_analex () == ba0_no_token)
        {
          ba0_unget_token_analex (1);
          n_get -= 1;
          break;
        }
      if (strlen (ba0_context_analex) +
          strlen (ba0_value_token_analex ()) + 1 >= BA0_CONTEXT_LMAX - 1)
        {
          ba0_unget_token_analex (1);
          n_get -= 1;
          break;
        }
      if (ba0_spaces_before_token_analex ())
        strcat (ba0_context_analex, " ");
      strcat (ba0_context_analex, ba0_value_token_analex ());
    }
  ba0_unget_token_analex (n_get);
}

/*
 * texinfo: ba0_record_analex
 * Record the value of the current lexical analyzer for future restoration.
 * Exception @code{BA0_ERRSOV} is raised if the saving variable is full.
 */

BA0_DLL void
ba0_record_analex (
    void)
{
  if (ba0_analex_save_full)
    BA0_RAISE_EXCEPTION (BA0_ERRSOV);
  ba0_record_input ();
  ba0_analex_save.first = ba0_analex.first;
  ba0_analex_save.last = ba0_analex.last;
  memcpy (ba0_analex_save.fifo, ba0_analex.fifo,
      ba0_nbtokens * sizeof (struct ba0_token));
  ba0_analex_save_full = true;
}

/*
 * texinfo: ba0_restore_analex
 * Restore the value of the current lexical analyzer saved by the above function.
 * Exception @code{BA0_ERRSOV} is raised if the saving variable is empty.
 */

BA0_DLL void
ba0_restore_analex (
    void)
{
  if (!ba0_analex_save_full)
    BA0_RAISE_EXCEPTION (BA0_ERRSOV);
  ba0_restore_input ();
  ba0_analex.first = ba0_analex_save.first;
  ba0_analex.last = ba0_analex_save.last;
  memcpy (ba0_analex.fifo, ba0_analex_save.fifo,
      ba0_nbtokens * sizeof (struct ba0_token));
  ba0_analex_save_full = false;
}

/*
 * nb_tokens must not be modified between init and clear.
 */

/*
 * texinfo: ba0_init_analex
 * Initialize the lexical analyzer.
 * The counter of calls to @code{ba0_get_token_analex} is reset to zero.
 */

BA0_DLL void
ba0_init_analex (
    void)
{
  ba0_int_p analex;

  ba0_get_settings_stack (0, 0, &analex, 0, 0);
  ba0_analex.fifo = (struct ba0_token *) ba0_malloc
      (ba0_nbtokens * sizeof (struct ba0_token));
  ba0_analex_save.fifo = (struct ba0_token *) ba0_malloc
      (ba0_nbtokens * sizeof (struct ba0_token));
  ba0_reset_analex ();
}

/*
 * texinfo: ba0_clear_analex
 * Free the resources allocated to the lexical analyzer.
 */

BA0_DLL void
ba0_clear_analex (
    void)
{
  ba0_free (ba0_analex.fifo);
  ba0_free (ba0_analex_save.fifo);
  ba0_malloc_counter -= 2 * ba0_nbtokens * sizeof (struct ba0_token);
}

static void
ba0_empty_analex (
    void)
{
  ba0_int_p i;

  for (i = 0; i < ba0_nbtokens; i++)
    {
      ba0_analex.fifo[i].type = ba0_no_token;
      ba0_analex.fifo[i].spaces_before = true;
      ba0_analex.fifo[i].value = (char *) 0;
    }
  ba0_analex.first = 0;
  ba0_analex.last = 0;
  ba0_analex.counter = 0;
  ba0_context_analex[0] = '\0';
}

/*
 * texinfo: ba0_reset_analex
 * Reset the lexical analyzer. Recorded lexical analyzers are erased.
 * the stack @code{ba0_global.stack.analex} is cleaned. 
 * The function @code{ba0_reset_input} is called.
 * The string @code{ba0_context_analex} is cleared.
 * The counter of calls to @code{ba0_get_token_analex} is reset to zero.
 */

BA0_DLL void
ba0_reset_analex (
    void)
{
  ba0_reset_input ();
  ba0_empty_analex ();
  ba0_analex_save_full = false;
  ba0_reset_stack (&ba0_global.stack.analex);
}

/*
 * texinfo: ba0_set_analex_FILE
 * Initialize the lexical analyzer. The input stream is now read in @var{f}.
 * The counter of calls to @code{ba0_get_token_analex} is reset to zero.
 */

BA0_DLL void
ba0_set_analex_FILE (
    FILE *f)
{
  ba0_set_input_FILE (f);
  ba0_empty_analex ();
}

/*
 * texinfo: ba0_set_analex_string
 * Initialize the lexical analyzer. The input stream is now read in @var{s}.
 * The counter of calls to @code{ba0_get_token_analex} is reset to zero.
 */

BA0_DLL void
ba0_set_analex_string (
    char *s)
{
  ba0_set_input_string (s);
  ba0_empty_analex ();
}

/*
 * Subfunction of realloc_token
 *
 * We are about to allocate a new cell.
 * Before to do that, we pick the unused cells which appear before the
 * current cell and move them to the end of ba0_global.stack.analex.cells
 *
 * This is a very important process, which permits analex to use
 * a small amount of memory.
 */

static void
rotate_free_cells (
    void)
{
  struct ba0_tableof_int_p libre;
  struct ba0_mark M;
  ba0_int_p free_index, i, j;

  free_index = ba0_global.stack.analex.free.index_in_cells;
  if (free_index < 1)
    return;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_table ((ba0_table) & libre);
  ba0_realloc_table ((ba0_table) & libre, free_index);
  ba0_pull_stack ();

  for (i = 0; i < free_index; i++)
    {
      libre.tab[libre.size] = true;
      libre.size += 1;
    }

  for (i = 0; i < ba0_nbtokens; i++)
    {
      if (ba0_analex.fifo[i].type != ba0_no_token)
        {
          j = ba0_cell_index_mark
              (ba0_analex.fifo[i].value, &ba0_global.stack.analex.free);
          if (j == -1)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          else if (j < free_index)
            libre.tab[j] = false;
        }
    }
  if (ba0_analex_save_full)
    {
      for (i = 0; i < ba0_nbtokens; i++)
        {
          if (ba0_analex_save.fifo[i].type != ba0_no_token)
            {
              j = ba0_cell_index_mark
                  (ba0_analex_save.fifo[i].value,
                  &ba0_global.stack.analex.free);
              if (j == -1)
                BA0_RAISE_EXCEPTION (BA0_ERRALG);
              else if (j < free_index)
                libre.tab[j] = false;
            }
        }
    }

  for (i = free_index - 1; i >= 0; i--)
    {
      if (libre.tab[i])
        ba0_rotate_cells (i);
    }
  ba0_restore (&M);
}

/*
 * Starts the process of token extraction.
 * See the two following functions.
 *
 * The mark M and ba0_analex.fifo [ba0_analex.last].value are modified
 * in order to point to the same area. All the available memory of
 * the current cell is allocated for the token. The amount of memory
 * is returned.
 */

static unsigned ba0_int_p
start_token (
    struct ba0_mark *M)
{
  unsigned ba0_int_p available;

  ba0_record (M);
  available = ba0_memory_left_in_cell ();
  ba0_analex.fifo[ba0_analex.last].value = (char *) ba0_alloc (available);
  return available;
}

/*
 * The mark M and ba0_analex.fifo [ba0_analex.last].value point to the same
 * address. The beginning of a token has been extracted and stored at this
 * address. It has length: length.
 *
 * Memory is however, missing.
 *
 * A new cell, large enough, is allocated (or recovered).
 *
 * The mark M and ba0_analex.fifo [ba0_analex.last].value are set to
 * the beginning of this cell. All the available memory of the cell is
 * allocated for the token. 
 *
 * The existing part of the token is copied in the new area.
 *
 * The amount of available memory in the cell is returned.
 */

static unsigned ba0_int_p
realloc_token (
    struct ba0_mark *M,
    ba0_int_p length)
{
  unsigned ba0_int_p available;
  char *p;

  p = ba0_analex.fifo[ba0_analex.last].value;

  rotate_free_cells ();
/* At least 2 bytes are allocated */
  ba0_alloc (2 * length + 2);
  ba0_reset_cell_stack (ba0_current_stack ());

  ba0_record (M);
  available = ba0_memory_left_in_cell ();
  ba0_analex.fifo[ba0_analex.last].value = (char *) ba0_alloc (available);

  if (length > 0)
    memcpy (ba0_analex.fifo[ba0_analex.last].value, p, length);

  return available;
}

/*
 * The mark M points to the beginning of the token which is just extracted.
 * The token has length: length.
 * The allocated block is shrinked to the length of the token.
 */

static void
finish_token (
    struct ba0_mark *M,
    ba0_int_p length)
{
  ba0_restore (M);
  ba0_alloc (length);
}

/*
 * texinfo: ba0_get_counter_analex
 * Return the current value of the counter of calls 
 * to @code{ba0_get_token_analex}. 
 */

BA0_DLL ba0_int_p
ba0_get_counter_analex (
    void)
{
  return ba0_analex.counter;
}

/*
 * Extracts one token and stores it in the FIFO.
 */

/*
 * texinfo: ba0_get_token_analex
 * Read a new token on the input stream.
 * The counter of calls to @code{ba0_get_token_analex} is increased by @math{1}.
 * If the input stream is empty then the current token receives the
 * type @code{ba0_no_token}.
 */

BA0_DLL void
ba0_get_token_analex (
    void)
{
  struct ba0_mark M;
  unsigned ba0_int_p available;
  ba0_int_p i;
  bool spaces_before;
  int chrin;

  if (ba0_analex.first != ba0_analex.last)
    ba0_analex.first = (ba0_analex.first + 1) % ba0_nbtokens;
  else
    {
/* Read a char (skip spaces) */
      spaces_before = false;
      do
        {
          do
            {
              chrin = ba0_get_char ();
              if (isspace (chrin))
                spaces_before = true;
            }
          while (chrin != EOF && isspace (chrin));
          if (chrin == '#')
            {
              spaces_before = true;
              do
                chrin = ba0_get_char ();
              while (chrin != EOF && chrin != '\n');
            }
        }
      while (isspace (chrin));
/* Extract the token */
      ba0_push_stack (&ba0_global.stack.analex);

      ba0_analex.first = (ba0_analex.first + 1) % ba0_nbtokens;
      ba0_analex.last = ba0_analex.first;
/* 
 * start_token makes the mark M and ba0_analex.fifo [ba0_analex.last].value
 * point to the same area. 
 * available is the amount of memory available for the token to be extracted.
 */
      available = start_token (&M);
/*
 * realloc_token is called when the amount of memory available is not enough.
 * It allocates a big piece of memory, copies the current part of the
 * token in this memory, moves ba0_analex.fifo [ba0_analex.last].value and
 * the mark M to the beginning of the new piece of memory.
 */
      if (chrin == EOF)
        {
          if (available == 0)
            available = realloc_token (&M, 0);
          ba0_analex.fifo[ba0_analex.last].value[0] = '\0';
          ba0_analex.fifo[ba0_analex.last].spaces_before = spaces_before;
          ba0_analex.fifo[ba0_analex.last].type = ba0_no_token;
/*
 * finish_token resizes the piece of memory allocated to the token
 */
          finish_token (&M, 1);
        }
      else if (isdigit (chrin))
        {
          for (i = 0; isdigit (chrin); i++)
            {
              if (available == (unsigned ba0_int_p) i)
                available = realloc_token (&M, i);
              ba0_analex.fifo[ba0_analex.last].value[i] = chrin;
              chrin = ba0_get_char ();
            }
          ba0_unget_char (chrin);
          if (available == (unsigned ba0_int_p) i)
            available = realloc_token (&M, i);
          ba0_analex.fifo[ba0_analex.last].value[i] = '\0';
          ba0_analex.fifo[ba0_analex.last].spaces_before = spaces_before;
          ba0_analex.fifo[ba0_analex.last].type = ba0_integer_token;
          finish_token (&M, i + 1);
        }
      else if (isalpha (chrin) || chrin == '_')
        {
          for (i = 0; isalnum (chrin) || chrin == '_'; i++)
            {
              if (available == (unsigned ba0_int_p) i)
                available = realloc_token (&M, i);
              ba0_analex.fifo[ba0_analex.last].value[i] = chrin;
              chrin = ba0_get_char ();
            }
          ba0_unget_char (chrin);
          if (available == (unsigned ba0_int_p) i)
            available = realloc_token (&M, i);
          ba0_analex.fifo[ba0_analex.last].value[i] = '\0';
          ba0_analex.fifo[ba0_analex.last].spaces_before = spaces_before;
          ba0_analex.fifo[ba0_analex.last].type = ba0_string_token;
          finish_token (&M, i + 1);
        }
      else if (chrin == '"')
        {
          chrin = ba0_get_char ();
          for (i = 0; chrin != EOF && chrin != '"'; i++)
            {
              if (available == (unsigned ba0_int_p) i)
                available = realloc_token (&M, i);
              ba0_analex.fifo[ba0_analex.last].value[i] = chrin;
              chrin = ba0_get_char ();
            }
          if (chrin != '"')
            ba0_unget_char (chrin);
          if (available == (unsigned ba0_int_p) i)
            available = realloc_token (&M, i);
          ba0_analex.fifo[ba0_analex.last].value[i] = '\0';
          ba0_analex.fifo[ba0_analex.last].spaces_before = spaces_before;
          ba0_analex.fifo[ba0_analex.last].type = ba0_string_token;
          finish_token (&M, i + 1);
        }
      else
        {
          if (available < 2)
            available = realloc_token (&M, 0);
          ba0_analex.fifo[ba0_analex.last].value[0] = chrin;
          ba0_analex.fifo[ba0_analex.last].value[1] = '\0';
          ba0_analex.fifo[ba0_analex.last].spaces_before = spaces_before;
          ba0_analex.fifo[ba0_analex.last].type = ba0_sign_token;
          finish_token (&M, 2);
        }

      ba0_pull_stack ();
    }
  ba0_analex.counter += 1;
}

/*
 * texinfo: ba0_unget_token_analex
 * Replace the @var{n} previous tokens on the input stream.
 * The counter of calls to @code{ba0_get_token_analex} is decreased by @var{n}.
 */

BA0_DLL void
ba0_unget_token_analex (
    ba0_int_p n)
{
  ba0_int_p i;

  for (i = 0; i < n; i++)
    {
      ba0_analex.first = (ba0_analex.first + ba0_nbtokens - 1) % ba0_nbtokens;
      ba0_analex.counter -= 1;
    }
}

/*
 * texinfo: ba0_unget_given_token_analex
 * The current token i erased.
 * Its value is replaced by @var{value} and @var{type}.
 * The next call to @code{ba0_get_token_analex} will read it.
 * The boolean @var{spaces_before} indicates if it must be considered 
 * that at least one space was skipped before reading the token value
 * (see @code{ba0_spaces_before_token_analex}).
 * A copy of the string @var{value} is stored in the memory used by the analyzer.
 * The counter of calls to @code{ba0_get_token_analex} is decreased by @math{1}.
 */

BA0_DLL void
ba0_unget_given_token_analex (
    char *value,
    enum ba0_typeof_token type,
    bool spaces_before)
{
  ba0_int_p len;

  ba0_push_stack (&ba0_global.stack.analex);

/* Rotate cells if needed */

  len = strlen (value);
  if (ba0_memory_left_in_cell () < (unsigned ba0_int_p) len + 1)
    rotate_free_cells ();

  ba0_analex.fifo[ba0_analex.first].value = (char *) ba0_alloc (len + 1);
  strcpy (ba0_analex.fifo[ba0_analex.first].value, value);
  ba0_analex.fifo[ba0_analex.first].type = spaces_before;
  ba0_analex.fifo[ba0_analex.first].type = type;

  ba0_analex.first = (ba0_analex.first + ba0_nbtokens - 1) % ba0_nbtokens;

  ba0_pull_stack ();
  ba0_analex.counter -= 1;
}

/*
 * texinfo: ba0_sign_token_analex
 * Return @code{true} is the current token has type @code{ba0_sign_token}
 * and is equal to @var{s}.
 */

BA0_DLL bool
ba0_sign_token_analex (
    char *s)
{
  if (ba0_analex.fifo[ba0_analex.first].type != ba0_sign_token)
    return false;
  else
    return strcmp (s, ba0_analex.fifo[ba0_analex.first].value) == 0;
}

/*
 * texinfo: ba0_spaces_before_token_analex
 * Return @code{true} if at least one space was skipped 
 * before reading the value of the current token. 
 * Observe that comments are not considered as spaces.
 */

BA0_DLL bool
ba0_spaces_before_token_analex (
    void)
{
  return ba0_analex.fifo[ba0_analex.first].spaces_before;
}

/*
 * texinfo: ba0_type_token_analex
 * Return the type of the current token.
 */

BA0_DLL enum ba0_typeof_token
ba0_type_token_analex (
    void)
{
  return ba0_analex.fifo[ba0_analex.first].type;
}

/*
 * texinfo: ba0_value_token_analex
 * Return the value of the current token i.e. the string read on the input
 * stream (whatever the type of the token). The memory used by the returned
 * string is reused by the lexical analyzer after @var{n} calls to
 * @code{ba0_get_token_analex} (where @var{n} denotes the length of the
 * fifo used by the analyzer).
 */

BA0_DLL char *
ba0_value_token_analex (
    void)
{
  return ba0_analex.fifo[ba0_analex.first].value;
}
