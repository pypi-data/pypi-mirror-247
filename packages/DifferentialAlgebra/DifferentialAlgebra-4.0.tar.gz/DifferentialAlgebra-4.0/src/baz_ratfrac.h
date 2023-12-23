#ifndef BAZ_RATFRAC_H
#   define BAZ_RATFRAC_H 1

#   include "baz_common.h"

BEGIN_C_DECLS

/*
 * texinfo: baz_ratfrac
 * This data type implements fractions of differential polynomials.
 * The fraction is not necessarily reduced.
 * The denominator is nonzero.
 */

struct baz_ratfrac
{
  struct bap_polynom_mpz numer;
  struct bap_polynom_mpz denom;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_ratfrac *baz_ratfrac;
#   endif

struct baz_listof_ratfrac
{
  struct baz_ratfrac *value;
  struct baz_listof_ratfrac *next;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_listof_ratfrac *baz_listof_ratfrac;
#   endif

struct baz_tableof_ratfrac
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct baz_ratfrac **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_tableof_ratfrac *baz_tableof_ratfrac;
#   endif

struct baz_matrixof_ratfrac
{
  ba0_int_p alloc;
  ba0_int_p nrow;
  ba0_int_p ncol;
  struct baz_ratfrac **entry;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_matrixof_ratfrac *baz_matrixof_ratfrac;
#   endif

extern BAZ_DLL void baz_init_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL void baz_init_readonly_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL struct baz_ratfrac *baz_new_ratfrac (
    void);

extern BAZ_DLL void baz_set_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_set_ratfrac_zero (
    struct baz_ratfrac *);

extern BAZ_DLL void baz_set_ratfrac_one (
    struct baz_ratfrac *);

extern BAZ_DLL void baz_set_ratfrac_term (
    struct baz_ratfrac *,
    struct bav_term *);

extern BAZ_DLL void baz_set_ratfrac_polynom (
    struct baz_ratfrac *,
    struct bap_polynom_mpz *);

extern BAZ_DLL void baz_set_ratfrac_fraction (
    struct baz_ratfrac *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *);

extern BAZ_DLL ba0_scanf_function baz_scanf_ratfrac;

extern BAZ_DLL ba0_scanf_function baz_scanf_product_ratfrac;

extern BAZ_DLL ba0_scanf_function baz_scanf_expanded_ratfrac;

extern BAZ_DLL ba0_scanf_function baz_scanf_careful_expanded_ratfrac;

extern BAZ_DLL ba0_printf_function baz_printf_ratfrac;

extern BAZ_DLL ba0_garbage1_function baz_garbage1_ratfrac;

extern BAZ_DLL ba0_garbage2_function baz_garbage2_ratfrac;

extern BAZ_DLL ba0_copy_function baz_copy_ratfrac;

extern BAZ_DLL bool baz_is_zero_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL bool baz_is_one_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL bool baz_is_numeric_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL bool baz_depend_ratfrac (
    struct baz_ratfrac *,
    struct bav_variable *);

extern BAZ_DLL bool baz_equal_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_sort_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_physort_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL void baz_numer_ratfrac (
    struct bap_polynom_mpz *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_denom_ratfrac (
    struct bap_polynom_mpz *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_mark_indets_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL struct bav_variable *baz_leader_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL struct bav_rank baz_rank_ratfrac (
    struct baz_ratfrac *);

extern BAZ_DLL void baz_initial_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_reductum_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_lcoeff_and_reductum_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct bav_variable *);

extern BAZ_DLL void baz_reduce_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_reduce_numeric_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_neg_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_add_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_sub_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_mul_ratfrac_numeric (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    ba0_mpz_t);

extern BAZ_DLL void baz_mul_ratfrac_numeric_mpq (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    ba0_mpq_t);

extern BAZ_DLL void baz_mul_ratfrac_variable (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct bav_variable *,
    bav_Idegree);

extern BAZ_DLL void baz_mul_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_pow_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    bav_Idegree);

extern BAZ_DLL void baz_invert_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_div_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_separant_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *);

extern BAZ_DLL void baz_separant2_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct bav_variable *);

extern BAZ_DLL void baz_diff_ratfrac (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct bav_symbol *,
    struct bav_tableof_variable *);

extern BAZ_DLL bool baz_is_constant_ratfrac (
    struct baz_ratfrac *,
    struct bav_symbol *,
    struct bav_tableof_parameter *);

extern BAZ_DLL bool baz_is_independent_ratfrac (
    struct baz_ratfrac *,
    struct bav_tableof_parameter *);

END_C_DECLS
#endif /* !BAZ_RATFRAC_H */
