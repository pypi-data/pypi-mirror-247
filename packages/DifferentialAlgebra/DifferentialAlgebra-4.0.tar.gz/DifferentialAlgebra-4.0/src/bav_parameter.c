#include "bav_parameter.h"
#include "bav_differential_ring.h"
#include "bav_global.h"
#include "bav_variable.h"

/*
 * texinfo: bav_init_parameters
 * Initialize @var{P} to the empty table.
 */

BAV_DLL void
bav_init_parameters (
    bav_tableof_parameter P)
{
  ba0_init_table ((ba0_table) P);
}

/*
 * texinfo: bav_reset_parameters
 * Set the field @code{size} of @var{P} to zero.
 */

BAV_DLL void
bav_reset_parameters (
    bav_tableof_parameter P)
{
  ba0_reset_table ((ba0_table) P);
}

/*
 * texinfo: bav_new_parameters
 * Allocate a table of parameter, initialize it and return it.
 */

BAV_DLL bav_tableof_parameter
bav_new_parameters (
    void)
{
  bav_tableof_parameter P;

  P = (bav_tableof_parameter) ba0_alloc (sizeof (struct bav_tableof_parameter));
  bav_init_parameters (P);
  return P;
}

/*
 * texinfo: bav_sizeof_parameters
 * Return the size of the memory needed to perform a copy of the table.
 */

BAV_DLL unsigned ba0_int_p
bav_sizeof_parameters (
    bav_tableof_parameter P)
{
  unsigned ba0_int_p size;
  ba0_int_p i;

  size = ba0_allocated_size (sizeof (struct bav_tableof_parameter));
  size += ba0_allocated_size (sizeof (bav_parameter) * P->size);
  for (i = 0; i < P->size; i++)
    size += ba0_allocated_size (sizeof (struct bav_parameter)) +
        ba0_allocated_size (sizeof (bav_symbol) * P->tab[i]->dep.size);
  return size;
}

/*
 * texinfo: bav_set_parameters
 * Assign @var{Q} to @var{P}.
 */

BAV_DLL void
bav_set_parameters (
    bav_tableof_parameter P,
    bav_tableof_parameter Q)
{
  if (P != Q)
    {
      ba0_reset_table ((ba0_table) P);
      ba0_realloc2_table ((ba0_table) P, Q->size,
          (ba0_new_function *) & bav_new_parameter);
      while (P->size < Q->size)
        {
          bav_set_parameter (P->tab[P->size], Q->tab[P->size]);
          P->size += 1;
        }
    }
}

/*
 * texinfo: bav_switch_ring_parameters
 * Apply @code{bav_switch_ring_symbol} to each symbol occuring in the 
 * table @var{P}. The table @var{P} is modified. 
 * This low level function should be used in conjunction with 
 * @code{bav_set_differential_ring}.
 */

BAV_DLL void
bav_switch_ring_parameters (
    bav_tableof_parameter P,
    struct bav_differential_ring *R)
{
  bav_parameter a;
  ba0_int_p i, j;

  for (i = 0; i < P->size; i++)
    {
      a = P->tab[i];
      a->root = bav_switch_ring_symbol (a->root, R);
      for (j = 0; j < a->dep.size; j++)
        a->dep.tab[j] = bav_switch_ring_symbol (a->dep.tab[j], R);
    }
}

/*
 * texinfo: bav_init_parameter
 * Initialize @var{p}.
 */

BAV_DLL void
bav_init_parameter (
    bav_parameter p)
{
  p->root = BAV_NOT_A_SYMBOL;
  ba0_init_table ((ba0_table) & p->dep);
}

/*
 * texinfo: bav_new_parameter
 * Allocate a table of parameters, initialize it and return it.
 */

BAV_DLL bav_parameter
bav_new_parameter (
    void)
{
  bav_parameter p = (bav_parameter) ba0_alloc (sizeof (struct bav_parameter));

  bav_init_parameter (p);
  return p;
}

/*
 * texinfo: bav_set_parameter
 * Assign @var{q} to @var{p}.
 */

BAV_DLL void
bav_set_parameter (
    bav_parameter p,
    bav_parameter q)
{
  if (p != q)
    {
      p->root = q->root;
      ba0_set_table ((ba0_table) & p->dep, (ba0_table) & q->dep);
    }
}

/*
 * texinfo: bav_set_parameter_symbol_table
 * Assign @var{root} and @var{dep} to @var{p}.
 */

BAV_DLL void
bav_set_parameter_symbol_table (
    bav_parameter p,
    bav_symbol root,
    bav_tableof_symbol dep)
{
  p->root = root;
  ba0_set_table ((ba0_table) & p->dep, (ba0_table) dep);
}

