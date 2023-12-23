#include "bav_parameter.h"
#include "bav_variable.h"
#include "bav_differential_ring.h"
#include "bav_global.h"
#include "bav_term.h"

/* 
 * texinfo: bav_set_settings_variable
 * Assign @var{s} and @var{p} to the corresponding settings variables.
 * Set the prefix used for temporary variables to @var{tmp}.
 * Zero values are replaced by default values.
 */

BAV_DLL void
bav_set_settings_variable (
    ba0_scanf_function *s,
    ba0_printf_function *p,
    char *jet0,
    char *temp)
{
  bav_initialized_global.variable.scanf = s ? s : &bav_scanf_jet_variable;
  bav_initialized_global.variable.printf = p ? p : &bav_printf_jet_variable;
  bav_initialized_global.variable.jet0_string = jet0 ? jet0 : BAV_JET0_STRING;
  bav_initialized_global.variable.temp_string = temp ? temp : BAV_TEMP_STRING;
}

/*
 * texinfo: bav_get_settings_variable
 * Assign to *@var{s} and *@var{p} the values of the corresponding settings
 * variable. Assigns to *@var{tmp} the prefix used for temporary variables.
 * Parameters may be zero.
 */

BAV_DLL void
bav_get_settings_variable (
    ba0_scanf_function **s,
    ba0_printf_function **p,
    char **jet0,
    char **temp)
{
  if (s)
    *s = bav_initialized_global.variable.scanf;
  if (p)
    *p = bav_initialized_global.variable.printf;
  if (jet0)
    *jet0 = bav_initialized_global.variable.jet0_string;
  if (temp)
    *temp = bav_initialized_global.variable.temp_string;
}


static void
bav_init_variable (
    bav_variable v)
{
  v->root = (bav_symbol) 0;
  ba0_init_table ((ba0_table) & v->number);
  ba0_init_table ((ba0_table) & v->order);
  ba0_init_table ((ba0_table) & v->derivative);
}

/* 
 * texinfo: bav_new_variable
 * Allocate a new variable and return its address
 */

BAV_DLL bav_variable
bav_new_variable (
    void)
{
  bav_variable v;

  v = (bav_variable) ba0_alloc (sizeof (struct bav_variable));
  bav_init_variable (v);
  return v;
}

/*
 * texinfo: bav_not_a_variable
 * Return the constant @code{BAV_NOT_A_VARIABLE}.
 */

BAV_DLL bav_variable
bav_not_a_variable (
    void)
{
  return BAV_NOT_A_VARIABLE;
}

/*
 * texinfo: bav_order_variable
 * Return the order of @var{v} w.r.t. @var{d}.
 * If @var{v} is not a derivative or an operator or if @var{d} is not a 
 * derivation, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_Iorder
bav_order_variable (
    bav_variable v,
    bav_symbol d)
{
  bav_Inumber i;

  if (d->type != bav_independent_symbol ||
      (v->root->type != bav_dependent_symbol &&
          v->root->type != bav_operator_symbol))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  i = d->derivation_index;
  return v->order.tab[i];
}

/*
 * texinfo: bav_total_order_variable
 * Return the total order of  @var{v}.
 * If @var{v} is not a derivative or an operator, 
 * exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_Iorder
bav_total_order_variable (
    bav_variable v)
{
  bav_Inumber i;
  bav_Iorder cpt;

  if (v->root->type != bav_dependent_symbol &&
      v->root->type != bav_operator_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  cpt = 0;
  for (i = 0; i < v->order.size; i++)
    cpt += v->order.tab[i];
  return cpt;
}

/*
 * texinfo: bav_is_constant_variable
 * Return @code{true} if @var{v} is a constant w.r.t. derivation @var{s} 
 * (or w.r.t. all derivations, if @var{s} is zero).
 * If @var{v} is a derivative, this information is extracted from @var{P}.
 */

BAV_DLL bool
bav_is_constant_variable (
    struct bav_variable *v,
    struct bav_symbol *s,
    struct bav_tableof_parameter *P)
{
  bool is_constant;
  ba0_int_p j, k;

  if (s == BAV_NOT_A_SYMBOL)
    {
      if (bav_symbol_type_variable (v) == bav_independent_symbol)
        is_constant = false;
      else if (P != (struct bav_tableof_parameter *) 0 &&
          bav_is_a_parameter (v->root, &k, P))
        is_constant = P->tab[k]->dep.size == 0;
      else
        is_constant = false;
    }
  else
    {
      if (bav_symbol_type_variable (v) == bav_independent_symbol)
        is_constant = v->root != s;
      else if (P != (struct bav_tableof_parameter *) 0 &&
          bav_is_a_parameter (v->root, &k, P))
        {
          is_constant = true;
          for (j = 0; is_constant && j < P->tab[k]->dep.size; j++)
            is_constant = P->tab[k]->dep.tab[j] != s;
        }
      else
        is_constant = false;
    }
  return is_constant;
}

/*
 * texinfo: bav_diff_variable
 * Return the derivative of @var{v} w.r.t. @var{s}.
 * If @var{v} is not a derivative or an operator or if @var{s} is not
 * a derivation, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_variable
bav_diff_variable (
    bav_variable v,
    bav_symbol s)
{
  ba0_int_p i;

  if (v->root->type != bav_dependent_symbol &&
      v->root->type != bav_operator_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  i = s->derivation_index;
  if (v->derivative.tab[i] == BAV_NOT_A_VARIABLE)
    v->derivative.tab[i] = bav_R_derivative (v, s);
  return v->derivative.tab[i];
}

/*
 * texinfo: bav_diff2_variable
 * Return the derivative of @var{v} w.r.t. the derivation operator
 * encoded by @var{theta}.
 * If @var{v} is not a derivative or an operator or if some factor
 * of @var{theta} is not a derivation, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_variable
bav_diff2_variable (
    bav_variable v,
    bav_term theta)
{
  ba0_int_p i;

  for (i = 0; i < theta->size; i++)
    v = bav_diff_variable (v, theta->rg[i].var->root);
  return v;
}

/*
 * texinfo: bav_int_variable
 * Return the variable @var{u} whose derivative w.r.t. @var{s} is
 * equal to @var{v}.
 * If @var{v} is not a derivative or an operator, if @var{s} is not
 * a derivation, or @var{v} has zero order w.r.t. @var{s}, 
 * exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_variable
bav_int_variable (
    bav_variable v,
    bav_symbol s)
{
  bav_variable w;
  bav_symbol t;
  ba0_int_p i, j, k;

  i = s->derivation_index;
  if ((v->root->type != bav_dependent_symbol &&
          v->root->type != bav_operator_symbol) || v->order.tab[i] <= 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  w = bav_R_symbol_to_variable (v->root);
  for (k = 0; k < v->order.size; k++)
    {
      t = bav_R_derivation_index_to_derivation (k)->root;
      if (k == i)
        for (j = 0; j < v->order.tab[k] - 1; j++)
          w = bav_diff_variable (w, t);
      else
        for (j = 0; j < v->order.tab[k]; j++)
          w = bav_diff_variable (w, t);
    }
  return w;
}

/*
 * texinfo: bav_symbol_type_variable
 * Return the type of the symbol over which @var{v} is built.
 */

BAV_DLL enum bav_typeof_symbol
bav_symbol_type_variable (
    bav_variable v)
{
  return v->root->type;
}

