#ifndef BAZ_COMMON_H
#   define BAZ_COMMON_H 1

#   include <bap.h>

/* 
 * The _MSC_VER flag is set if the code is compiled under WINDOWS
 * by using Microsoft Visual C (through Visual Studio 2008).
 *
 * In that case, some specific annotations must be added for DLL exports
 * Beware to the fact that this header file is going to be used either
 * for/while building BLAD or for using BLAD from an outer software.
 *
 * In the first case, functions are exported.
 * In the second one, they are imported.
 *
 * The flag BAZ_BLAD_BUILDING must thus be set in the Makefile and passed
 * to the C preprocessor at BAP building time. Do not set it when using BAP.
 *
 * When compiling static libraries under Windows, set BA0_STATIC.
 */

#   if defined (_MSC_VER) && ! defined (BA0_STATIC)
#      if defined (BAZ_BLAD_BUILDING)
#         define BAZ_DLL  __declspec(dllexport)
#      else
#         define BAZ_DLL  __declspec(dllimport)
#      endif
#   else
#      define BAZ_DLL
#   endif

/* #   include "baz_mesgerr.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_reset_all_settings (
    void);

extern BAZ_DLL void baz_restart (
    ba0_int_p,
    ba0_int_p);

extern BAZ_DLL void baz_terminate (
    enum ba0_restart_level);

END_C_DECLS
#endif /* !BAZ_COMMON_H */
#ifndef BAZ_MESGERR_H
#   define BAZ_MESGERR_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

extern BAZ_DLL char BAZ_ERRNHL[];

extern BAZ_DLL char BAZ_ERRVPD[];

extern BAZ_DLL char BAZ_ERRGCD[];

extern BAZ_DLL char BAZ_ERRHEU[];

extern BAZ_DLL char BAZ_EXHDIS[];

extern BAZ_DLL char BAZ_EXHENS[];

END_C_DECLS
#endif /* !BAZ_MESGERR_H */
#ifndef BAZ_RATFRAC_H
#   define BAZ_RATFRAC_H 1

/* #   include "baz_common.h" */

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
#ifndef BAZ_COLLECT_TERMS_RATFRAC_H
#   define BAZ_COLLECT_TERMS_RATFRAC_H 1

/* #   include "baz_ratfrac.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_collect_terms_tableof_ratfrac (
    struct baz_tableof_ratfrac *,
    struct baz_tableof_ratfrac *,
    struct baz_tableof_ratfrac *,
    struct baz_tableof_ratfrac *);

END_C_DECLS
#endif /*! BAZ_COLLECT_TERMS_RATFRAC_H */
#if ! defined (BAZ_EVAL_POLYSPEC_MPZ_H)
#   define BAZ_EVAL_POLYSPEC_MPZ_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_eval_polynom_point_interval_mpq_mpz (
    struct ba0_interval_mpq *,
    struct bap_polynom_mpz *,
    struct bav_point_interval_mpq *);

END_C_DECLS
#endif /* !BAZ_EVAL_POLYSPEC_MPZ_H */
#ifndef BAZ_FACTOR_POLYNOM_MPQ_H
#   define BAZ_FACTOR_POLYNOM_MPQ_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_factor_polynom_mpq (
    struct bap_product_mpq *,
    struct bap_polynom_mpq *);

END_C_DECLS
#endif /* !BAZ_FACTOR_POLYNOM_MPQ_H */
#ifndef BAZ_FACTOR_POLYNOM_MPZ_H
#   define BAZ_FACTOR_POLYNOM_MPZ_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_factor_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_polynom_mpz *);

END_C_DECLS
#endif /* ! BAZ_FACTOR_POLYNOM_MPZ_H */
#ifndef BAZ_GCD_POLYNOM_MPZ_H
#   define BAZ_GCD_POLYNOM_MPZ_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

struct baz_factored_polynom_mpz
{
  struct bap_product_mpz outer;
  struct bap_polynom_mpz poly;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_factored_polynom_mpz *baz_factored_polynom_mpz;
#   endif

struct baz_tableof_factored_polynom_mpz
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct baz_factored_polynom_mpz **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_tableof_factored_polynom_mpz
    *baz_tableof_factored_polynom_mpz;
#   endif

struct baz_gcd_data
{
  bool proved_relatively_prime;
  struct bap_product_mpz common;
  struct baz_tableof_factored_polynom_mpz F;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_gcd_data *baz_gcd_data;
#   endif

extern BAZ_DLL ba0_printf_function baz_printf_gcd_data;

extern BAZ_DLL void baz_gcd_univariate_tableof_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_tableof_polynom_mpz *);

extern BAZ_DLL void baz_gcdheu_tableof_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_tableof_polynom_mpz *,
    ba0_int_p);

extern BAZ_DLL void baz_extended_Zassenhaus_gcd_tableof_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_tableof_polynom_mpz *,
    bool);

extern BAZ_DLL void baz_gcd_tableof_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_tableof_polynom_mpz *,
    bool);

extern BAZ_DLL void baz_gcd_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *);

extern BAZ_DLL void baz_content_tableof_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_tableof_polynom_mpz *,
    struct bav_variable *,
    bool);

extern BAZ_DLL void baz_content_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *);

extern BAZ_DLL void baz_primpart_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *);

extern BAZ_DLL void baz_Yun_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_polynom_mpz *,
    bool);

extern BAZ_DLL void baz_squarefree_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_polynom_mpz *);

extern BAZ_DLL void baz_factor_easy_polynom_mpz (
    struct bap_product_mpz *,
    struct bap_polynom_mpz *,
    struct bap_listof_polynom_mpz *);

