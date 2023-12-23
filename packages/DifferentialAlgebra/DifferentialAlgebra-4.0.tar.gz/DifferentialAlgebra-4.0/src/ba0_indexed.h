#ifndef BA0_INDEXED_H
#   define BA0_INDEXED_H 1

#   include "ba0_common.h"

BEGIN_C_DECLS

struct ba0_indexed;

struct ba0_indices;

struct ba0_tableof_indexed
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct ba0_indexed **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_tableof_indexed *ba0_tableof_indexed;
#   endif

struct ba0_tableof_indices
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct ba0_indices **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_tableof_indices *ba0_tableof_indices;
#   endif

struct ba0_indices
{
  char po, pf;
  struct ba0_tableof_indexed Tindex;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_indices *ba0_indices;
#   endif

struct ba0_indexed
{
  char *string;
  struct ba0_tableof_indices Tindic;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_indexed *ba0_indexed;
#   endif

typedef void ba0_indexed_function (
    struct ba0_indexed *);

extern BA0_DLL void ba0_init_indexed (
    struct ba0_indexed *);

extern BA0_DLL void ba0_reset_indexed (
    struct ba0_indexed *);

extern BA0_DLL struct ba0_indexed *ba0_new_indexed (
    void);

extern BA0_DLL void ba0_set_indexed (
    struct ba0_indexed *,
    struct ba0_indexed *);

extern BA0_DLL ba0_garbage1_function ba0_garbage1_indexed;

extern BA0_DLL ba0_garbage2_function ba0_garbage2_indexed;

extern BA0_DLL ba0_copy_function ba0_copy_indexed;

extern BA0_DLL char *ba0_indexed_to_string (
    struct ba0_indexed *);

extern BA0_DLL ba0_printf_function ba0_printf_indexed;

extern BA0_DLL struct ba0_indexed *ba0_scanf_indexed (
    struct ba0_indexed *,
    bool *,
    bool (*)(char *));

/* 
 * The first one returns the struct ba0_indexed* data structure
 * The second one converts the data structure into a string
 */
extern BA0_DLL ba0_scanf_function ba0_scanf_raw_indexed;

extern BA0_DLL ba0_scanf_function ba0_scanf_indexed_string;

END_C_DECLS
#endif /* !BA0_INDEXED_H */