/*
 * texinfo: bav_order_zero_variable
 * Return the order zero variable @var{v} is a derivative of.
 * If @var{v} is not a derivative or an operator, exception
 * @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_variable
bav_order_zero_variable (
    bav_variable v)
{
  if (v->root->type != bav_dependent_symbol &&
      v->root->type != bav_operator_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  return bav_R_symbol_to_variable (v->root);
}

/*
 * texinfo: bav_lcd_variable
 * Return the least common derivative of @var{v} and @var{w}.
 * If @var{v} and @var{w} are not both differential operators, or
 * if they are not derivatives of the same differential indeterminate,
 * exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_variable
bav_lcd_variable (
    bav_variable v,
    bav_variable w)
{
  bav_symbol t;
  ba0_int_p j;

  if ((v->root->type != bav_dependent_symbol &&
          v->root->type != bav_operator_symbol) || v->root != w->root)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  for (j = 0; j < v->order.size; j++)
    {
      t = bav_R_derivation_index_to_derivation (j)->root;
      while (v->order.tab[j] < w->order.tab[j])
        {
          if (v->derivative.tab[j] == BAV_NOT_A_VARIABLE)
            v->derivative.tab[j] = bav_R_derivative (v, t);
          v = v->derivative.tab[j];
        }
    }
  return v;
}

/*
 * texinfo: bav_disjoint_variables
 * Return @code{true} if, for every derivation @var{s}, the
 * order of @var{v} w.r.t. @var{s} is zero or the order of @var{w} w.r.t. 
 * @var{s} is zero.
 * If @var{v} and @var{w} are not derivatives of the same
 * differential indeterminate, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bool
bav_disjoint_variables (
    bav_variable v,
    bav_variable w)
{
  ba0_int_p i;

  if (v->root != w->root || v->root->type == bav_dependent_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  for (i = 0; i < v->order.size; i++)
    if (v->order.tab[i] != 0 && w->order.tab[i] != 0)
      return false;
  return true;
}

/*
 * texinfo: bav_is_derivative
 * Return @code{true} if @var{v} is a derivative of @var{w}.
 * May raise exception @code{BA0_ERRALG}.
 */

BAV_DLL bool
bav_is_derivative (
    bav_variable v,
    bav_variable w)
{
  ba0_int_p j;

  if (v->root != w->root)
    return false;
  if (v->root->type == bav_independent_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  for (j = 0; j < v->order.size; j++)
    if (v->order.tab[j] < w->order.tab[j])
      return false;
  return true;
}

/*
 * texinfo: bav_is_proper_derivative
 * Return @code{true} if @var{v} is a proper derivative of @var{w}.
 * If @var{v} and @var{w} are not derivatives of the same differential
 * indeterminate, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bool
bav_is_proper_derivative (
    bav_variable v,
    bav_variable w)
{
  ba0_int_p j;

  if (v->root != w->root || v == w)
    return false;
  if (v->root->type == bav_independent_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  for (j = 0; j < v->order.size; j++)
    if (v->order.tab[j] < w->order.tab[j])
      return false;
  return true;
}

/*
 * texinfo: bav_is_d_derivative
 * Return @code{true} if @var{v} is the derivative of @var{w} w.r.t.
 * derivation @var{d}.
 * If @var{v} and @var{w} are not derivatives of the same differential
 * indeterminate, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bool
bav_is_d_derivative (
    bav_variable v,
    bav_variable w,
    bav_symbol d)
{
  ba0_int_p j;

  if (v->root->type == bav_independent_symbol ||
      w->root->type == bav_independent_symbol ||
      d->type != bav_independent_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (v->root != w->root)
    return false;

  for (j = 0; j < v->order.size; j++)
    {
      if (d->derivation_index == j)
        {
          if (v->order.tab[j] != w->order.tab[j] + 1)
            return false;
        }
      else if (v->order.tab[j] != w->order.tab[j])
        return false;
    }
  return true;
}

/*
 * texinfo: bav_is_derivative2
 * Return @code{true} if @var{v} is the derivative of some element of @var{T}.
 * May raise exception @code{BA0_ERRALG} if some element of @var{T}
 * and @var{v} are not derivatives of the same differential indeterminate.
 */

BAV_DLL bool
bav_is_derivative2 (
    bav_variable v,
    bav_tableof_variable T)
{
  ba0_int_p i;
  bool found;

  for (i = 0, found = false; !found && i < T->size; i++)
    found = bav_is_derivative (v, T->tab[i]);
  return found;
}

/*
 * texinfo: bav_derivation_between_derivatives
 * Return a derivation @var{d} such that @var{v} (resp. @var{w})
 * is a derivative of the derivative of @var{w} (resp. @var{v}) w.r.t. @var{d}.
 * If @var{v} and @var{w} are not derivatives of the same differential
 * indeterminate, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL bav_variable
bav_derivation_between_derivatives (
    bav_variable v,
    bav_variable w)
{
  bav_Inumber j;

  if (v->root != w->root || v == w)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  else if (bav_is_derivative (w, v))
    BA0_SWAP (bav_variable, v, w);
  else if (!bav_is_derivative (v, w))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  j = 0;
  while (v->order.tab[j] == w->order.tab[j])
    j++;
  return bav_R_derivation_index_to_derivation (j);
}

/*
 * texinfo: bav_operator_between_derivatives
 * Assign to @var{T} the power product of derivations such that
 * @var{v} (resp. @var{w}) is the derivative @var{w} (resp. @var{v}) 
 * w.r.t. @var{T}.
 * If @var{v} and @var{w} are not derivatives of the same differential
 * indeterminate, exception @code{BA0_ERRALG} is raised.
 */

BAV_DLL void
bav_operator_between_derivatives (
    bav_term T,
    bav_variable v,
    bav_variable w)
{
  bav_variable x;

  if (bav_is_derivative (v, w))
    BA0_SWAP (bav_variable, v, w);

  bav_set_term_one (T);
  bav_realloc_term (T, bav_global.R.ders.size);
  while (v != w)
    {
      x = bav_derivation_between_derivatives (v, w);
      bav_mul_term_variable (T, T, x, 1);
      v = bav_diff_variable (v, x->root);
    }
}

static bav_variable
bav_basic_next_derivative (
    bav_variable v)
{
  bav_variable w;
  bav_symbol x;
  bav_Iorder d, d0, i;

  d = bav_total_order_variable (v);
  x = bav_global.R.vars.tab[bav_global.R.ders.tab[0]]->root;
  d0 = bav_order_variable (v, x);
  if (d == d0)
    {
      w = bav_order_zero_variable (v);
      x = bav_global.R.vars.tab[bav_global.R.ders.tab[bav_global.R.ders.size -
              1]]->root;
      for (i = 0; i < d + 1; i++)
        w = bav_diff_variable (w, x);
    }
  else
    {
      w = v;
      for (i = 0; i < d0; i++)
        w = bav_int_variable (w, x);
      i = 1;
      x = bav_global.R.vars.tab[bav_global.R.ders.tab[i]]->root;
      while (bav_order_variable (w, x) == 0)
        {
          i += 1;
          x = bav_global.R.vars.tab[bav_global.R.ders.tab[i]]->root;
        }
      w = bav_int_variable (w, x);
      i -= 1;
      x = bav_global.R.vars.tab[bav_global.R.ders.tab[i]]->root;
      for (i = 0; i <= d0; i++)
        w = bav_diff_variable (w, x);
    }
  return w;
}

/*
 * texinfo: bav_next_derivative
 * This function permits to enumerate the derivatives by increasing total
 * order. It returns the derivative which follows @var{v} and which is
 * not a derivative of any element of @var{T}. If no such derivative exists,
 * it returns the zero variable.
 * If @var{v} and some element of @var{T} are not derivatives of the 
 * same differential indeterminate, exception @code{BA0_ERRALG}
 * is raised.
 */

BAV_DLL bav_variable
bav_next_derivative (
    bav_variable v,
    bav_tableof_variable T)
{
  bav_variable w, x;
  ba0_int_p i;
  bool found;

  if (bav_symbol_type_variable (v) != bav_dependent_symbol ||
      bav_global.R.ders.size == 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
/*
 * w is the next derivative of w. 
 * If it is okay, return it
 */
  w = bav_basic_next_derivative (v);
  found = false;
  for (i = 0; !found && i < T->size; i++)
    found = bav_is_derivative (w, T->tab[i]);
  if (!found)
    return w;
/*
 * The next derivative, w, of v is not okay.
 */
  x = w;
  do
    {
      x = bav_basic_next_derivative (x);
      found = false;
      for (i = 0; !found && i < T->size; i++)
        found = bav_is_derivative (x, T->tab[i]);
    }
  while (found && !bav_is_derivative (x, w));
  return found ? BAV_NOT_A_VARIABLE : x;
}

/*
 * texinfo: bav_scanf_jet_variable
 * The function for parsing variables in the @code{jet} notation.
 * Empty square brackets are allowed but not mandatory behind 
 * order zero derivatives. 
 * The default function called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_jet_variable (
    void *z)
{
  bav_variable v;
  bav_symbol y;
  struct ba0_mark M;
  ba0_int_p i;
  ba0_indexed indexed;
  ba0_indices der_indices = (ba0_indices) 0;
  bool has_der_indices;
  char *s;

  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  ba0_record (&M);
  indexed = ba0_scanf_indexed (0, &has_der_indices, &bav_is_a_derivation);
/*
 * has_der_indices = true if the last INDEXED involves derivations only
 */
  if (has_der_indices)
    der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
  if (!has_der_indices || der_indices->po != '[')
    {
      s = ba0_indexed_to_string (indexed);
      v = bav_R_string_to_variable (s);
      if (v == BAV_NOT_A_VARIABLE)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
    }
  else
    {
      indexed->Tindic.size -= 1;
      s = ba0_indexed_to_string (indexed);
      v = bav_R_string_to_variable (s);
      if (v == BAV_NOT_A_VARIABLE && der_indices->Tindex.size == 0)
        {
/*
 * If the last INDEXED is '[]' then one may also try to incorporate
 * it in the symbol (a way to solve the notation ambiguity)
 */
          indexed->Tindic.size += 1;
          s = ba0_indexed_to_string (indexed);
          v = bav_R_string_to_variable (s);
        }
      if (v == BAV_NOT_A_VARIABLE)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
      if (v->root->type != bav_dependent_symbol &&
          v->root->type != bav_operator_symbol)
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBSD);
      for (i = 0; i < der_indices->Tindex.size; i++)
        {
          s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
          y = bav_R_string_to_derivation (s);
/*
 * This should not happen since has_der_indices is true
 */
          if (y == BAV_NOT_A_SYMBOL)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          v = bav_diff_variable (v, y);
        }
    }
  ba0_restore (&M);
  if (z != (void *) 0)
    *(bav_variable *) z = v;
  return v;
}

