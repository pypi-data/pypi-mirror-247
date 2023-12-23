#include "ba0_exception.h"
#include "ba0_stack.h"
#include "ba0_garbage.h"
#include "ba0_analex.h"
#include "ba0_gmp.h"
#include "ba0_basic_io.h"
#include "ba0_global.h"
#include "ba0_string.h"

/*
 * texinfo: ba0_set_settings_gmp
 * Assign the values of its parameters to the @code{gmp} substructure
 * of @code{ba0_initialized_global}.
 * Parameter @var{protect} must be specified.
 * The other parameters may be left to zero in which case the 
 * corresponding fields of the @code{gmp} substructure
 * are restored to their default values.
 */

BA0_DLL void
ba0_set_settings_gmp (
    ba0_set_memory_functions_function *set,
    bool protect,
    char *mpz_string)
{
  if (set)
    ba0_initialized_global.gmp.set_memory_functions = set;
  else
    ba0_initialized_global.gmp.set_memory_functions = &ba0_mp_set_memory_functions;
  ba0_initialized_global.gmp.protect_from_evaluation = protect;
  if (mpz_string)
    ba0_initialized_global.gmp.mpz_string = mpz_string;
  else
    ba0_initialized_global.gmp.mpz_string = "Integer";
}

/*
 * texinfo: ba0_get_settings_gmp
 * Assign to its parameters the values of the corresponding fields
 * in the @code{gmp} substructure of @code{ba0_initialized_global}.
 * Zero parameters are allowed.
 */

BA0_DLL void
ba0_get_settings_gmp (
    ba0_set_memory_functions_function **set,
    bool *protect,
    char **mpz_string)
{
  if (set)
    *set = ba0_initialized_global.gmp.set_memory_functions;
  if (protect)
    *protect = ba0_initialized_global.gmp.protect_from_evaluation;
  if (mpz_string)
    *mpz_string = ba0_initialized_global.gmp.mpz_string;
}

/*
 * texinfo: ba0_record_gmp_memory_functions
 * Record the GMP memory allocation functions for further restoration.
 */

BA0_DLL void
ba0_record_gmp_memory_functions (
    void)
{
  ba0_mp_get_memory_functions
      (&ba0_global.gmp.alloc_function, &ba0_global.gmp.realloc_function,
      &ba0_global.gmp.free_function);
}


/*
 * texinfo: ba0_restore_gmp_memory_functions
 * Restore the GMP memory allocation functions previously recorded.
 * Calls the function pointed to by the settings variables
 * @code{ba0_gmp_set_memory_functions}.
 */

BA0_DLL void
ba0_restore_gmp_memory_functions (
    void)
{
  (*ba0_initialized_global.gmp.set_memory_functions)
      (ba0_global.gmp.alloc_function, ba0_global.gmp.realloc_function,
      ba0_global.gmp.free_function);
}

BA0_DLL bool
ba0_domain_mpz (
    void)
{
  return true;
}

BA0_DLL bool
ba0_domain_mpq (
    void)
{
  return true;
}

BA0_DLL void *
ba0_gmp_alloc (
    size_t n)
{
  ba0_global.gmp.alloc_function_called = true;
  if (n > 10000)
    ba0_process_check_interrupt ();
  return ba0_alloc ((ba0_int_p) n);
}

BA0_DLL void *
ba0_gmp_realloc (
    void *p,
    size_t oldsize,
    size_t newsize)
{
  if (newsize <= oldsize)
    return p;
  else
    {
      ba0_int_p *q;

      q = (ba0_int_p *) ba0_alloc ((ba0_int_p) newsize);
      memcpy (q, p, oldsize);
#if defined(BA0_HEAVY_DEBUG)
      {
        struct ba0_stack *sp, *sq;
        sp = ba0_which_stack (p);
        sq = ba0_which_stack (q);
        if (sp != sq)
          BA0_RAISE_EXCEPTION (BA0_ERRALG);
      }
#endif
      return q;
    }
}

/*
 * On Windows, GMP does not use gmp_realloc.
 * This causes memory problems in ba0_global.stack.quiet
 */

