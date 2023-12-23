#if ! defined (BA0_POINT_H)
#   define BA0_POINT_H 1

#   include "ba0_common.h"

BEGIN_C_DECLS

/*
 * texinfo: ba0_value
 * This data type permits to associate a value to a variable
 * (variables will be defined in the @code{bav} library).
 */

struct ba0_value
{
  void *var;
  void *value;
};

#   define BA0_NOT_A_VALUE (struct ba0_value *)0

#   if defined (BA0_OLDDEF)
typedef struct ba0_value *ba0_value;
#   endif

#   define BA0_NOT_A_VARIABLE 0

/*
 * texinfo: ba0_point
 * This data type permits to associate values to many different variables.
 */

struct ba0_point
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct ba0_value **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_point *ba0_point;
#   endif

extern BA0_DLL void ba0_init_value (
    struct ba0_value *);

extern BA0_DLL struct ba0_value *ba0_new_value (
    void);

extern BA0_DLL void ba0_init_point (
    struct ba0_point *);

extern BA0_DLL struct ba0_point *ba0_new_point (
    void);

extern BA0_DLL void ba0_set_point (
    struct ba0_point *,
    struct ba0_point *);

extern BA0_DLL void ba0_sort_point (
    struct ba0_point *,
    struct ba0_point *);

extern BA0_DLL bool ba0_is_sorted_point (
    struct ba0_point *);

extern BA0_DLL void ba0_delete_coord_point (
    struct ba0_point *,
    struct ba0_point *,
    ba0_int_p);

extern BA0_DLL struct ba0_value *ba0_bsearch_point (
    void *,
    struct ba0_point *,
    ba0_int_p *);

extern BA0_DLL struct ba0_value *ba0_assoc_point (
    void *,
    struct ba0_point *,
    ba0_int_p *);

END_C_DECLS
#endif /* !BA0_POINT_H */