/*
 * texinfo: bav_scanf_jet0_variable
 * The function for parsing variables in the @code{jet0} notation.
 * Order zero variables are supposed to be indexed by @code{[0]}.
 * However, empty square brackets and no square brackets at all are
 * allowed.
 * The @code{0} character can be customized by modifying
 * @code{bav_initialized_global.variable.jet0_string}.
 * A function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_jet0_variable (
    void *z)
{
  bav_variable v;
  bav_symbol y;
  struct ba0_mark M;
  ba0_int_p i;
  ba0_indexed indexed;
  ba0_indices der_indices = (ba0_indices) 0;
  bool has_der_indices;
  char *s;

  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  ba0_record (&M);
  indexed = ba0_scanf_indexed (0, &has_der_indices, &bav_is_a_derivation);
/*
 * Special jet0 handling. 
 * If trailing [0] then remove the 0 and set has_der_indices to true
 */
  if (!has_der_indices && indexed->Tindic.size > 0)
    {
      der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
      if (der_indices->po == '[' && der_indices->Tindex.size == 1)
        {
          s = ba0_indexed_to_string (der_indices->Tindex.tab[0]);
          if (strcmp (s, bav_initialized_global.variable.jet0_string) == 0)
            {
              der_indices->Tindex.size -= 1;
              has_der_indices = true;
            }
        }
    }
/*
 * has_der_indices = true if the last INDEXED involves derivations only
 */
  if (has_der_indices)
    der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
  if (!has_der_indices || der_indices->po != '[')
    {
      s = ba0_indexed_to_string (indexed);
      v = bav_R_string_to_variable (s);
      if (v == BAV_NOT_A_VARIABLE)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
    }
  else
    {
      indexed->Tindic.size -= 1;
      s = ba0_indexed_to_string (indexed);
      v = bav_R_string_to_variable (s);
      if (v == BAV_NOT_A_VARIABLE && der_indices->Tindex.size == 0)
        {
/*
 * If the last INDEXED is '[]' then one may also try to incorporate
 * it in the symbol
 *
 * Actually, we do not worry about this case because the jet0 notation
 * is used only when the '[]' notation is not available.
 */
          indexed->Tindic.size += 1;
          s = ba0_indexed_to_string (indexed);
          v = bav_R_string_to_variable (s);
        }
      if (v == BAV_NOT_A_VARIABLE)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
      if (v->root->type != bav_dependent_symbol &&
          v->root->type != bav_operator_symbol)
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRBSD);
      for (i = 0; i < der_indices->Tindex.size; i++)
        {
          s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
          y = bav_R_string_to_derivation (s);
/*
 * This should not happen since has_der_indices is true
 */
          if (y == BAV_NOT_A_SYMBOL)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          v = bav_diff_variable (v, y);
        }
    }
  ba0_restore (&M);
  if (z != (void *) 0)
    *(bav_variable *) z = v;
  return v;
}

/*
 * Subfunction of bav_scanf_diff_variable
 * Reads non differentiated variables of the form: u(x,y)
 * where u is a dependent variable
 * x,y is the sequence of the derivations in the same order as in bav_global.R.ders
 *
 * If the function symbol is present in the bav_global.parameters table, then
 * the notation provided in that table is required.
 */

static bav_variable
bav_scanf_non_diff_variable (
    char *mesgerr)
{
  bav_variable v;
  bav_symbol y, d;
  struct ba0_mark M;
  ba0_int_p i, k;
  ba0_indexed indexed;
  ba0_indices der_indices = (ba0_indices) 0;
  bool has_der_indices, tolerated, found;
  char *s;

  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (mesgerr);

  ba0_record (&M);
  indexed = ba0_scanf_indexed (0, &has_der_indices, &bav_is_a_derivation);
  if (has_der_indices)
    der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
/*
 * has_der_indices = the last INDEXED is a list of derivations.
 * This list may be empty.
 *
 * tolerated = indexed is tolerated as a symbol i.e. it has no terminating
 *             list of derivations or an empty one, which is not '()'
 */
  tolerated = !has_der_indices ||
      (has_der_indices &&
      der_indices->po != '(' && der_indices->Tindex.size == 0);

  if (tolerated)
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
      if (der_indices->po != '(' || !has_der_indices)
        BA0_RAISE_PARSER_EXCEPTION (mesgerr);
      indexed->Tindic.size -= 1;
      s = ba0_indexed_to_string (indexed);
      y = bav_R_string_to_symbol (s);
      if (y == BAV_NOT_A_SYMBOL)
        {
          (*bav_initialized_global.common.unknown) (indexed);
          BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
        }
    }