BA0_DLL void
ba0_gmp_free (
    void *ptr,
    size_t size)
{
#if defined (_MSC_VER)
  size = ba0_allocated_size (size);
  if (ba0_current_stack () == &ba0_global.stack.quiet &&
      ptr >= ba0_global.stack.quiet.cells.tab
      [ba0_global.stack.quiet.free.index_in_cells] &&
      (char *) ptr + size == (char *) ba0_global.stack.quiet.free.address)
    {
      ba0_global.stack.quiet.free.address = ptr;
      ba0_global.stack.quiet.free.memory_left += size;
    }
#else
  ptr = 0;                      /* To avoid annoying warnings */
  size = 0;
#endif
}

/*
 * texinfo: ba0_new_mpz
 * Return a @code{ba0_mpz_t} allocated on the current stack.
 */

BA0_DLL ba0__mpz_struct *
ba0_new_mpz (
    void)
{
  ba0__mpz_struct *z;

  z = (ba0__mpz_struct *) ba0_alloc (sizeof (ba0__mpz_struct));
  ba0_mpz_init (z);
  return z;
}

/*
 * texinfo: ba0_mpz_si_pow_ui
 * Assign @math{u^n} to @var{w}.
 */

BA0_DLL void
ba0_mpz_si_pow_ui (
    ba0_mpz_t w,
    ba0_int_p u,
    unsigned ba0_int_p n)
{
  if (u >= 0)
    ba0_mpz_ui_pow_ui (w, (unsigned ba0_int_p) u, n);
  else
    {
      ba0_mpz_ui_pow_ui (w, (unsigned ba0_int_p) (-u), n);
      if (n % 2 == 1)
        ba0_mpz_neg (w, w);
    }
}

/*
 * texinfo: ba0_mpz_nextprime
 * Assign to @var{next} the smallest prime number greater than @var{prev}.
 * The function calls @code{mpz_nextprime} if GMP is used else
 * it relies on the mini-gmp @code{mpz_probab_prime_p} function,
 * combined with an elementary sieve.
 */

BA0_DLL void
ba0_mpz_nextprime (
    ba0_mpz_t next,
    ba0_mpz_t prev)
{
#if defined (BA0_USE_GMP)
  mpz_nextprime (next, prev);
#else
  if (ba0_mpz_cmp_ui (prev, 7) < 0)
    {
      if (ba0_mpz_cmp_ui (prev, 3) < 0)
        ba0_mpz_set_ui (next, 3);
      else if (ba0_mpz_cmp_ui (prev, 5) < 0)
        ba0_mpz_set_ui (next, 5);
      else
        ba0_mpz_set_ui (next, 7);
    }
  else
    {
      struct ba0_mark M;
      ba0_int_p i, j, s, r;
      ba0_mpz_t n;
/*
 * The following gaps permit to avoid multiples of 2, 3 and 5 starting from 7
 * The period length is 2*3*5 = 30
 */
      static ba0_int_p gap [] = { 4, 2, 4, 2, 4, 6, 2, 6 };

      ba0_push_another_stack ();
      ba0_record (&M);
      ba0_mpz_init (n);
      ba0_mpz_sub_ui (n, prev, 7);
      r = ba0_mpz_tdiv_r_ui ((ba0__mpz_struct*)0, n, 30);
      i = -1;
      s = 0;
      while (s <= r)
        {
          i += 1;
          s += gap[i];
        }
      ba0_mpz_add_ui (n, n, s - r);
      while (! bam_mpz_probab_prime_p (n, 25))
        {
          i = (i + 1) % (sizeof(gap) / sizeof(int));
          ba0_mpz_add_ui (n, n, gap[i]);
        } 
      ba0_pull_stack ();
      ba0_mpz_set (next, n);
      ba0_restore (&M);
    }
#endif
}

/*
 * texinfo: ba0_scanf_mpz
 * Read a @code{ba0_mpz_t} through the lexical analyzer and store it
 * in @var{z} if @var{z} is nonzero. Allocate otherwise a new 
 * @code{ba0_mpz_t}. Return the read @code{ba0_mpz_t}.
 */

