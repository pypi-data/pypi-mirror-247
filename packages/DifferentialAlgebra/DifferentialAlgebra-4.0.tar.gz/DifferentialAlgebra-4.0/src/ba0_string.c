#include "ba0_exception.h"
#include "ba0_stack.h"
#include "ba0_string.h"
#include "ba0_basic_io.h"
#include "ba0_analex.h"
#include "ba0_garbage.h"
#include "ba0_gmp.h"
#include "ba0_scanf.h"
#include "ba0_printf.h"

BA0_DLL char *
ba0_not_a_string (
    void)
{
  return (char *) 0;
}

/*
 * texinfo: ba0_new_string
 * Return the empty string allocated in the current stack 
 * (not the @code{(char*)0} pointer, which is not a string).
 */

BA0_DLL char *
ba0_new_string (
    void)
{
  return ba0_strdup ("");
}

/*
 * texinfo: ba0_strdup
 * Return a copy of @var{s} in an area dynamically allocated in
 * the current stack.
 */

BA0_DLL char *
ba0_strdup (
    char *s)
{
  char *t;

  t = (char *) ba0_alloc (strlen (s) + 1);
  strcpy (t, s);
  return t;
}

/*
 * texinfo: ba0_strcat
 * Concatenate all the strings of @var{T} in a single, allocated, string
 * and returns it.
 */

BA0_DLL char *
ba0_strcat (
    ba0_tableof_string T)
{
  char *p, *q, *r;
  ba0_int_p l, i;

  l = 0;
  for (i = 0; i < T->size; i++)
    l += strlen (T->tab[i]);
  p = (char *) ba0_alloc (l + 1);
  q = p;
  for (i = 0; i < T->size; i++)
    {
      r = T->tab[i];
      while (*r)
        *q++ = *r++;
    }
  *q = '\0';
  return p;
}

/*
   Directly picked from the glibc since strcasecmp is actually not defined
   in the ANSI norm. Hence a bug on some architectures with the -ansi flag.
*/

BA0_DLL int
ba0_strcasecmp (
    char *s1,
    char *s2)
{
  const unsigned char *p1 = (const unsigned char *) s1;
  const unsigned char *p2 = (const unsigned char *) s2;
  int result;

  if (p1 == p2)
    return 0;

  while ((result = tolower (*p1) - tolower (*p2++)) == 0)
    if (*p1++ == '\0')
      break;

  return result;
}

BA0_DLL int
ba0_strncasecmp (
    char *s1,
    char *s2,
    size_t n)
{
  const unsigned char *p1 = (const unsigned char *) s1;
  const unsigned char *p2 = (const unsigned char *) s2;
  unsigned int i;
  int result = 0;

  if (p1 == p2)
    return 0;

  i = 0;
  while (i < n && (result = tolower (*p1) - tolower (*p2++)) == 0)
    {
      if (*p1++ == '\0')
        break;
      i++;
    }

  return result;
}

/*
 * The tacky string - no square brackets
 */

BA0_DLL void *
ba0_scanf_string (
    void *z)
{
  char *s;

  if (z == (void *) 0)
    s = (char *) ba0_alloc (strlen (ba0_value_token_analex ()) + 1);
  else
    s = (char *) z;
  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);
  strcpy (s, ba0_value_token_analex ());
  return s;
}

BA0_DLL void
ba0_printf_string (
    void *str)
{
  ba0_put_string ((char *) str);
}

/*
 * Readonly static data
 */

static char _string[] = "string";

BA0_DLL ba0_int_p
ba0_garbage1_string (
    void *str,
    enum ba0_garbage_code code)
{
  char *s = (char *) str;

  if (code == ba0_isolated)
    return ba0_new_gc_info (s, ba0_ceil_align (strlen (s) + 1), _string);
  else
    return 0;
}

BA0_DLL void *
ba0_garbage2_string (
    void *str,
    enum ba0_garbage_code code)
{
  if (code == ba0_isolated)
    return ba0_new_addr_gc_info (str, _string);
  else
    return str;
}

BA0_DLL void *
ba0_copy_string (
    void *str)
{
  char *s;

  s = (char *) ba0_alloc (strlen ((char *) str) + 1);
  strcpy (s, (char *) str);
  return s;
}