/*
 * At this step, the symbol is recognized. It is in y.
 */
  if (y->type == bav_dependent_symbol)
    {
/*
 * found = y is dependent, declared in bav_global.parameters at index k.
 * One then needs to check whether the order of the independent variables
 * following y is correct or not. Possible errors have nothing to do with
 * not recognizing a symbol.
 */
      found = bav_is_a_parameter (y, &k, &bav_global.parameters);
      if (found && has_der_indices)
        {
          if (der_indices->Tindex.size !=
              bav_global.parameters.tab[k]->dep.size)
            BA0_RAISE_PARSER_EXCEPTION (mesgerr);
          for (i = 0; i < der_indices->Tindex.size; i++)
            {
              s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
              d = bav_global.parameters.tab[k]->dep.tab[i];
              if (strcmp (s, d->ident) != 0)
                BA0_RAISE_PARSER_EXCEPTION (mesgerr);
            }
        }
      else if (found)
        {
          if (bav_global.parameters.tab[k]->dep.size > 0)
            BA0_RAISE_PARSER_EXCEPTION (mesgerr);
        }
      else if (!found && has_der_indices)
        {
          if (der_indices->Tindex.size != bav_global.R.ders.size)
            BA0_RAISE_PARSER_EXCEPTION (mesgerr);
          for (i = 0; i < der_indices->Tindex.size; i++)
            {
              s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
              d = bav_global.R.syms.tab[bav_global.R.ders.tab[i]];
              if (strcmp (s, d->ident) != 0)
                BA0_RAISE_PARSER_EXCEPTION (mesgerr);
            }
        }
      else
        {
          if (bav_global.R.ders.size > 0)
            BA0_RAISE_PARSER_EXCEPTION (mesgerr);
        }
    }
  else if (!tolerated)
    BA0_RAISE_PARSER_EXCEPTION (mesgerr);

  ba0_restore (&M);
  v = bav_R_symbol_to_variable (y);
  return v;
}

/*
 * Reads a variable of the form: diff(diff(u(x,y),y,x)) or diff(u(x,y),x,x)
 */

static void *
bav_scanf_generic_diff_variable (
    void *z,
    char *mesgerr)
{
  bav_variable v;
  bav_symbol d;
  struct ba0_mark M;
  char *s;

  ba0_record (&M);
  s = ba0_value_token_analex ();
  if (strcmp (s, "diff") == 0 || strcmp (s, "Diff") == 0)
    {
      ba0_get_token_analex ();
      if (!ba0_sign_token_analex ("("))
        BA0_RAISE_PARSER_EXCEPTION (mesgerr);
      ba0_get_token_analex ();
      v = bav_scanf_generic_diff_variable ((void *) 0, mesgerr);
      ba0_get_token_analex ();

      while (ba0_sign_token_analex (","))
        {
          ba0_get_token_analex ();
          d = bav_scanf_symbol ((void *) 0);
          v = bav_diff_variable (v, d);
          ba0_get_token_analex ();
        }

      if (!ba0_sign_token_analex (")"))
        BA0_RAISE_PARSER_EXCEPTION (mesgerr);
    }
  else
    v = bav_scanf_non_diff_variable (mesgerr);

  ba0_restore (&M);

  if (z != (void *) 0)
    *(bav_variable *) z = v;

  return v;
}

/*
 * texinfo: bav_scanf_diff_variable
 * The function for parsing variables in the Maple @code{diff} or
 * @code{Diff} notations.
 * A function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_diff_variable (
    void *z)
{
/*
    bav_global.variable.diff_string = "diff";
 */
  return bav_scanf_generic_diff_variable (z, BAV_ERRDIF);
}

BAV_DLL void *
bav_scanf_Diff_variable (
    void *z)
{
/*
    bav_global.variable.diff_string = "Diff";
 */
  return bav_scanf_generic_diff_variable (z, BAV_ERRDIF);
}

/*
 * texinfo: bav_scanf_sympy_Derivative_variable
 * The function for parsing variables in the Python3/sympy
 * @code{Derivative} notation.
 *  function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_sympy_Derivative_variable (
    void *z)
{
  struct ba0_mark M;
  struct bav_variable *v;
  struct bav_symbol *d;
  char *s;

  ba0_record (&M);
  s = ba0_value_token_analex ();
  if (strcmp (s, "Derivative") == 0)
    {
      ba0_get_token_analex ();
      if (!ba0_sign_token_analex ("("))
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRSPY);
      ba0_get_token_analex ();
      v = bav_scanf_sympy_Derivative_variable (z);
      ba0_get_token_analex ();

      while (ba0_sign_token_analex (","))
        {
          ba0_get_token_analex ();
          if (ba0_sign_token_analex ("("))
            {
              ba0_int_p j, k;

              ba0_get_token_analex ();
              d = bav_scanf_symbol ((void *) 0);
              ba0_get_token_analex ();
              if (!ba0_sign_token_analex (","))
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRSPY);
              ba0_get_token_analex ();
              if (ba0_type_token_analex () != ba0_integer_token)
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRSPY);
              k = atoi (ba0_value_token_analex ());
              if (k < 1)
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRSPY);
              for (j = 0; j < k; j++)
                v = bav_diff_variable (v, d);
              ba0_get_token_analex ();
              if (!ba0_sign_token_analex (")"))
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRSPY);
            }
          else
            {
              d = bav_scanf_symbol ((void *) 0);
              v = bav_diff_variable (v, d);
            }
          ba0_get_token_analex ();
        }

      if (!ba0_sign_token_analex (")"))
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRSPY);
    }
  else
    v = bav_scanf_non_diff_variable (BAV_ERRSPY);

  ba0_restore (&M);

  if (z != (void *) 0)
    *(bav_variable *) z = v;

  return v;
}

static void *
bav_scanf_generic_D_variable (
    void *z,
    ba0_int_p offset)
{
  bav_variable v, d;
  struct ba0_tableof_int_p T;
  struct ba0_mark M;
  char *s;
  ba0_int_p i, j, k;

  ba0_record (&M);
  ba0_init_table ((ba0_table) & T);

  s = ba0_value_token_analex ();
  if (strcmp (s, "D") == 0)
    {
      ba0_get_token_analex ();

      BA0_TRY
      {
        if (ba0_sign_token_analex ("["))
          ba0_scanf ("%t[%d]", &T);
      }
      BA0_CATCH
      {
        if (ba0_global.exception.raised == BA0_ERROOM ||
            ba0_global.exception.raised == BA0_ERRALR)
          BA0_RE_RAISE_EXCEPTION;
        BA0_RAISE_EXCEPTION (BAV_ERRDVR);
      }
      BA0_ENDTRY;

      ba0_get_token_analex ();
      if (!ba0_sign_token_analex ("("))
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDVR);
      ba0_get_token_analex ();
      if (ba0_type_token_analex () != ba0_string_token)
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDVR);

      s = ba0_scanf_indexed_string ((void *) 0);

      ba0_get_token_analex ();
      if (!ba0_sign_token_analex (")"))
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDVR);
/*
 * One erases the first ')' of D(f)(x) so that the parser reads f(x)
 */
      ba0_unget_given_token_analex (s, ba0_string_token, false);
      ba0_get_token_analex ();
    }
  v = bav_scanf_non_diff_variable (BAV_ERRDVR);
  if (!bav_is_a_parameter (v->root, &k, &bav_global.parameters))
    {
      for (i = 0; i < T.size; i++)
        {
          d = bav_R_derivation_index_to_derivation (T.tab[i] - offset);
          v = bav_diff_variable (v, d->root);
        }
    }
  else
    {
      for (i = 0; i < T.size; i++)
        {
          j = bav_global.parameters.tab[k]->dep.tab[T.tab[i] - offset]->index;
          d = bav_R_derivation_index_to_derivation (j);
          v = bav_diff_variable (v, d->root);
        }
    }

  ba0_restore (&M);
  if (z != (void *) 0)
    *(bav_variable *) z = v;
  return v;
}