BA0_DLL void *
ba0_scanf_mpz (
    void *z)
{
  ba0__mpz_struct *c;
  bool minus;

  if (z == (void *) 0)
    c = ba0_new_mpz ();
  else
    c = (ba0__mpz_struct *) z;
  if (ba0_sign_token_analex ("-"))
    {
      minus = true;
      ba0_get_token_analex ();
    }
  else
    minus = false;
  if (ba0_type_token_analex () != ba0_integer_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRINT);
  ba0_mpz_set_str (c, ba0_value_token_analex (), (int) 10);
  if (minus)
    ba0_mpz_neg (c, c);
  return c;
}

/*
 * Print the ba0_mpz_t z.
 */

BA0_DLL void
ba0_printf_mpz (
    void *z)
{
  ba0__mpz_struct *c = (ba0__mpz_struct *) z;
  char *s;
  struct ba0_mark M;

  ba0_record (&M);
  s = ba0_mpz_get_str ((char *) 0, 10, c);
  if (ba0_initialized_global.gmp.protect_from_evaluation)
    {
      ba0_put_string (ba0_initialized_global.gmp.mpz_string);
      ba0_put_char ('(');
      ba0_put_string (s);
      ba0_put_char (')');
    }
  else
    ba0_put_string (s);
  ba0_restore (&M);
}

/*
 * Readonly static data
 */

static char mpz_struct_[] = "ba0__mpz_struct";
static char mpz_struct_mp_d_[] = "ba0__mpz_struct._mp_d";

BA0_DLL ba0_int_p
ba0_garbage1_mpz (
    void *_c,
    enum ba0_garbage_code code)
{
  ba0__mpz_struct *c = (ba0__mpz_struct *) _c;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (c, sizeof (ba0__mpz_struct), mpz_struct_);
  if (c->_mp_alloc != 0)
    n += ba0_new_gc_info
        (c->_mp_d, c->_mp_alloc * sizeof (ba0_mp_limb_t), mpz_struct_mp_d_);
  return n;
}

BA0_DLL void *
ba0_garbage2_mpz (
    void *_c,
    enum ba0_garbage_code code)
{
  ba0__mpz_struct *c;

  if (code == ba0_isolated)
    c = (ba0__mpz_struct *) ba0_new_addr_gc_info (_c, mpz_struct_);
  else
    c = (ba0__mpz_struct *) _c;

  if (c->_mp_alloc != 0)
    c->_mp_d = ba0_new_addr_gc_info (c->_mp_d, mpz_struct_mp_d_);
  return c;
}

BA0_DLL void *
ba0_copy_mpz (
    void *z)
{
  ba0__mpz_struct *c;

  c = ba0_new_mpz ();
  ba0_mpz_init_set (c, (ba0__mpz_struct *) z);
  return c;
}

/*
 * texinfo: ba0_new_mpq
 * Return a @code{mpq_t} allocated on the current stack.
 */

BA0_DLL ba0__mpq_struct *
ba0_new_mpq (
    void)
{
  ba0__mpq_struct *q;

  q = (ba0__mpq_struct *) ba0_alloc (sizeof (ba0__mpq_struct));
  ba0_mpq_init (q);
  return q;
}

/*
 * Reads a ba0_mpq_t through the lexical analyzer and assigns it to z,
 * if z in nonzero. Exceptions BA0_ERRRAT, BA0_ERRDPZ may be raised.
 */

