#ifndef BAV_POINT_INTERVAL_MPQ_H
#   define BAV_POINT_INTERVAL_MPQ_H 1

#   include "bav_common.h"
#   include "bav_variable.h"

BEGIN_C_DECLS

/*
 * texinfo: bav_value_interval_mpq
 * This data type associates an interval with @code{mpq_t} ends
 * to a variable.
 */

struct bav_value_interval_mpq
{
  struct bav_variable *var;
  struct ba0_interval_mpq *value;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_value_interval_mpq *bav_value_interval_mpq;
#   endif

/* In the next one, all variables might be equal */

struct bav_tableof_value_interval_mpq
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_value_interval_mpq **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_value_interval_mpq *bav_tableof_value_interval_mpq;
#   endif


/*
 * texinfo: bav_point_interval_mpq
 * This data type permits to associate interval with @code{mpq_t} ends
 * to many different variables. The array @code{tab} should be sorted
 * by increasing addresses.
 */

struct bav_point_interval_mpq
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_value_interval_mpq **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_point_interval_mpq *bav_point_interval_mpq;
#   endif

struct bav_tableof_point_interval_mpq
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_point_interval_mpq **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_tableof_point_interval_mpq *bav_tableof_point_interval_mpq;
#   endif

extern BAV_DLL struct bav_value_interval_mpq *bav_new_value_interval_mpq (
    void);

extern BAV_DLL void bav_set_value_interval_mpq (
    struct bav_value_interval_mpq *,
    struct bav_value_interval_mpq *);

extern BAV_DLL void bav_init_point_interval_mpq (
    struct bav_point_interval_mpq *);

extern BAV_DLL struct bav_point_interval_mpq *bav_new_point_interval_mpq (
    void);

extern BAV_DLL void bav_realloc_point_interval_mpq (
    struct bav_point_interval_mpq *,
    ba0_int_p);

extern BAV_DLL void bav_set_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *);

extern BAV_DLL void bav_set_coord_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_variable *,
    struct ba0_interval_mpq *);

extern BAV_DLL void bav_intersect_coord_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *,
    struct bav_variable *,
    struct ba0_interval_mpq *);

extern BAV_DLL void bav_intersect_point_interval_mpq (
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *,
    struct bav_point_interval_mpq *);

extern BAV_DLL bool bav_is_empty_point_interval_mpq (
    struct bav_point_interval_mpq *);

extern BAV_DLL void bav_bisect_point_interval_mpq (
    struct bav_tableof_point_interval_mpq *,
    struct bav_point_interval_mpq *,
    ba0_int_p);

extern BAV_DLL void bav_set_tableof_point_interval_mpq (
    struct bav_tableof_point_interval_mpq *,
    struct bav_tableof_point_interval_mpq *);

END_C_DECLS
#endif /* !BAV_POINT_INTERVAL_MPQ_H */
