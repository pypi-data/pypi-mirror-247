#ifndef BAV_GLOBAL_H
#   define BAV_GLOBAL_H 1

#   include "bav_common.h"
#   include "bav_differential_ring.h"
#   include "bav_parameter.h"
#   include "bav_term.h"


BEGIN_C_DECLS

struct bav_global
{
  struct
  {
/* 
 * Receives the faulty string when an unknown variable/symbol is parsed
 */
    char unknown[BA0_BUFSIZE];
  } common;
  struct bav_differential_ring R;
  struct
  {
/*
 * Flags indicating which input notation was used
 */
    ba0_int_p notations;
/* 
 * "diff" or "Diff" to display derivatives
 */
    char *diff_string;
  } variable;
/* 
 * Variables some derivatives of which are zero
 */
  struct bav_tableof_parameter parameters;
  struct
  {
/* 
 * Comparison functions w.r.t. term orderings
 */
    enum ba0_compare_code (
        *compare) (
        struct bav_term *,
        struct bav_term *);
    enum ba0_compare_code (
        *compare_stripped) (
        struct bav_term *,
        struct bav_term *,
        bav_Inumber);
  } term_ordering;
};

struct bav_initialized_global
{
  struct
  {
/* 
 * Function called when an unknown symbol/variable/parameter is parsed
 */
    ba0_indexed_function *unknown;
  } common;
  struct
  {
/* 
 * Functions pointers for customizing symbol parsing and printing
 */
    ba0_scanf_function *scanf;
    ba0_printf_function *printf;
  } symbol;
  struct
  {
/* 
 * Functions pointers for customizing variable parsing and printing
 */
    ba0_scanf_function *scanf;
    ba0_printf_function *printf;
/*
 * The string which stands for no derivation in the jet0 notation
 */
    char *jet0_string;
/* 
 * The prefix of temporary variables
 */
    char *temp_string;
  } variable;
  struct
  {
/* 
 * Function pointer for customizing the way ranks are printed.
 */
    ba0_printf_function *printf;
  } rank;
  struct
  {
/* 
 * The string for displaying orderings
 */
    char *string;
  } ordering;
};

extern BAV_DLL struct bav_global bav_global;

extern BAV_DLL struct bav_initialized_global bav_initialized_global;

END_C_DECLS
#endif /* !BAV_GLOBAL_H */