/*
 * texinfo: bav_scanf_sage_D_variable
 * The function for parsing variables in the Sagemath @code{D} notation.
 * A function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_sage_D_variable (
    void *z)
{
  return bav_scanf_generic_D_variable (z, 0);
}

/*
 * texinfo: bav_scanf_maple_D_variable
 * The function for parsing variables in the Maple @code{D} notation.
 * A function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_maple_D_variable (
    void *z)
{
  return bav_scanf_generic_D_variable (z, 1);
}

static void *
bav_scanf_generic_all_notations_variable (
    void *z,
    ba0_int_p offset,
    ba0_int_p *notations)
{
  bav_variable v = BAV_NOT_A_VARIABLE;  /* to avoid a warning */
  bav_symbol y, d;
  ba0_indexed indexed;
  ba0_indices der_indices;
  struct ba0_mark M;
  ba0_int_p i, k, n = 0;        /* idem */
  char *s;
  bool could_be_D, has_der_indices, found;

  *notations = 0;

  if (ba0_type_token_analex () != ba0_string_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  ba0_record (&M);

  s = ba0_value_token_analex ();

  if (strcmp (s, "diff") == 0)
    *notations |= BAV_diff_FLAG;
  else if (strcmp (s, "Diff") == 0)
    *notations |= BAV_Diff_FLAG;
  if (*notations)
    v = bav_scanf_generic_diff_variable ((void *) 0, BAV_ERRDIF);
  else
    {
      could_be_D = strcmp (s, "D") == 0;
      if (could_be_D)
        n = ba0_get_counter_analex ();
/*
 * Adapted from bav_scanf_jet_variable and bav_scanf_non_diff_variable
 */
      indexed = ba0_scanf_indexed (0, &has_der_indices, &bav_is_a_derivation);
      if (has_der_indices)
        der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
/*
 * has_der_indices = true if the last INDEXED only involve derivations
 */
      if (!has_der_indices)
        {
/*
 * The last INDEXED does not involve derivations only.
 * Thus it must be part of the symbol.
 */
          s = ba0_indexed_to_string (indexed);
          v = bav_R_string_to_variable (s);
          if (v == BAV_NOT_A_VARIABLE)
            {
              (*bav_initialized_global.common.unknown) (indexed);
              BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
            }
/*
 * In the case of an independent symbol, all notations are possible.
 * Otherwise, 
 *    Notation could be jet.
 *    It could also be diff, Diff, D either if we are in the algebraic
 *    case or in the case of a parameter with no dependency.
 */
          if (v->root->type == bav_independent_symbol)
            *notations |= BAV_jet_FLAG | BAV_tjet_FLAG |
                BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
          else
            {
              *notations |= BAV_jet_FLAG;
              if (bav_global.R.ders.size == 0 ||
                  (bav_is_a_parameter (v->root, &k,
                          &bav_global.parameters)
                      && bav_global.parameters.tab[k]->dep.size == 0))
                *notations |= BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
            }
        }
      else if (der_indices->po == '[' && der_indices->Tindex.size == 0)
        {
/*
 * The last INDEXED is '[]'. 
 * If, removing it, one gets a symbol then the notation is tjet. 
 * Otherwise, there is still a chance it is part of the symbol and we
 * are back to the above case.
 */
          der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
          indexed->Tindic.size -= 1;
          s = ba0_indexed_to_string (indexed);
          v = bav_R_string_to_variable (s);
          if (v != BAV_NOT_A_VARIABLE)
            {
              if (v->root->type == bav_independent_symbol)
                *notations |= BAV_jet_FLAG | BAV_tjet_FLAG |
                    BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
              else
                *notations |= BAV_tjet_FLAG;
            }
          else
            {
              indexed->Tindic.size += 1;
              s = ba0_indexed_to_string (indexed);
              v = bav_R_string_to_variable (s);
              if (v == BAV_NOT_A_VARIABLE)
                {
                  (*bav_initialized_global.common.unknown) (indexed);
                  BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
                }
/*
 * See above
 */
              if (v->root->type == bav_independent_symbol)
                *notations |= BAV_jet_FLAG | BAV_tjet_FLAG |
                    BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
              else
                {
                  *notations |= BAV_jet_FLAG;
                  if (bav_global.R.ders.size == 0 ||
                      (bav_is_a_parameter (v->root, &k,
                              &bav_global.parameters)
                          && bav_global.parameters.tab[k]->dep.size == 0))
                    *notations |= BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
                }
            }
        }
      else if (der_indices->po == '[')
        {
          *notations |= BAV_jet_FLAG | BAV_tjet_FLAG;
/*
 * A derivative, with positive order, in jet or tjet notation
 */
          der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
          indexed->Tindic.size -= 1;
          s = ba0_indexed_to_string (indexed);
          v = bav_R_string_to_variable (s);
          if (v == BAV_NOT_A_VARIABLE)
            {
              (*bav_initialized_global.common.unknown) (indexed);
              BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
            }
          if (v->root->type != bav_dependent_symbol &&
              v->root->type != bav_operator_symbol)
            BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
          for (i = 0; i < der_indices->Tindex.size; i++)
            {
              s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
              y = bav_R_string_to_derivation (s);
/*
 * This should not happen since has_der_indices is true
 */
              if (y == BAV_NOT_A_SYMBOL)
                BA0_RAISE_EXCEPTION (BA0_ERRALG);
              v = bav_diff_variable (v, y);
            }
        }
      else if (der_indices->po == '(')
        {
          *notations |= BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
/*
 * A derivative, of order zero, in diff, Diff or D notation
 */
          der_indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
          indexed->Tindic.size -= 1;
          s = ba0_indexed_to_string (indexed);
          y = bav_R_string_to_symbol (s);
          if (y != BAV_NOT_A_SYMBOL)
            {
              if (y->type != bav_dependent_symbol)
                BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
              found = bav_is_a_parameter (y, &k, &bav_global.parameters);
              if (found)
                {
                  if (der_indices->Tindex.size !=
                      bav_global.parameters.tab[k]->dep.size)
                    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
                  for (i = 0; i < der_indices->Tindex.size; i++)
                    {
                      s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
                      d = bav_global.parameters.tab[k]->dep.tab[i];
                      if (strcmp (s, d->ident) != 0)
                        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
                    }
                }
              else
                {
                  if (der_indices->Tindex.size != bav_global.R.ders.size)
                    BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
                  for (i = 0; i < der_indices->Tindex.size; i++)
                    {
                      s = ba0_indexed_to_string (der_indices->Tindex.tab[i]);
                      d = bav_global.R.syms.tab[bav_global.R.ders.tab[i]];
                      if (strcmp (s, d->ident) != 0)
                        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
                    }
                }
              v = bav_R_symbol_to_variable (y);
            }
          else if (could_be_D)
            {
              *notations |= BAV_D_FLAG;
              n = ba0_get_counter_analex () - n;
              ba0_unget_token_analex (n);
              v = bav_scanf_generic_D_variable ((void *) 0, offset);
            }
          else
            {
              (*bav_initialized_global.common.unknown) (indexed);
              BA0_RAISE_PARSER_EXCEPTION (BAV_ERRUSY);
            }
        }
      else
        BA0_RAISE_PARSER_EXCEPTION (BAV_ERRDFV);
    }
  ba0_restore (&M);
  if (z != (void *) 0)
    *(bav_variable *) z = v;
  return v;
}

