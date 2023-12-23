#ifndef BA0_STRING_H
#   define BA0_STRING_H 1

#   include "ba0_common.h"

BEGIN_C_DECLS

struct ba0_tableof_string
{
  ba0_int_p alloc;
  ba0_int_p size;
  char **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_tableof_string *ba0_tableof_string;
#   endif

struct ba0_matrixof_string
{
  ba0_int_p alloc;
  ba0_int_p nrow;
  ba0_int_p ncol;
  char **entry;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_matrixof_string *ba0_matrixof_string;
#   endif

struct ba0_listof_string
{
  char *value;
  struct ba0_listof_string *next;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_listof_string *ba0_listof_string;
#   endif

struct ba0_tableof_tableof_string
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct ba0_tableof_string **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_tableof_tableof_string *ba0_tableof_tableof_string;
#   endif

extern BA0_DLL char *ba0_not_a_string (
    void);

extern BA0_DLL char *ba0_new_string (
    void);

extern BA0_DLL char *ba0_strdup (
    char *);

extern BA0_DLL char *ba0_strcat (
    struct ba0_tableof_string *);

/* 
 * redefined since they are not ANSI */

extern BA0_DLL int ba0_strcasecmp (
    char *,
    char *);

extern BA0_DLL int ba0_strncasecmp (
    char *,
    char *,
    size_t);

extern BA0_DLL ba0_scanf_function ba0_scanf_string;

extern BA0_DLL ba0_printf_function ba0_printf_string;

extern BA0_DLL ba0_garbage1_function ba0_garbage1_string;

extern BA0_DLL ba0_garbage2_function ba0_garbage2_string;

extern BA0_DLL ba0_copy_function ba0_copy_string;

END_C_DECLS
#endif /* !BA0_STRING_H */