BA0_DLL void *
ba0_scanf_mpq (
    void *z)
{
  ba0__mpq_struct *q;
  struct ba0_mark M;
  struct ba0_tableof_string mantissa;
  bool minus_sign;
  ba0_int_p exponent;
  char *p;

  ba0_init_table ((ba0_table) & mantissa);
  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_realloc_table ((ba0_table) & mantissa, 10);
  ba0_pull_stack ();

  if (z == (void *) 0)
    q = ba0_new_mpq ();
  else
    q = (ba0__mpq_struct *) z;
/*
 * First the sign
 */
  if (ba0_sign_token_analex ("-"))
    {
      minus_sign = true;
      ba0_get_token_analex ();
    }
  else
    {
      if (ba0_sign_token_analex ("+"))
        ba0_get_token_analex ();
      minus_sign = false;
    }
/*
 * Possibly a non empty integer part
 * Spaces are authorized between the minus sign and what follows.
 */
  if (ba0_type_token_analex () == ba0_integer_token)
    {
      mantissa.tab[mantissa.size] = ba0_value_token_analex ();
      mantissa.size += 1;
      ba0_get_token_analex ();
    }
/*
 * If no integer is read then there must be a dot + a fractionnal part
 */
  if (mantissa.size == 0 && !ba0_sign_token_analex ("."))
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRRAT);
/*
 * The case of the double notation
 */
  p = ba0_value_token_analex ();
  if ((mantissa.size == 0 || !ba0_spaces_before_token_analex ()) &&
      (ba0_sign_token_analex (".") ||
          ((p[0] == 'e' || p[0] == 'E' || p[0] == '@') &&
              (p[1] == '\0' || isdigit ((int) p[1])))))
    {
      exponent = 0;
/*
 * At the end, the integer read is multiplied by 10**exponent.
 */
      if (ba0_sign_token_analex ("."))
        {
          ba0_get_token_analex ();
          if (!ba0_spaces_before_token_analex () &&
              ba0_type_token_analex () == ba0_integer_token)
            {
              mantissa.tab[mantissa.size] = ba0_value_token_analex ();
              mantissa.size += 1;
              exponent = -(ba0_int_p) strlen (ba0_value_token_analex ());
              ba0_get_token_analex ();
            }
        }
/*
 * Possibly an exponent in the double notation.
 */
      p = ba0_value_token_analex ();
      if (!ba0_spaces_before_token_analex () &&
          (p[0] == 'e' || p[0] == 'E' || p[0] == '@') &&
          (p[1] == '\0' || isdigit ((int) p[1])))
        {
/*
 * To simplify the coming analysis, the current token may be split
 * into two different tokens
 */
          if (isdigit ((int) p[1]))
            {
              ba0_int_p i;
              i = 2;
              while (isdigit ((int) p[i]))
                i++;
              if (p[i] == '\0')
                ba0_unget_given_token_analex (p + 1, ba0_integer_token, false);
              else
                {
                  ba0_push_another_stack ();
                  p = ba0_strdup (p);
                  ba0_pull_stack ();
                  ba0_unget_given_token_analex (p + i, ba0_string_token, false);
                  p[i] = '\0';
                  ba0_unget_given_token_analex
                      (p + 1, ba0_integer_token, false);
                }
            }
/*
 * The analysis of the exponent starts here
 */
          ba0_get_token_analex ();
          if (!ba0_spaces_before_token_analex () &&
              ba0_type_token_analex () == ba0_integer_token)
            exponent = exponent + atoi (ba0_value_token_analex ());
          else if (!ba0_spaces_before_token_analex () &&
              (ba0_sign_token_analex ("+") || ba0_sign_token_analex ("-")))
            {
              bool minus_sign2 = ba0_sign_token_analex ("-");
              ba0_get_token_analex ();
              if (ba0_spaces_before_token_analex () ||
                  ba0_type_token_analex () != ba0_integer_token)
                BA0_RAISE_PARSER_EXCEPTION (BA0_ERRRAT);
              if (minus_sign2)
                exponent -= atoi (ba0_value_token_analex ());
              else
                exponent += atoi (ba0_value_token_analex ());
            }
          else
            BA0_RAISE_PARSER_EXCEPTION (BA0_ERRRAT);
        }
      else
        ba0_unget_token_analex (1);

      ba0_push_another_stack ();
      p = ba0_strcat (&mantissa);
      ba0_pull_stack ();

      ba0_mpz_set_str (ba0_mpq_numref (q), p, 10);
      if (exponent > 0)
        {
          ba0_mpz_ui_pow_ui (ba0_mpq_denref (q), 10, exponent);
          ba0_mpz_mul (ba0_mpq_numref (q), ba0_mpq_numref (q),
              ba0_mpq_denref (q));
          ba0_mpz_set_ui (ba0_mpq_denref (q), 1);
        }
      else
        {
          ba0_mpz_ui_pow_ui (ba0_mpq_denref (q), 10, -exponent);
          ba0_mpq_canonicalize (q);
        }
    }
  else