/*
 * texinfo: bav_scanf_sage_all_variable
 * The function for parsing variables in Sagemath.
 * The set of compatible notations is stored in the
 * global variable @code{bav_global.variable.notations}.
 * A function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_sage_all_variable (
    void *z)
{
  ba0_int_p notations;
  bav_variable v;

  v = bav_scanf_generic_all_notations_variable (z, 0, &notations);
  bav_global.variable.notations &= notations;
  return v;
}

/*
 * texinfo: bav_scanf_maple_all_variable
 * The function for parsing variables in Maple.
 * The set of compatible notations is stored in the
 * global variable @code{bav_global.variable.notations}.
 * A function that may be called by @code{ba0_scanf/%v}.
 */

BAV_DLL void *
bav_scanf_maple_all_variable (
    void *z)
{
  ba0_int_p notations;
  bav_variable v;

  v = bav_scanf_generic_all_notations_variable (z, 1, &notations);
  bav_global.variable.notations &= notations;
  return v;
}

/*
 * texinfo: bav_reset_notations
 * Set @code{bav_global.variable.notations} to all notations.
 */

BAV_DLL void
bav_reset_notations (
    void)
{
  bav_global.variable.notations =
      BAV_jet_FLAG | BAV_tjet_FLAG | BAV_diff_FLAG | BAV_Diff_FLAG | BAV_D_FLAG;
}

/*
 * texinfo: bav_get_notations
 * Return @code{bav_global.variable.notations}.
 */

BAV_DLL ba0_int_p
bav_get_notations (
    void)
{
#define PRINT 1
#if defined (PRINT)
  if (bav_global.variable.notations & BAV_jet_FLAG)
    printf ("jet ");
  if (bav_global.variable.notations & BAV_tjet_FLAG)
    printf ("tjet ");
  if (bav_global.variable.notations & BAV_diff_FLAG)
    printf ("diff ");
  if (bav_global.variable.notations & BAV_Diff_FLAG)
    printf ("Diff ");
  if (bav_global.variable.notations & BAV_D_FLAG)
    printf ("D ");
  printf ("\n");
#endif
  return bav_global.variable.notations;
}

BAV_DLL void *
bav_scanf_variable (
    void *z)
{
  void *res;
#define OLD_CODE 1
#if defined (OLD_CODE)
  if (bav_initialized_global.variable.scanf != (ba0_scanf_function *) 0)
    res = (*bav_initialized_global.variable.scanf) (z);
  else
    {
      BA0_RAISE_EXCEPTION (BA0_ERRALG);
      res = bav_scanf_jet_variable (z);
    }
#else
  if (bav_initialized_global.variable.scanf == &bav_scanf_sage_D_variable)
    res = bav_scanf_sage_all_variable (z);
  else
    res = bav_scanf_maple_all_variable (z);
#endif
  return res;
}

/*
 * texinfo: bav_printf_jet_variable
 * Print a variable following in the @code{jet} notation.
 * The default function called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_jet_variable (
    void *z)
{
  bav_variable v = (bav_variable) z;
  bav_variable d;
  bav_Inumber i, j;
  bool yet;

  bav_printf_symbol (v->root);
  if ((v->root->type == bav_dependent_symbol ||
          v->root->type == bav_operator_symbol) &&
      bav_total_order_variable (v) > 0)
    {
      ba0_put_char ('[');
      yet = false;
      for (i = 0; i < v->order.size; i++)
        {
          if (v->order.tab[i] != 0)
            {
              d = bav_R_derivation_index_to_derivation (i);
              for (j = 0; j < v->order.tab[i]; j++)
                {
                  if (yet)
                    ba0_put_char (',');
                  else
                    yet = true;
                  bav_printf_symbol (d->root);
                }
            }
        }
      ba0_put_char (']');
    }
}

/*
 * texinfo: bav_printf_jet_wesb_variable
 * The function for printing variables in the @code{tjet} notation.
 * Order zero derivatives are followed by empty square brackets.
 * This function can be called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_jet_wesb_variable (
    void *z)
{
  bav_variable v = (bav_variable) z;
  bav_variable d;
  bav_Inumber i, j;
  bool yet;

  bav_printf_symbol (v->root);
  if ((v->root->type == bav_dependent_symbol ||
          v->root->type == bav_operator_symbol) &&
      !bav_is_constant_variable (v, BAV_NOT_A_SYMBOL, &bav_global.parameters))
    {
      ba0_put_char ('[');
      yet = false;
      for (i = 0; i < v->order.size; i++)
        {
          if (v->order.tab[i] != 0)
            {
              d = bav_R_derivation_index_to_derivation (i);
              for (j = 0; j < v->order.tab[i]; j++)
                {
                  if (yet)
                    ba0_put_char (',');
                  else
                    yet = true;
                  bav_printf_symbol (d->root);
                }
            }
        }
      ba0_put_char (']');
    }
}

/*
 * texinfo: bav_printf_jet0_variable
 * The function for printing variables in the @code{jet0} notation.
 * Order zero derivatives are followed by @code{[0]}.
 * The @code{0} character can be customized by modifying
 * @code{bav_initialized_global.variable.jet0_string}
 * This function can be called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_jet0_variable (
    void *z)
{
  bav_variable v = (bav_variable) z;
  bav_variable d;
  bav_Inumber i, j;
  bool yet;

  bav_printf_symbol (v->root);
  if ((v->root->type == bav_dependent_symbol ||
          v->root->type == bav_operator_symbol) &&
      !bav_is_constant_variable (v, BAV_NOT_A_SYMBOL, &bav_global.parameters))
    {
      ba0_put_char ('[');
      yet = false;
      for (i = 0; i < v->order.size; i++)
        {
          if (v->order.tab[i] != 0)
            {
              d = bav_R_derivation_index_to_derivation (i);
              for (j = 0; j < v->order.tab[i]; j++)
                {
                  if (yet)
                    ba0_put_char (',');
                  else
                    yet = true;
                  bav_printf_symbol (d->root);
                }
            }
        }
      if (!yet)
        ba0_put_string (bav_initialized_global.variable.jet0_string);
      ba0_put_char (']');
    }
}

/*
 * texinfo: bav_printf_LaTeX_variable
 * The function for printing variables in the @code{jet} notation
 * using LaTeX indices.
 * This function can be called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_LaTeX_variable (
    void *z)
{
  bav_variable v = (bav_variable) z;
  bav_variable d;
  bav_Inumber i, j;
  bool yet;

  bav_printf_symbol (v->root);

  if (v->root->type != bav_dependent_symbol)
    return;

  yet = false;
  for (i = 0; i < v->order.size && !yet; i++)
    yet = v->order.tab[i] > 0;

  if (!yet)
    return;

  ba0_put_char ('_');
  ba0_put_char ('{');
  for (i = 0; i < v->order.size; i++)
    {
      if (v->order.tab[i] != 0)
        {
          d = bav_R_derivation_index_to_derivation (i);
          for (j = 0; j < v->order.tab[i]; j++)
            bav_printf_symbol (d->root);
        }
    }
  ba0_put_char ('}');
}

static void
bav_printf_generic_D_variable (
    void *z,
    ba0_int_p offset)
{
  bav_variable v = (bav_variable) z;
  bav_variable d;
  bav_parameter p;
  bav_Iorder order;
  bav_Inumber i, j;
  ba0_int_p k;
  bool yet;

  switch (v->root->type)
    {
    case bav_temporary_symbol:
    case bav_independent_symbol:
      bav_printf_symbol (v->root);
      break;
    case bav_operator_symbol:
      BA0_RAISE_EXCEPTION (BA0_ERRNYP);
      break;
    case bav_dependent_symbol:
      order = bav_total_order_variable (v);
/*
 * D [...]
 */
      if (order > 0)
        {
          ba0_put_string ("D");
          ba0_put_char ('[');
          yet = false;
          for (i = 0; i < v->order.size; i++)
            {
              if (v->order.tab[i] != 0)
                {
                  for (j = 0; j < v->order.tab[i]; j++)
                    {
                      if (yet)
                        ba0_printf (",%d", i + offset);
                      else
                        ba0_printf ("%d", i + offset);
                      yet = true;
                    }
                }
            }
          ba0_put_char (']');
        }