BAV_DLL void *
bav_scanf_parameter (
    void *z)
{
  bav_parameter p = (bav_parameter) z;
  bav_symbol y;
  struct bav_tableof_symbol T;
  struct ba0_mark M;
  ba0_int_p i;
  ba0_indexed indexed;
  ba0_indices der_indices = (ba0_indices) 0;
  bool has_der_indices;
  char *s;

  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  ba0_push_another_stack ();
  ba0_record (&M);
  indexed = ba0_scanf_indexed (0, &has_der_indices, &bav_is_a_derivation);
  if (has_der_indices)
    der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];

  ba0_init_table ((ba0_table) & T);
  if (!has_der_indices || (has_der_indices && der_indices->po != '('
          && der_indices->Tindex.size == 0))
    {
      s = ba0_indexed_to_string (indexed);
      y = bav_R_string_to_symbol (s);
      if (y == BAV_NOT_A_SYMBOL)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
    }
  else
    {
      if (der_indices->po != '(')
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDIF);
      indexed->Tindic.size -= 1;
      s = ba0_indexed_to_string (indexed);
      y = bav_R_string_to_symbol (s);
      if (y == BAV_NOT_A_SYMBOL)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
      ba0_realloc_table ((ba0_table) & T, der_indices->Tindex.size);
      for (i = 0; i < der_indices->Tindex.size; i++)
        {
          s = ba0_indexed_to_string (der_indices->Tindex.tab[i]),
              T.tab[T.size] = bav_R_string_to_derivation (s);
/*
 * This should not happen since has_der_indices is true
 */
          if (T.tab[T.size] == BAV_NOT_A_SYMBOL)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          T.size += 1;
        }
    }
  ba0_pull_stack ();
  if (p == (bav_parameter) 0)
    p = bav_new_parameter ();
  bav_set_parameter_symbol_table (p, y, &T);
  ba0_restore (&M);
  return p;
}

BAV_DLL void
bav_printf_parameter (
    void *z)
{
  bav_parameter p = (bav_parameter) z;
  ba0_int_p i;

  bav_printf_symbol (p->root);
  if (p->dep.size > 0)
    {
      ba0_put_char ('(');
      for (i = 0; i < p->dep.size; i++)
        {
          ba0_printf ("%y", p->dep.tab[i]);
          if (i < p->dep.size - 1)
            ba0_put_char (',');
        }
      ba0_put_char (')');
    }
}

/*
 * texinfo: bav_is_a_parameter
 * Return @code{true} if @var{y} occurs as the root field of some
 * entry of the table @var{P}, @code{false} otherwise.
 * If @var{y} occurs in the table and @var{k} is nonzero then *@var{k} 
 * is assigned the index of the entry.
 */

BAV_DLL bool
bav_is_a_parameter (
    bav_symbol y,
    ba0_int_p *k,
    bav_tableof_parameter P)
{
  ba0_int_p i;

  for (i = 0; i < P->size; i++)
    if (y == P->tab[i]->root)
      {
        if (k != (ba0_int_p *) 0)
          *k = i;
        return true;
      }
  return false;
}

/*
 * texinfo: bav_is_zero_derivative_of_parameter
 * Return @code{true} if @var{v} is a zero derivative of some
 * element of @var{P}. Used by the parser of polynomials.
 */

BAV_DLL bool
bav_is_zero_derivative_of_parameter (
    bav_variable v,
    bav_tableof_parameter P)
{
  bav_variable x;
  ba0_int_p i, d;

  if (v->root->type != bav_dependent_symbol)
    return false;

  for (i = 0; i < P->size; i++)
    {
      if (v->root == P->tab[i]->root)
        {
          for (d = 0; d < v->order.size; d++)
            {
              if (v->order.tab[d] > 0)
                {
                  x = bav_R_derivation_index_to_derivation (d);
                  if (!ba0_member_table (x->root, (ba0_table) & P->tab[i]->dep))
                    return true;
                }
            }
        }
    }
  return false;
}

/*
 * texinfo: bav_zero_derivatives_of_parameter
 * Append to @var{nulles} the order @math{1} derivatives of 
 * @var{param} which are zero.
 */

BAV_DLL void
bav_zero_derivatives_of_parameter (
    bav_tableof_variable nulles,
    bav_parameter param)
{
  bav_variable v, x;
  ba0_int_p d;

  ba0_realloc_table ((ba0_table) nulles, nulles->size + bav_global.R.ders.size);
  v = bav_R_symbol_to_variable (param->root);
  for (d = 0; d < bav_global.R.ders.size; d++)
    {
      x = bav_R_derivation_index_to_derivation (d);
      if (!ba0_member_table (x->root, (ba0_table) & param->dep))
        {
          nulles->tab[nulles->size] = bav_diff_variable (v, x->root);
          nulles->size += 1;
        }
    }
}

/*
 * texinfo: bav_zero_derivatives_of_tableof_parameter
 * Append to @var{nulles} the order @math{1} derivatives of
 * any element of @var{P} which are zero.
 */

BAV_DLL void
bav_zero_derivatives_of_tableof_parameter (
    bav_tableof_variable nulles,
    bav_tableof_parameter P)
{
  ba0_int_p p;

  ba0_realloc_table ((ba0_table) nulles,
      nulles->size + P->size * bav_global.R.ders.size);
  for (p = 0; p < P->size; p++)
    bav_zero_derivatives_of_parameter (nulles, P->tab[p]);
}