/*
 * The traditional rational notation
 */
    {
      ba0_push_another_stack ();
      p = ba0_strcat (&mantissa);
      ba0_pull_stack ();

      ba0_mpz_set_str (ba0_mpq_numref (q), p, 10);
      if (ba0_sign_token_analex ("/"))
        {
          ba0_get_token_analex ();
/*
 * A minus sign is allowed before the denominator
 */
          if (ba0_sign_token_analex ("-") || ba0_sign_token_analex ("+"))
            {
              if (ba0_sign_token_analex ("-"))
                minus_sign = !minus_sign;
              ba0_get_token_analex ();
            }
          if (ba0_type_token_analex () != ba0_integer_token)
            BA0_RAISE_PARSER_EXCEPTION (BA0_ERRRAT);
          ba0_mpz_set_str (ba0_mpq_denref (q), ba0_value_token_analex (), 10);
          if (ba0_mpz_sgn (ba0_mpq_denref (q)) == 0)
            BA0_RAISE_PARSER_EXCEPTION (BA0_ERRIVZ);
          ba0_mpq_canonicalize (q);
        }
      else
        ba0_unget_token_analex (1);
    }
  if (minus_sign)
    ba0_mpq_neg (q, q);
  ba0_restore (&M);
  return q;
}

BA0_DLL void
ba0_printf_mpq (
    void *z)
{
  ba0__mpq_struct *q = (ba0__mpq_struct *) z;
  char *s;
  struct ba0_mark M;

  ba0_record (&M);
  s = ba0_mpz_get_str ((char *) 0, 10, ba0_mpq_numref (q));
  if (ba0_initialized_global.gmp.protect_from_evaluation)
    {
      ba0_put_string (ba0_initialized_global.gmp.mpz_string);
      ba0_put_char ('(');
      ba0_put_string (s);
      ba0_put_char (')');
    }
  else
    ba0_put_string (s);
  if (ba0_mpz_cmp_ui (ba0_mpq_denref (q), 1) != 0)
    {
      ba0_put_char ('/');
      s = ba0_mpz_get_str ((char *) 0, 10, ba0_mpq_denref (q));
      if (ba0_initialized_global.gmp.protect_from_evaluation)
        {
          ba0_put_string (ba0_initialized_global.gmp.mpz_string);
          ba0_put_char ('(');
          ba0_put_string (s);
          ba0_put_char (')');
        }
      else
        ba0_put_string (s);
    }
  ba0_restore (&M);
}

/*
 * Readonly static data
 */

static char mpq_struct_[] = "ba0__mpq_struct";
static char mpq_struct_mp_num_[] = "ba0__mpq_struct._mp_num._mp_d";
static char mpq_struct_mp_den_[] = "ba0__mpq_struct._mp_den._mp_d";

BA0_DLL ba0_int_p
ba0_garbage1_mpq (
    void *_q,
    enum ba0_garbage_code code)
{
  ba0__mpq_struct *q = (ba0__mpq_struct *) _q;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info (q, sizeof (ba0__mpq_struct), mpq_struct_);

  if (q->_mp_num._mp_alloc != 0)
    n += ba0_new_gc_info
        (q->_mp_num._mp_d,
        q->_mp_num._mp_alloc * sizeof (ba0_mp_limb_t), mpq_struct_mp_num_);
  if (q->_mp_den._mp_alloc != 0)
    n += ba0_new_gc_info
        (q->_mp_den._mp_d,
        q->_mp_den._mp_alloc * sizeof (ba0_mp_limb_t), mpq_struct_mp_den_);
  return n;
}

BA0_DLL void *
ba0_garbage2_mpq (
    void *_q,
    enum ba0_garbage_code code)
{
  ba0__mpq_struct *q;

  if (code == ba0_isolated)
    q = (ba0__mpq_struct *) ba0_new_addr_gc_info (_q, mpq_struct_);
  else
    q = (ba0__mpq_struct *) _q;

  if (q->_mp_num._mp_alloc != 0)
    q->_mp_num._mp_d = ba0_new_addr_gc_info
        (q->_mp_num._mp_d, mpq_struct_mp_num_);
  if (q->_mp_den._mp_alloc != 0)
    q->_mp_den._mp_d = ba0_new_addr_gc_info
        (q->_mp_den._mp_d, mpq_struct_mp_den_);
  return q;
}

BA0_DLL void *
ba0_copy_mpq (
    void *z)
{
  ba0__mpq_struct *q;

  q = ba0_new_mpq ();
  ba0_mpq_init (q);
  ba0_mpq_set (q, (ba0__mpq_struct *) z);
  return q;
}