/*
 * u(x,y)
 * beware to the special case of non differential problems
 */
      if (bav_is_a_parameter (v->root, &k, &bav_global.parameters))
        {
          p = bav_global.parameters.tab[k];
          if (order > 0)
            {
              ba0_put_char ('(');
              bav_printf_symbol (p->root);
              ba0_put_char (')');
            }
          else
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
      else
        {
          if (order > 0)
            {
              ba0_put_char ('(');
              bav_printf_symbol (v->root);
              ba0_put_char (')');
            }
          else
            bav_printf_symbol (v->root);
          if (v->order.size > 0)
            {
              ba0_put_char ('(');
              for (i = 0; i < v->order.size; i++)
                {
                  d = bav_R_derivation_index_to_derivation (i);
                  bav_printf_symbol (d->root);
                  if (i < v->order.size - 1)
                    ba0_put_char (',');
                  else
                    ba0_put_char (')');
                }
            }
        }
      break;
    }
}

/*
 * texinfo: bav_printf_maple_D_variable
 * The function for printing variables in the Maple @code{D} notation.
 * This function can be called by @code{ba0_printf/%v}.
 */


BAV_DLL void
bav_printf_maple_D_variable (
    void *z)
{
  bav_printf_generic_D_variable (z, 1);
}

/*
 * Subfunction of printf_diff_variable and printf_sympy_variable
 * Print the (non-differentiated) function (e.g. u(x,y))
 * Take care to the special case of parameters
 */

static void
bav_printf_uxy_variable (
    struct bav_variable *v)
{
  ba0_int_p i;

  if (bav_is_a_parameter (v->root, &i, &bav_global.parameters))
    ba0_printf ("%param", bav_global.parameters.tab[i]);
  else
    {
      bav_printf_symbol (v->root);
      if (v->order.size > 0)
        {
          ba0_put_char ('(');
          for (i = 0; i < v->order.size; i++)
            {
              struct bav_variable *d;
              d = bav_R_derivation_index_to_derivation (i);
              bav_printf_symbol (d->root);
              if (i < v->order.size - 1)
                ba0_put_char (',');
              else
                ba0_put_char (')');
            }
        }
    }
}

/*
 * Prints a variable using the diff format
 * If a symbol is present in the bav_global.parameters table then a special
 * notation is applied.
 */

static void
bav_printf_generic_diff_variable (
    void *z)
{
  bav_variable v = (bav_variable) z;
  bav_variable d;
  bav_Iorder order;
  bav_Inumber i, j;

  switch (v->root->type)
    {
    case bav_temporary_symbol:
    case bav_independent_symbol:
      bav_printf_symbol (v->root);
      break;
    case bav_operator_symbol:
      BA0_RAISE_EXCEPTION (BA0_ERRNYP);
      break;
    case bav_dependent_symbol:
      order = bav_total_order_variable (v);
/*
 * diff (
 */
      if (order > 0)
        {
          ba0_put_string (bav_global.variable.diff_string);
          ba0_put_char (' ');
          ba0_put_char ('(');
        }
      bav_printf_uxy_variable (v);
/*
 * ,x ,x, y)
 */
      if (order > 0)
        {
          for (i = 0; i < v->order.size; i++)
            {
              if (v->order.tab[i] != 0)
                {
                  d = bav_R_derivation_index_to_derivation (i);
                  for (j = 0; j < v->order.tab[i]; j++)
                    {
                      ba0_put_char (',');
                      ba0_put_char (' ');
                      bav_printf_symbol (d->root);
                    }
                }
            }
          ba0_put_char (')');
        }
      break;
    }
}

/*
 * texinfo: bav_printf_diff_variable
 * The function for printing variables in the Maple @code{diff} notation.
 * This function can be called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_diff_variable (
    void *z)
{
  bav_global.variable.diff_string = "diff";
  bav_printf_generic_diff_variable (z);
}

/*
 * texinfo: bav_printf_Diff_variable
 * The function for printing variables in the Maple @code{Diff} notation.
 * This function can be called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_Diff_variable (
    void *z)
{
  bav_global.variable.diff_string = "Diff";
  bav_printf_generic_diff_variable (z);
}

/*
 * texinfo: bav_printf_sympy_Derivative_variable
 * The function for printing variables in the Python3/sympy
 * @code{Derivative} notation.
 * This function can be called by @code{ba0_printf/%v}.
 */

BAV_DLL void
bav_printf_sympy_Derivative_variable (
    void *z)
{
  bav_variable v = (bav_variable) z;
  ba0_int_p k;

  if (v->root->type == bav_dependent_symbol)
    k = bav_total_order_variable (v);
  else
    k = 0;
  if (k == 0)
    bav_printf_diff_variable (v);
  else
    {
      bav_variable d;

      ba0_put_string ("Derivative (");
      bav_printf_uxy_variable (v);
      for (int i = 0; i < v->order.size; i++)
        {
          if (v->order.tab[i] != 0)
            {
              ba0_put_char (',');
              d = bav_R_derivation_index_to_derivation (i);
              if (v->order.tab[i] == 1)
                bav_printf_symbol (d->root);
              else
                {
                  ba0_put_char ('(');
                  bav_printf_symbol (d->root);
                  ba0_put_char (',');
                  ba0_put_int_p (v->order.tab[i]);
                  ba0_put_char (')');
                }
            }
        }
      ba0_put_char (')');
    }
}

BAV_DLL void
bav_printf_variable (
    void *z)
{
  if (ba0_global.common.LaTeX)
    bav_printf_LaTeX_variable (z);
  else if (bav_initialized_global.variable.printf != (ba0_printf_function *) 0)
    (*bav_initialized_global.variable.printf) (z);
  else
    {
      BA0_RAISE_EXCEPTION (BA0_ERRALG);
      bav_printf_jet_variable (z);
    }
}

/*
 * texinfo: bav_gt_index_variable
 * Return @code{true} if the index of @var{x} is greater than that of @var{y}.
 */

