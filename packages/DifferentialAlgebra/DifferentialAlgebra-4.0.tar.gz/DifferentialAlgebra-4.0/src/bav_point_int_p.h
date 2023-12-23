#ifndef BAV_POINT_INT_P_H
#   define BAV_POINT_INT_P_H 1

#   include "bav_common.h"
#   include "bav_variable.h"

BEGIN_C_DECLS

/*
 * texinfo: bav_value_int_p
 * This data type permits to associate a @code{ba0_int_p} value
 * to a variable.
 */

struct bav_value_int_p
{
  struct bav_variable *var;
  ba0_int_p value;
};

extern BAV_DLL int bav_inv_comp_value_int_p (
    const void *,
    const void *);

#   if defined (BA0_OLDDEF)
typedef struct bav_value_int_p *bav_value_int_p;
#   endif

/*
 * texinfo: bav_point_int_p
 * This data type permits to associate @code{ba0_int_p} values to
 * many different variables. The variables in the @code{tab} field
 * should be sorted by increasing addresses.
 */

struct bav_point_int_p
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_value_int_p **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_point_int_p *bav_point_int_p;
#   endif

extern BAV_DLL void bav_sort_point_int_p (
    struct bav_point_int_p *);

END_C_DECLS
#endif /* !BAV_POINT_INT_P_H */