END_C_DECLS
#endif /* ! BAZ_GCD_POLYNOM_MPZ_H */
#ifndef BAZ_POLYSPEC_MPZ_H
#   define BAZ_POLYSPEC_MPZ_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_genpoly_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    ba0_mpz_t,
    struct bav_variable *);

extern BAZ_DLL void baz_yet_another_point_int_p_mpz (
    struct bav_point_int_p *,
    struct bap_tableof_polynom_mpz *,
    struct bap_product_mpz *,
    struct bav_variable *);

struct baz_ideal_lifting
{
  struct bap_polynom_mpz *A;
  struct bap_polynom_mpz *initial;
  struct bap_product_mpz factors_initial;
  struct bap_product_mpzm factors_mod_point;
  struct bav_point_int_p point;
  ba0_mpz_t p;
  ba0_int_p l;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_ideal_lifting *baz_ideal_lifting;
#   endif

extern BAZ_DLL void baz_HL_init_ideal_lifting (
    struct baz_ideal_lifting *);

extern BAZ_DLL void baz_HL_printf_ideal_lifting (
    void *);

extern BAZ_DLL void baz_HL_integer_divisors (
    ba0_mpz_t *,
    struct baz_ideal_lifting *,
    ba0_mpz_t *);

extern BAZ_DLL void baz_HL_end_redistribute (
    struct baz_ideal_lifting *,
    ba0_mpz_t *,
    struct bap_polynom_mpz *,
    ba0_mpz_t);

extern BAZ_DLL void baz_HL_begin_redistribute (
    struct baz_ideal_lifting *,
    ba0_mpz_t *,
    struct bap_polynom_mpz *,
    ba0_mpz_t);

extern BAZ_DLL void baz_HL_redistribute_the_factors_of_the_initial (
    struct baz_ideal_lifting *);

extern BAZ_DLL void baz_HL_ideal_Hensel_lifting (
    struct bap_product_mpz *,
    struct baz_ideal_lifting *);

extern BAZ_DLL void baz_monomial_reduce_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    ba0_mpz_t,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *);

extern BAZ_DLL void baz_gcd_pseudo_division_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bap_product_mpz *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *);

extern BAZ_DLL void baz_gcd_prem_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_product_mpz *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *);

extern BAZ_DLL void baz_gcd_pquo_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_product_mpz *,
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *);

END_C_DECLS
#endif /* !BAZ_POLYSPEC_MPZ_H */
#ifndef BAZ_PROSPEC_MPZ_H
#   define BAZ_PROSPEC_MPZ_H 1

/* #   include "baz_common.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_factor_numeric_content_product_mpz (
    struct bap_product_mpz *,
    struct bap_product_mpz *);

extern BAZ_DLL void baz_gcd_product_mpz (
    struct bap_product_mpz *,
    struct bap_product_mpz *,
    struct bap_product_mpz *,
    struct bap_product_mpz *,
    struct bap_product_mpz *);

END_C_DECLS
#endif /* !BAZ_PROSPEC_MPZ_H */
#if ! defined (BAZ_RATBILGE_H)
#   define BAZ_RATBILGE_H 1

/* #   include "baz_ratfrac.h" */

BEGIN_C_DECLS

extern BAZ_DLL void baz_rat_bilge_mpz (
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct bav_symbol *,
    struct bav_tableof_parameter *);

END_C_DECLS
#endif
#if ! defined (BAZ_REL_RATFRAC_H)
#   define BAZ_REL_RATFRAC_H 1

/* #   include "baz_ratfrac.h" */

BEGIN_C_DECLS

/*
 * texinfo: baz_typeof_relop
 * This data type provides an encoding for relational operators.
 */

enum baz_typeof_relop
{
  baz_none_relop,
  baz_equal_relop,
  baz_not_equal_relop,
  baz_greater_relop,
  baz_greater_or_equal_relop,
  baz_less_relop,
  baz_less_or_equal_relop
};

/*
 * texinfo: baz_rel_ratfrac
 * This data type implements a pair of rational fractions connected
 * by a relational operator.
 */

struct baz_rel_ratfrac
{
  struct baz_ratfrac lhs;
  struct baz_ratfrac rhs;
  enum baz_typeof_relop op;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_rel_ratfrac *baz_rel_ratfrac;
#   endif

struct baz_tableof_rel_ratfrac
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct baz_rel_ratfrac **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct baz_tableof_rel_ratfrac *baz_tableof_rel_ratfrac;
#   endif

extern BAZ_DLL void baz_init_rel_ratfrac (
    struct baz_rel_ratfrac *);

extern BAZ_DLL struct baz_rel_ratfrac *baz_new_rel_ratfrac (
    void);

extern BAZ_DLL void baz_set_rel_ratfrac (
    struct baz_rel_ratfrac *,
    struct baz_rel_ratfrac *);

extern BAZ_DLL void baz_set_ratfrac_rel_ratfrac (
    struct baz_ratfrac *,
    struct baz_rel_ratfrac *);

extern BAZ_DLL ba0_scanf_function baz_scanf_rel_ratfrac;

extern BAZ_DLL ba0_printf_function baz_printf_rel_ratfrac;

extern BAZ_DLL ba0_garbage1_function baz_garbage1_rel_ratfrac;

extern BAZ_DLL ba0_garbage2_function baz_garbage2_rel_ratfrac;

extern BAZ_DLL ba0_copy_function baz_copy_rel_ratfrac;

END_C_DECLS
#endif /*!BAZ_REL_RATFRAC_H */
