#include <blad.h>
#include "bmi_indices.h"
#include "bmi_mesgerr.h"
#include "bmi_options.h"

void
bmi_init_options (
    struct bmi_options *options)
{
  memset (options, 0, sizeof (struct bmi_options));
  strcpy (options->cellsize, BMI_IX_large);
  options->input_notation = options->output_notation =
      bmi_jet_notation;
}

void
bmi_clear_options (
    struct bmi_options *options)
{
  memset (options, 0, sizeof (struct bmi_options));
}

/*
 * Converts a notation from string to enum bmi_typeof_notation.
 */

static bool
bmi_set_typeof_notation (
    enum bmi_typeof_notation *type,
    char *s)
{
  bool b;

  b = true;
  if (strcmp (s, BMI_IX_jet) == 0)
    *type = bmi_jet_notation;
  else if (strcmp (s, BMI_IX_tjet) == 0)
    *type = bmi_tjet_notation;
  else if (strcmp (s, BMI_IX_jet0) == 0)
    *type = bmi_jet0_notation;
  else if (strcmp (s, BMI_IX_diff) == 0)
    *type = bmi_diff_notation;
  else if (strcmp (s, BMI_IX_udif) == 0)
    *type = bmi_udif_notation;
  else if (strcmp (s, BMI_IX_D) == 0)
    *type = bmi_D_notation;
  else if (strcmp (s, BMI_IX_Derivative) == 0)
    *type = bmi_Derivative_notation;
  else
    b = false;

  return b;
}

/*
 * blad_eval (Rosenfeld_Groebner (...), notation=diff, memory=100)
 * options = args[0], ..., args[nargs-1]
 */

bool
bmi_set_options (
    struct bmi_options *options,
    struct bmi_callback *callback,
    ALGEB * args,
    long nargs)
{
#if defined (BMI_MEMCHECK)
  if (nargs < 5)
    {
      fprintf (stderr, "bmi fatal error: bad nargs value (%ld)\n",
          nargs);
      exit (1);
    }
#endif
/*
 * Input_notation
 */
  bmi_set_callback_ALGEB (callback, args[0]);
  if (!bmi_set_typeof_notation
      (&options->input_notation, bmi_string_op (1, callback)))
    return false;
/*
 * Output_notation
 */
  bmi_set_callback_ALGEB (callback, args[1]);
  if (!bmi_set_typeof_notation
      (&options->output_notation, bmi_string_op (1, callback)))
    return false;
/*
 * Time_limit
 * Minus sign to call ba0_check_interrupt
 */
  bmi_set_callback_ALGEB (callback, args[2]);
  options->time_limit = -atoi (bmi_string_op (1, callback));
  if (options->time_limit == 0)
    options->time_limit = -LONG_MAX;
/*
 * Memory_limit
 */
  bmi_set_callback_ALGEB (callback, args[3]);
  options->memory_limit = atoi (bmi_string_op (1, callback));
/*
 * Cell size
 */
  bmi_set_callback_ALGEB (callback, args[4]);
  strcpy (options->cellsize, bmi_string_op (1, callback));

  return true;
}
