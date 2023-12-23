#include "ba0_exception.h"
#include "ba0_stack.h"
#include "ba0_format.h"
#include "ba0_list.h"
#include "ba0_table.h"
#include "ba0_array.h"
#include "ba0_matrix.h"
#include "ba0_point.h"
#include "ba0_copy.h"

static ba0_list this_copy_list (
    ba0_format,
    ba0_list);
static ba0_table ba0_copy_table (
    ba0_format,
    ba0_table);
static ba0_array ba0_copy_array (
    ba0_format,
    ba0_array);
static ba0_matrix ba0_copy_matrix (
    ba0_format,
    ba0_matrix);
static ba0_value ba0_copy_value (
    ba0_format,
    ba0_value);
static ba0_point ba0_copy_point (
    ba0_format,
    ba0_point);

static void *
ba0_copy_pointer (
    ba0_format f,
    void *o)
{
  switch (f->link[0]->code)
    {
    case ba0_leaf_format:
      return (*f->link[0]->u.leaf.copy) (o);
    case ba0_list_format:
      return this_copy_list (f->link[0]->u.node.op, (ba0_list) o);
    case ba0_table_format:
      return ba0_copy_table (f->link[0]->u.node.op, (ba0_table) o);
    case ba0_array_format:
      return ba0_copy_array (f->link[0]->u.node.op, (ba0_array) o);
    case ba0_matrix_format:
      return ba0_copy_matrix (f->link[0]->u.node.op, (ba0_matrix) o);
    case ba0_value_format:
      return ba0_copy_value (f->link[0]->u.node.op, (ba0_value) o);
    case ba0_point_format:
      return ba0_copy_point (f->link[0]->u.node.op, (ba0_point) o);
    }
  return (void *) 0;            /* to avoid annoying warnings */
}

static ba0_list
this_copy_list (
    ba0_format f,
    ba0_list L)
{
  ba0_list M;

  M = (ba0_list) 0;
  while (L != (ba0_list) 0)
    {
      M = ba0_cons_list (ba0_copy_pointer (f, L->value), M);
      L = L->next;
    }
  M = ba0_reverse_list (M);
  return M;
}

static ba0_table
ba0_copy_table (
    ba0_format f,
    ba0_table t)
{
  ba0_table u;
  ba0_int_p i;

  u = ba0_new_table ();
  ba0_realloc_table (u, t->size);
  u->size = t->size;
  for (i = 0; i < u->size; i++)
    u->tab[i] = ba0_copy_pointer (f, t->tab[i]);
  return u;
}

static ba0_value
ba0_copy_value (
    ba0_format f,
    ba0_value value)
{
  ba0_value newval;

  newval = ba0_new_value ();
  newval->var = value->var;
  newval->value = ba0_copy_pointer (f, value->value);
  return newval;
}

static ba0_point
ba0_copy_point (
    ba0_format f,
    ba0_point point)
{
  ba0_point newpnt;
  ba0_int_p i;

  newpnt = ba0_new_point ();
  ba0_realloc_table ((ba0_table) newpnt, point->size);
  newpnt->size = point->size;
  for (i = 0; i < newpnt->size; i++)
    newpnt->tab[i] = ba0_copy_value (f, point->tab[i]);
  return newpnt;
}

static ba0_array
ba0_copy_array (
    ba0_format f,
    ba0_array A)
{
  ba0_array u;
  ba0_int_p i;
  void *x;

  u = ba0_new_array ();
  ba0_realloc_array (u, A->size, A->sizelt);
  u->size = A->size;
  for (i = 0; i < u->size; i++)
    {
      x = ba0_copy_pointer (f, A->tab + i * A->sizelt);
      memcpy (u->tab + i * A->sizelt, x, A->sizelt);
    }
  return u;
}

static ba0_matrix
ba0_copy_matrix (
    ba0_format f,
    ba0_matrix M)
{
  ba0_matrix N;
  ba0_int_p i, size;

  size = M->nrow * M->ncol;
  N = ba0_new_matrix ();
  ba0_realloc_matrix (N, M->nrow, M->ncol);
  for (i = 0; i < size; i++)
    N->entry[i] = ba0_copy_pointer (f, M->entry[i]);
  return N;
}

/*
   Returns a copy of the the object o the format of which is described by s.
*/

BA0_DLL void *
ba0_copy (
    char *s,
    void *o)
{
  ba0_format f = ba0_get_format (s);

  return ba0_copy_pointer (f, o);
}
