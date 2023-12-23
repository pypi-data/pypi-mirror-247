#ifndef BA0_FORMAT_H
#   define BA0_FORMAT_H 1

#   include "ba0_common.h"

BEGIN_C_DECLS
#   define BA0_SIZE_HTABLE_FORMAT      8009
/* 
 * The size of the H-Table for formats.
 * Should be a prime number.
 */
enum ba0_typeof_format
{
  ba0_leaf_format,
  ba0_table_format,
  ba0_list_format,
  ba0_matrix_format,
  ba0_array_format,
  ba0_value_format,
  ba0_point_format
};

struct ba0_format;

struct ba0_subformat
{
  enum ba0_typeof_format code;
  union
  {
    struct _node
    {
      struct ba0_format *op;
      char po;
      char pf;
    } node;
    struct _leaf
    {
      ba0_int_p sizelt;
      ba0_scanf_function *scanf;
      ba0_printf_function *printf;
      ba0_garbage1_function *garbage1;
      ba0_garbage2_function *garbage2;
      ba0_copy_function *copy;
    } leaf;
  } u;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_subformat *ba0_subformat;
#   endif

struct ba0_format
{
  char *text;
  struct ba0_subformat **link;
  ba0_int_p linknmb;
};

#   if defined (BA0_OLDDEF)
typedef struct ba0_format *ba0_format;
#   endif

extern BA0_DLL void ba0_initialize_format (
    void);

extern BA0_DLL void ba0_define_format (
    char *,
    ba0_scanf_function *,
    ba0_printf_function *,
    ba0_garbage1_function *,
    ba0_garbage2_function *,
    ba0_copy_function *);

extern BA0_DLL void ba0_define_format_with_sizelt (
    char *,
    ba0_int_p,
    ba0_scanf_function *,
    ba0_printf_function *,
    ba0_garbage1_function *,
    ba0_garbage2_function *,
    ba0_copy_function *);

extern BA0_DLL struct ba0_format *ba0_get_format (
    char *);

extern BA0_DLL ba0_garbage1_function ba0_empty_garbage1;

extern BA0_DLL ba0_garbage2_function ba0_empty_garbage2;

struct ba0_pair
{
  char *identificateur;
  void *value;
};

struct ba0_tableof_pair
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct ba0_pair **tab;
};

END_C_DECLS
#endif /* !BA0_FORMAT_H */
