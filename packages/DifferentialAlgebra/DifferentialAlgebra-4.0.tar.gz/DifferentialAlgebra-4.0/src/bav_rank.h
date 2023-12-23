#ifndef BAV_RANK_H
#   define BAV_RANK_H 1

#   include "bav_common.h"
#   include "bav_variable.h"

BEGIN_C_DECLS

/*
 * texinfo: bav_rank
 * A rank is a variable raised to some degree.
 * Observe that some special ranks are also defined such as the
 * rank of zero and the one of nonzero constants.
 * The rank of zero is encoded by 
 * (@code{BAV_NOT_A_VARIABLE}, @math{-1}).
 * The rank of nonzero constants is encoded by a field @code{deg}
 * equal to @math{0} (the field @code{var} is unspecified).
 * Ranks are stored in the main and second stacks.
 */

struct bav_rank
{
  struct bav_variable *var;     // possibly BAV_NOT_A_VARIABLE
  bav_Idegree deg;              // possibly 0 or negative
};

#   if defined (BA0_OLDDEF)
typedef struct bav_rank *bav_rank;
#   endif

extern BAV_DLL void bav_init_rank (
    struct bav_rank *);

extern BAV_DLL struct bav_rank *bav_new_rank (
    void);

extern BAV_DLL bool bav_is_zero_rank (
    struct bav_rank *);

extern BAV_DLL bool bav_is_constant_rank (
    struct bav_rank *);

extern BAV_DLL bool bav_lt_rank (
    struct bav_rank *,
    struct bav_rank *);

extern BAV_DLL bool bav_gt_rank (
    struct bav_rank *,
    struct bav_rank *);

extern BAV_DLL bool bav_equal_rank (
    struct bav_rank *,
    struct bav_rank *);

extern BAV_DLL int bav_inv_comp_rank (
    const void *,
    const void *);

extern BAV_DLL struct bav_rank bav_zero_rank (
    void);

extern BAV_DLL struct bav_rank bav_constant_rank (
    void);

extern BAV_DLL struct bav_rank bav_constant_rank2 (
    struct bav_variable *);

extern BAV_DLL void bav_set_settings_rank (
    ba0_printf_function *);

extern BAV_DLL void bav_get_settings_rank (
    ba0_printf_function **);

extern BAV_DLL ba0_scanf_function bav_scanf_rank;

extern BAV_DLL ba0_printf_function bav_printf_rank;

extern BAV_DLL ba0_printf_function bav_printf_default_rank;

extern BAV_DLL ba0_printf_function bav_printf_stars_rank;

extern BAV_DLL ba0_printf_function bav_printf_list_rank;

struct bav_tableof_rank
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_rank **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_rank *bav_tableof_rank;
#   endif

END_C_DECLS
#endif /* !BAV_RANK_H */