BAV_DLL bool
bav_gt_index_variable (
    void *x,
    void *y)
{
  bav_variable v = (bav_variable) x, w = (bav_variable) y;

  return v->index > w->index;
}

/*
 * texinfo: bav_gt_variable
 * Return @code{true} if @var{x} is greater than @var{y} w.r.t.
 * the current ordering.
 */

BAV_DLL bool
bav_gt_variable (
    void *x,
    void *y)
{
  bav_variable v = (bav_variable) x, w = (bav_variable) y;

  return bav_R_variable_number (v) > bav_R_variable_number (w);
}

/*
 * For qsort. See below
 */

static int
comp_variable_ascending (
    const void *x,
    const void *y)
{
  bav_variable v = *(bav_variable *) x;
  bav_variable w = *(bav_variable *) y;

  if (v == w)
    return 0;
  else if (bav_gt_variable (v, w))
    return 1;
  else
    return -1;
}

static int
comp_variable_descending (
    const void *x,
    const void *y)
{
  bav_variable v = *(bav_variable *) x;
  bav_variable w = *(bav_variable *) y;

  if (v == w)
    return 0;
  else if (bav_gt_variable (v, w))
    return -1;
  else
    return 1;
}

/*
 * texinfo: bav_sort_tableof_variable
 * Sort @var{T} in place in ascending order w.r.t. the current ordering, 
 * if @var{mode} is @code{ba0_ascending_mode}, or in descending order, if
 * @var{mode} is @code{ba0_descending_mode}.
 */

BAV_DLL void
bav_sort_tableof_variable (
    bav_tableof_variable T,
    enum ba0_sort_mode mode)
{
  switch (mode)
    {
    case ba0_descending_mode:
      qsort (T->tab, T->size, sizeof (bav_variable), &comp_variable_descending);
      break;
    case ba0_ascending_mode:
      qsort (T->tab, T->size, sizeof (bav_variable), &comp_variable_ascending);
      break;
    }
}

/*
 * Used in order to create an ordering. The above function cannot be used yet.
 */

static int
compare_just_created_variable (
    const void *x,
    const void *y)
{
  bav_variable v = *(bav_variable *) x, w = *(bav_variable *) y;
  bav_ordering O;
  bav_Inumber num_blk_v, num_blk_w;
  ba0_int_p num_in_blk_v, num_in_blk_w;
  ba0_int_p i;
  bool v_gt_w = false, found;

  if (v == w)
    return 0;

  O = bav_R_ordering ();

  found = false;
  i = 0;
  while (!found && i < O->varmax.size)
    {
      found = O->varmax.tab[i] == v || O->varmax.tab[i] == w;
      if (!found)
        i++;
    }
  if (found)
    {
      v_gt_w = O->varmax.tab[i] == v;
      return v_gt_w ? 1 : -1;
    }

  switch (v->root->type)
    {
    case bav_operator_symbol:
      switch (w->root->type)
        {
        case bav_operator_symbol:
          v_gt_w = O->operator_block.subr->inf (w, v, 0, 0, &O->ders);
          break;
        case bav_independent_symbol:
        case bav_dependent_symbol:
        case bav_temporary_symbol:
          v_gt_w = true;
        }
      break;
    case bav_dependent_symbol:
      switch (w->root->type)
        {
        case bav_operator_symbol:
          v_gt_w = false;
          break;
        case bav_dependent_symbol:
          num_blk_v = bav_R_symbol_block_number (v->root, &num_in_blk_v);
          num_blk_w = bav_R_symbol_block_number (w->root, &num_in_blk_w);
          if (num_blk_v < num_blk_w)
            v_gt_w = true;
          else if (num_blk_v > num_blk_w)
            v_gt_w = false;
          else
            v_gt_w = O->blocks.tab[num_blk_v]->subr->inf
                (w, v, num_in_blk_w, num_in_blk_v, &O->ders);
          break;
        case bav_independent_symbol:
        case bav_temporary_symbol:
          v_gt_w = true;
        }
      break;
    case bav_independent_symbol:
      switch (w->root->type)
        {
        case bav_operator_symbol:
        case bav_dependent_symbol:
          v_gt_w = false;
          break;
        case bav_independent_symbol:
          found = false;
          i = 0;
          while (!found && i < O->ders.size)
            {
              found = O->ders.tab[i] == v->root || O->ders.tab[i] == w->root;
              if (!found)
                i++;
            }
          if (i == O->ders.size)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          v_gt_w = O->ders.tab[i] == v->root;
          break;
        case bav_temporary_symbol:
          v_gt_w = true;
        }
      break;
    case bav_temporary_symbol:
      switch (w->root->type)
        {
        case bav_operator_symbol:
        case bav_dependent_symbol:
        case bav_independent_symbol:
          v_gt_w = false;
          break;
        case bav_temporary_symbol:
          v_gt_w = v->root->ident < w->root->ident;
          break;
        }
    }
  return v_gt_w ? 1 : -1;
}

static int
bav_compare_just_created_variable (
    const void *x,
    const void *y)
{
#if defined (BA0_HEAVY_DEBUG)
  int a, b;
  a = compare_just_created_variable (x, y);
  b = compare_just_created_variable (y, x);
  if (a * b != -1)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  return a;
#else
  return compare_just_created_variable (x, y);
#endif
}

/*
 * texinfo: bav_sort_tableof_just_created_variable
 * Sort @var{T} by increasing order w.r.t the current ordering.
 * This low level function is used when variable numbers are not yet available.
 */

BAV_DLL void
bav_sort_tableof_just_created_variable (
    bav_tableof_variable T)
{
  qsort (T->tab, T->size, sizeof (bav_variable),
      &bav_compare_just_created_variable);
}

/*
 * texinfo: bav_independent_variables
 * Assign to @var{T} all the derivations a.k.a. independent variables.
 */

BAV_DLL void
bav_independent_variables (
    bav_tableof_variable T)
{
  ba0_int_p i;

  ba0_reset_table ((ba0_table) T);
  ba0_realloc_table ((ba0_table) T, bav_global.R.ders.size);
  for (i = 0; i < bav_global.R.ders.size; i++)
    T->tab[T->size++] = bav_R_derivation_index_to_derivation (i);
}

BAV_DLL ba0_mint_hp
bav_random_eval_variable_to_mint_hp (
    bav_variable v)
{
  bav_variable t;
  ba0_int_p clef, k, i;

  clef = (ba0_int_p) (void *) v->root / sizeof (struct bav_symbol);
  if (v->root->type == bav_dependent_symbol ||
      v->root->type == bav_operator_symbol)
    {
      for (i = 0; i < v->order.size; i++)
        {
          t = bav_R_derivation_index_to_derivation (i);
          k = v->order.tab[i] * (ba0_int_p) (void *) t /
              sizeof (struct bav_variable);
          clef += k;
        }
    }
  return (ba0_mint_hp) (clef % (unsigned ba0_int_p) ba0_mint_hp_module);
}

/*
 * texinfo: bav_switch_ring_variable
 * Return the variable of @var{R} which has the same index in 
 * @code{R->vars} as @var{v}. 
 * This low level function should be used in conjunction with
 * @code{bav_set_differential_ring}: if @var{R} is a ring obtained by
 * application of @code{bav_set_differential_ring} to the ring @var{v} 
 * refers to, then this function returns the element of @var{R} 
 * which corresponds to @var{v}.
 */

BAV_DLL bav_variable
bav_switch_ring_variable (
    bav_variable v,
    bav_differential_ring R)
{
  return R->vars.tab[v->index];
}
