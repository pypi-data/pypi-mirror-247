#include "bav_differential_ring.h"
#include "bav_global.h"

/*
 * texinfo: bav_init_differential_ring
 * Initialize @var{R} to the empty differential ring.
 */

BAV_DLL void
bav_init_differential_ring (
    bav_differential_ring R)
{
  R->empty = true;
  ba0_init_table ((ba0_table) & R->strs);
  ba0_init_table ((ba0_table) & R->syms);
  ba0_init_table ((ba0_table) & R->ders);
  ba0_init_table ((ba0_table) & R->deps);
  ba0_init_table ((ba0_table) & R->tmps);
  ba0_init_table ((ba0_table) & R->tmps_in_use);
  ba0_init_table ((ba0_table) & R->vars);
  R->opra = BAV_NOT_AN_OPINDEX;
  ba0_init_table ((ba0_table) & R->ords);
  ba0_init_table ((ba0_table) & R->ord_stack);
}

/*
 * texinfo: bav_new_differential_ring
 * Allocate a new differential ring in the process heap and initialize it.
 */

BAV_DLL bav_differential_ring
bav_new_differential_ring (
    void)
{
  bav_differential_ring R = ba0_alloc (sizeof (struct bav_differential_ring));
  bav_init_differential_ring (R);
  return R;
}

/* texinfo: bav_sizeof_differential_ring
 * Return the overall size of @var{R}: the one which is needed by
 * @code{bav_set_differential_ring} to perform a copy of @var{R} (including the
 * size of the structure itself).
 */

BAV_DLL unsigned ba0_int_p
bav_sizeof_differential_ring (
    bav_differential_ring R)
{
  bav_ordering o;
  unsigned ba0_int_p s;
  ba0_int_p i, j;

  s = ba0_allocated_size (sizeof (struct bav_differential_ring));
/*
 * strs
 */
  s += ba0_allocated_size (R->strs.size * sizeof (char *));
  for (i = 0; i < R->strs.size; i++)
    s += ba0_allocated_size (strlen (R->strs.tab[i]) + 1);
/*
 * syms
 */
  s += ba0_allocated_size (R->syms.size * sizeof (bav_symbol));
  s += R->syms.size * ba0_allocated_size (sizeof (struct bav_symbol));
/*
 * vars
 */
  s += ba0_allocated_size (R->vars.size * sizeof (bav_variable));
  s += R->vars.size *
      (ba0_allocated_size (sizeof (struct bav_variable)) +
      ba0_allocated_size (R->ords.size * sizeof (bav_Inumber)) +
      ba0_allocated_size (R->ders.size * sizeof (bav_Iorder)) +
      ba0_allocated_size (R->ders.size * sizeof (struct bav_variable)));
/*
 * ders, deps, tmps, tmps_in_use
 */
  s += ba0_allocated_size (R->ders.size * sizeof (ba0_int_p));
  s += ba0_allocated_size (R->deps.size * sizeof (ba0_int_p));
  s += ba0_allocated_size (R->tmps.size * sizeof (ba0_int_p));
  s += ba0_allocated_size (R->tmps_in_use.size * sizeof (ba0_int_p));
/*
 * ords
 */
  s += ba0_allocated_size (R->ords.size * sizeof (bav_ordering));
  s += R->ords.size * ba0_allocated_size (sizeof (struct bav_ordering));
  for (i = 0; i < R->ords.size; i++)
    {
      o = R->ords.tab[i];
      s += ba0_allocated_size (o->ders.size * sizeof (bav_symbol));
      s += ba0_allocated_size (o->blocks.size * sizeof (bav_block));
      for (j = 0; j < o->blocks.size; j++)
        {
          s += ba0_allocated_size (sizeof (struct bav_block));
          s += ba0_allocated_size
              (o->blocks.tab[j]->indices.size * sizeof (ba0_int_p));
          s += ba0_allocated_size
              (o->blocks.tab[j]->strs.size * sizeof (char *));
        }
      if (R->opra != BAV_NOT_AN_OPINDEX)
        {
          s += ba0_allocated_size (sizeof (ba0_int_p));
          s += ba0_allocated_size (sizeof (char *));
        }
      s += ba0_allocated_size (o->varmax.size * sizeof (bav_variable));
    }
/*
 * ord_stack
 */
  s += ba0_allocated_size (R->ord_stack.size * sizeof (bav_Iordering));
  return s;
}

/*
 * texinfo: bav_set_differential_ring
 * Copy @var{S} into @var{R}.
 * This function is very special since all strings, symbols and variables
 * are copied in the current stack.
 */

BAV_DLL void
bav_set_differential_ring (
    bav_differential_ring R,
    bav_differential_ring S)
{
  bav_ordering o, p;
  bav_variable v, w;
  ba0_int_p i, j, k, l;
/*
 * Copy the bool
 */
  R->empty = S->empty;
/*
 * Now, copy the strings and the symbols
 */
/* fprintf (stderr, "strs %d, %d\n", R->strs.size, S->strs.size); */
/* fprintf (stderr, "syms %d, %d\n", R->syms.size, S->syms.size); */

  ba0_realloc_table ((ba0_table) & R->strs, S->strs.size);
  ba0_realloc2_table ((ba0_table) & R->syms, S->syms.size,
      (ba0_new_function *) & bav_new_symbol);
  for (i = 0; i < S->syms.size; i++)
    {
      memcpy (R->syms.tab[i], S->syms.tab[i], sizeof (struct bav_symbol));
      R->strs.tab[i] = ba0_strdup (S->syms.tab[i]->ident);
      R->syms.tab[i]->ident = R->strs.tab[i];
      R->strs.size += 1;
      R->syms.size += 1;
    }
/*
 * Now, copy the variables
 */
/* fprintf (stderr, "vars %d, %d\n", R->vars.size, S->vars.size); */
  ba0_realloc2_table ((ba0_table) & R->vars, S->vars.size,
      (ba0_new_function *) & bav_new_variable);
  for (i = 0; i < S->vars.size; i++)
    {
      v = R->vars.tab[i];
      w = S->vars.tab[i];
      v->root = R->syms.tab[w->root->index];
      v->hack = w->hack;
      v->index = w->index;
      if (v->index != i)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);
      if (w->number.size != S->ords.size)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);
      if (w->order.size != w->order.alloc)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);
      if (w->derivative.size != w->derivative.alloc)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);
      ba0_set_table ((ba0_table) & v->number, (ba0_table) & w->number);
      ba0_set_table ((ba0_table) & v->order, (ba0_table) & w->order);
      ba0_realloc_table ((ba0_table) & v->derivative, w->derivative.size);
      for (j = 0; j < w->derivative.size; j++)
        {
          if (w->derivative.tab[j] != BAV_NOT_A_VARIABLE)
            v->derivative.tab[j] = R->vars.tab[w->derivative.tab[j]->index];
          else
            v->derivative.tab[j] = BAV_NOT_A_VARIABLE;
          v->derivative.size += 1;
        }
      R->vars.size += 1;
    }
/*
 * Now, copy the easy arrays
 */
/* fprintf (stderr, "ders %d, %d\n", R->ders.size, S->ders.size); */
  ba0_set_table ((ba0_table) & R->ders, (ba0_table) & S->ders);
  ba0_set_table ((ba0_table) & R->deps, (ba0_table) & S->deps);
  ba0_set_table ((ba0_table) & R->tmps, (ba0_table) & S->tmps);
  ba0_set_table ((ba0_table) & R->tmps_in_use, (ba0_table) & S->tmps_in_use);
  R->opra = S->opra;

/* fprintf (stderr, "ord_stack %d, %d\n", R->ord_stack.size, S->ord_stack.size); */
  ba0_set_table ((ba0_table) & R->ord_stack, (ba0_table) & S->ord_stack);
/*
 * Now copy the array of orderings
 */
/* fprintf (stderr, "ords %d, %d\n", R->ords.size, S->ords.size); */
  ba0_realloc2_table ((ba0_table) & R->ords, S->ords.size,
      (ba0_new_function *) & bav_new_ordering);
  for (i = 0; i < S->ords.size; i++)
    {
      o = R->ords.tab[i];
      p = S->ords.tab[i];
/* fprintf (stderr, "ords ders %d\n", p->ders.size); */
      ba0_realloc_table ((ba0_table) & o->ders, p->ders.size);
      for (j = 0; j < p->ders.size; j++)
        {
          o->ders.tab[j] = R->syms.tab[p->ders.tab[j]->index];
          o->ders.size += 1;
        }
/* fprintf (stderr, "ords blocks %d\n", p->blocks.size); */
      ba0_realloc2_table ((ba0_table) & o->blocks, p->blocks.size,
          (ba0_new_function *) & bav_new_block);
      for (j = 0; j < p->blocks.size; j++)
        {
          o->blocks.tab[j]->subr = p->blocks.tab[j]->subr;
          if (p->blocks.tab[j]->indices.size != p->blocks.tab[j]->strs.size)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          ba0_realloc_table ((ba0_table) & o->blocks.tab[j]->indices,
              p->blocks.tab[j]->indices.size);
          ba0_realloc_table ((ba0_table) & o->blocks.tab[j]->strs,
              p->blocks.tab[j]->strs.size);
          for (k = 0; k < p->blocks.tab[j]->indices.size; k++)
            {
              l = p->blocks.tab[j]->indices.tab[k];
              o->blocks.tab[j]->indices.tab[k] = l;
              o->blocks.tab[j]->strs.tab[k] = R->syms.tab[l]->ident;
              o->blocks.tab[j]->indices.size += 1;
              o->blocks.tab[j]->strs.size += 1;
            }
          o->blocks.size += 1;
        }
/* fprintf (stderr, "ords operator_block %d\n", R->opra); */
      if (R->opra != BAV_NOT_AN_OPINDEX)
        {
          o->operator_block.subr = p->operator_block.subr;
          if (p->operator_block.strs.size != 1 ||
              p->operator_block.indices.size != 1)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          ba0_realloc_table ((ba0_table) & o->operator_block.indices, 1);
          ba0_realloc_table ((ba0_table) & o->operator_block.strs, 1);
          o->operator_block.indices.tab[0] = R->opra;
          o->operator_block.strs.tab[0] = R->syms.tab[R->opra]->ident;
          o->operator_block.indices.size = 1;
          o->operator_block.strs.size = 1;
        }
/* fprintf (stderr, "ords varmax %d\n", p->varmax.size); */
      ba0_realloc_table ((ba0_table) & o->varmax, p->varmax.size);
      for (j = 0; j < p->varmax.size; j++)
        {
          o->varmax.tab[j] = R->vars.tab[p->varmax.tab[j]->index];
          o->varmax.size += 1;
        }
      R->ords.size += 1;
    }
}

/*
 * texinfo: bav_R_init
 * Initialize the @code{bav_global.R} variable to the empty
 * differential ring.
 */

BAV_DLL void
bav_R_init (
    void)
{
  bav_init_differential_ring (&bav_global.R);
}

/*
 * texinfo: bav_R_is_empty
 * Return @code{true} if @code{bav_global.R} is empty i.e. if
 * no ordering has yet been defined.
 */

BAV_DLL bool
bav_R_is_empty (
    void)
{
  return bav_global.R.empty;
}

/*
   This function is called by bav_R_create.
   A symbol is identified by a string.
   The strings are stored in bav_global.R.strs.
   nbders = the number of derivations.
*/

static void
bav_R_create_symbol (
    char *string,
    enum bav_typeof_symbol type,
    ba0_int_p nbders)
{
  bav_variable v;
  bav_symbol y;
  ba0_int_p j;

/*
   Symbols must be pairwise different thus string must not be equal to
   an already defined string.
*/
  for (j = 0; j < bav_global.R.strs.size; j++)
    if (strcmp (string, bav_global.R.strs.tab[j]) == 0)
      BA0_RAISE_EXCEPTION (BAV_ERRBOR);

  if (bav_global.R.strs.size == bav_global.R.strs.alloc)
    ba0_realloc2_table
        ((ba0_table) & bav_global.R.strs,
        2 * bav_global.R.strs.alloc + 1,
        (ba0_new_function *) & ba0_not_a_string);
  bav_global.R.strs.tab[bav_global.R.strs.size] =
      (char *) ba0_alloc (strlen (string) + 1);
  strcpy (bav_global.R.strs.tab[bav_global.R.strs.size++], string);
/*
   One does not take care not to increment the size fields before
   creations are completed for any raised exception is caught in
   bav_R_create and undoes everything.
*/
  if (bav_global.R.syms.size == bav_global.R.syms.alloc)
    ba0_realloc2_table
        ((ba0_table) & bav_global.R.syms,
        2 * bav_global.R.syms.alloc + 1, (ba0_new_function *) & bav_new_symbol);
  if (bav_global.R.vars.size == bav_global.R.vars.alloc)
    ba0_realloc2_table
        ((ba0_table) & bav_global.R.vars,
        2 * bav_global.R.vars.alloc + 1,
        (ba0_new_function *) & bav_new_variable);
  y = bav_global.R.syms.tab[bav_global.R.syms.size++];
  v = bav_global.R.vars.tab[bav_global.R.vars.size++];

  y->ident = bav_global.R.strs.tab[bav_global.R.strs.size - 1];
  y->type = type;
  y->index = bav_global.R.syms.size - 1;
  y->derivation_index = -1;

  switch (type)
    {
    case bav_independent_symbol:
      if (bav_global.R.ders.size == bav_global.R.ders.alloc)
        {
          if (bav_global.R.ders.size == nbders)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          ba0_realloc_table ((ba0_table) & bav_global.R.ders, nbders);
        }
      y->derivation_index = bav_global.R.ders.size;
      bav_global.R.ders.tab[bav_global.R.ders.size++] =
          bav_global.R.vars.size - 1;
      break;
    case bav_dependent_symbol:
      if (bav_global.R.deps.size == bav_global.R.deps.alloc)
        ba0_realloc_table
            ((ba0_table) & bav_global.R.deps, 2 * bav_global.R.deps.alloc + 1);
      bav_global.R.deps.tab[bav_global.R.deps.size++] =
          bav_global.R.vars.size - 1;
      break;
    case bav_temporary_symbol:
      if (bav_global.R.tmps.size == bav_global.R.tmps.alloc)
        ba0_realloc_table
            ((ba0_table) & bav_global.R.tmps, 2 * bav_global.R.tmps.alloc + 1);
      if (bav_global.R.tmps_in_use.size == bav_global.R.tmps_in_use.alloc)
        ba0_realloc_table ((ba0_table) & bav_global.R.tmps_in_use,
            2 * bav_global.R.tmps_in_use.alloc + 1);
      bav_global.R.tmps.tab[bav_global.R.tmps.size++] =
          bav_global.R.vars.size - 1;
      bav_global.R.tmps_in_use.tab[bav_global.R.tmps_in_use.size++] = 1;
      break;
    case bav_operator_symbol:
      bav_global.R.opra = bav_global.R.vars.size - 1;
    }

  v->root = y;
  v->index = bav_global.R.vars.size - 1;

  if (type == bav_dependent_symbol || type == bav_operator_symbol)
    {
      ba0_realloc_table ((ba0_table) & v->order, nbders);
      ba0_realloc2_table
          ((ba0_table) & v->derivative, nbders,
          (ba0_new_function *) & bav_not_a_variable);
      while (v->order.size < nbders)
        {
          v->order.tab[v->order.size++] = 0;
          v->derivative.tab[v->derivative.size++] = BAV_NOT_A_VARIABLE;
        }
    }
}

/*
 * texinfo: bav_R_ambiguous_symbols
 * Return @code{true} if one of the symbols present in
 * @code{bav_global.R.syms} is an indexed string
 * terminated by an @code{INDICES} made of a sequence of independent symbols.
 */

BAV_DLL bool
bav_R_ambiguous_symbols (
    void)
{
  bav_symbol y;
  struct ba0_mark M;
  ba0_indexed indexed;
  ba0_indices indices;
  ba0_int_p i;
  bool ambiguous, lder;

  ambiguous = false;
  ba0_record (&M);
  ba0_record_analex ();
  for (i = 0; i < bav_global.R.syms.size && !ambiguous; i++)
    {
      y = bav_global.R.syms.tab[i];
      ba0_set_analex_string (y->ident);
      ba0_get_token_analex ();
      indexed = ba0_scanf_indexed (0, &lder, &bav_is_a_derivation);
      if (lder)
        {
          indices = indexed->Tindic.tab[indexed->Tindic.size - 1];
          if (indices->Tindex.size > 0)
            ambiguous = true;
        }
    }
  ba0_restore_analex ();
  ba0_restore (&M);
  return ambiguous;
}

/*
 * texinfo: bav_R_create
 * Create the mathematical differential polynomial ring over which all
 * orderings will be defined. 
 * This function is called when parsing the first ordering in a 
 * sequence of calls to the library.
 * It creates all symbols.
 * Exception @code{BA0_ERRALG} is raised if @code{bav_global.R} is
 * not empty.
 * Exception @code{BAV_ERRBOR} is raised in case of a bad ordering.
 */

BAV_DLL void
bav_R_create (
    ba0_tableof_string D,
    bav_tableof_block B,
    bav_block O)
{
  struct ba0_mark M;
  ba0_int_p i, j;

  if (!bav_R_is_empty ())
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_push_stack (&ba0_global.stack.quiet);
  ba0_record (&M);
  ba0_pull_stack ();

  BA0_TRY
  {
    ba0_push_stack (&ba0_global.stack.quiet);
    for (i = 0; i < D->size; i++)
      bav_R_create_symbol (D->tab[i], bav_independent_symbol, D->size);
    for (i = 0; i < B->size; i++)
      for (j = 0; j < B->tab[i]->strs.size; j++)
        bav_R_create_symbol
            (B->tab[i]->strs.tab[j], bav_dependent_symbol, D->size);
    if (O->strs.size > 1)
      BA0_RAISE_EXCEPTION (BAV_ERRBOR);
    if (O->strs.size == 1)
      bav_R_create_symbol (O->strs.tab[0], bav_operator_symbol, D->size);
    else
      bav_global.R.opra = -1;
    ba0_pull_stack ();
    bav_global.R.empty = false;
  }
  BA0_CATCH
  {
    ba0_restore (&M);
    bav_R_init ();
    BA0_RE_RAISE_EXCEPTION;
  }
  BA0_ENDTRY;
}

static void
bav_compute_variable_numbers (
    bav_Iordering r)
{
  struct bav_tableof_variable T;
  struct ba0_mark M;
  ba0_int_p i;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_table ((ba0_table) & T);
  ba0_set_table ((ba0_table) & T, (ba0_table) & bav_global.R.vars);
  ba0_pull_stack ();

  bav_R_push_ordering (r);
  bav_sort_tableof_just_created_variable (&T);
  for (i = 0; i < T.size; i++)
    T.tab[i]->number.tab[r] = i;
  bav_R_pull_ordering ();

  ba0_restore (&M);
}

/*
 * texinfo: bav_R_new_temporary_variable
 * Return a new temporary variable.
 * Its symbol has type @code{bav_temporary_symbol}.
 */

BAV_DLL bav_variable
bav_R_new_temporary_variable (
    void)
{
  char string[16];
  bav_Iordering r;
  bav_variable v;
  ba0_int_p i;
  int k;
  bool found;

  i = 0;
  found = false;
  while (i < bav_global.R.tmps.size && !found)
    {
      found = bav_global.R.tmps_in_use.tab[i] == 0;
      if (!found)
        i++;
    }
  if (found)
    {
      v = bav_global.R.vars.tab[bav_global.R.tmps.tab[i]];
      bav_global.R.tmps_in_use.tab[i] = 1;
    }
  else
    {
      k = 0;
      do
        {
          sprintf (string, "%s[%d]",
              bav_initialized_global.variable.temp_string, k++);
          for (found = false, i = 0; i < bav_global.R.strs.size && !found; i++)
            found = strcmp (string, bav_global.R.strs.tab[i]) == 0;
        }
      while (found);
      ba0_push_stack (&ba0_global.stack.quiet);
      bav_R_create_symbol (string, bav_temporary_symbol,
          bav_global.R.ders.size);
      i = bav_global.R.vars.size - 1;
      ba0_realloc_table ((ba0_table) & bav_global.R.vars.tab[i]->number,
          bav_global.R.ords.alloc);
      bav_global.R.vars.tab[i]->number.size = bav_global.R.ords.size;
      for (r = 0; r < bav_global.R.ords.size; r++)
        bav_compute_variable_numbers (r);
      ba0_pull_stack ();
      v = bav_global.R.vars.tab[i];
    }
  return v;
}

/*
 * texinfo: bav_R_free_temporary_variable
 * Declare the temporary variable @var{v} as logically free.
 * This only implies that the next call to @code{bav_R_new_temporary_variable}
 * may return @var{v} instead of creating some new symbol.
 */

BAV_DLL void
bav_R_free_temporary_variable (
    bav_variable v)
{
  ba0_int_p i;
  bool found;

  if (v->root->type != bav_temporary_symbol)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  i = 0;
  found = false;
  while (i < bav_global.R.tmps.size && !found)
    {
      found = bav_global.R.tmps.tab[i] == v->index;
      if (!found)
        i++;
    }
  if (!found)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  bav_global.R.tmps_in_use.tab[i] = 0;
}

/*
 * texinfo: bav_R_new_ranking.
 * Create a new ranking, store it in @code{bav_R} and return the
 * index in @code{bav_global.R.ords} which identifies it.
 * This function is called by @code{bav_scanf_ordering}.
 */

BAV_DLL bav_Iordering
bav_R_new_ranking (
    ba0_tableof_string D,
    bav_tableof_block B,
    bav_block O)
{
  bav_ordering R;
  bav_symbol y;
  ba0_int_p i, j, nbdeps;
/*
   Checks consistency before starting any creation.
*/
  if (bav_R_is_empty ())
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (D->size != bav_global.R.ders.size)
    BA0_RAISE_EXCEPTION (BAV_ERRBOR);
  for (i = 0; i < D->size; i++)
    {
      y = bav_R_string_to_symbol (D->tab[i]);
      if (y == BAV_NOT_A_SYMBOL)
        {
          BA0_RAISE_EXCEPTION (BAV_ERRUSY);
        }
      if (y->type != bav_independent_symbol)
        BA0_RAISE_EXCEPTION (BAV_ERRBOR);
    }
  nbdeps = 0;
  for (i = 0; i < B->size; i++)
    nbdeps += B->tab[i]->strs.size;
  if (nbdeps != bav_global.R.deps.size)
    BA0_RAISE_EXCEPTION (BAV_ERRBOR);
  for (i = 0; i < B->size; i++)
    {
      for (j = 0; j < B->tab[i]->strs.size; j++)
        {
          y = bav_R_string_to_symbol (B->tab[i]->strs.tab[j]);
          if (y == BAV_NOT_A_SYMBOL)
            {
              BA0_RAISE_EXCEPTION (BAV_ERRUSY);
            }
          if (y->type != bav_dependent_symbol)
            BA0_RAISE_EXCEPTION (BAV_ERRBOR);
        }
    }
  if ((O->strs.size == 0 && bav_global.R.opra >= 0) ||
      (O->strs.size == 1 && bav_global.R.opra == BAV_NOT_AN_OPINDEX)
      || O->strs.size > 1)
    BA0_RAISE_EXCEPTION (BAV_ERRBOR);
  else if (O->strs.size == 1)
    {
      y = bav_R_string_to_symbol (O->strs.tab[0]);
      if (y == BAV_NOT_A_SYMBOL)
        {
          BA0_RAISE_EXCEPTION (BAV_ERRUSY);
        }
      if (y->type != bav_operator_symbol)
        BA0_RAISE_EXCEPTION (BAV_ERRBOR);
    }
/*
   Starts creating.
   If bav_global.R.ords is resized then so is v->number for any variable v.
*/
  ba0_push_stack (&ba0_global.stack.quiet);

  if (bav_global.R.ords.size == bav_global.R.ords.alloc)
    {
      ba0_realloc2_table
          ((ba0_table) & bav_global.R.ords,
          2 * bav_global.R.ords.alloc + 1,
          (ba0_new_function *) & bav_new_ordering);
      for (i = 0; i < bav_global.R.vars.size; i++)
        ba0_realloc_table
            ((ba0_table) & bav_global.R.vars.tab[i]->number,
            bav_global.R.ords.alloc);
    }
/*
   There should only be memory allocation failures. Anyway ...
*/
  BA0_TRY
  {
    R = bav_global.R.ords.tab[bav_global.R.ords.size++];
    bav_reset_ordering (R);

    for (i = 0; i < bav_global.R.vars.size; i++)
      bav_global.R.vars.tab[i]->number.size = bav_global.R.ords.size;

    ba0_realloc_table ((ba0_table) & R->ders, D->size);
    while (R->ders.size < D->size)
      {
        y = bav_R_string_to_symbol (D->tab[R->ders.size]);
        R->ders.tab[R->ders.size++] = y;
      }
/*
 * In blocks, the fields indices are set. The fields ident point to
 * the already existing strings.
 */
    ba0_realloc2_table
        ((ba0_table) & R->blocks, B->size,
        (ba0_new_function *) & bav_new_block);
    while (R->blocks.size < B->size)
      {
        i = R->blocks.size++;
        R->blocks.tab[i]->subr = B->tab[i]->subr;
        ba0_reset_table ((ba0_table) & R->blocks.tab[i]->strs);
        ba0_realloc_table
            ((ba0_table) & R->blocks.tab[i]->indices, B->tab[i]->strs.size);
        ba0_realloc_table ((ba0_table) & R->blocks.tab[i]->strs,
            B->tab[i]->strs.size);
        while (R->blocks.tab[i]->strs.size < B->tab[i]->strs.size)
          {
            j = R->blocks.tab[i]->strs.size;
            y = bav_R_string_to_symbol (B->tab[i]->strs.tab[j]);
            R->blocks.tab[i]->strs.tab[j] = y->ident;
            R->blocks.tab[i]->indices.tab[j] = y->index;
            R->blocks.tab[i]->strs.size += 1;
            R->blocks.tab[i]->indices.size += 1;
          }
      }
    if (O->strs.size == 1)
      {
        R->operator_block.subr = O->subr;
        ba0_realloc_table ((ba0_table) & R->operator_block.strs, 1);
        ba0_realloc_table ((ba0_table) & R->operator_block.indices, 1);
        y = bav_R_string_to_symbol (O->strs.tab[0]);
        R->operator_block.strs.tab[0] = y->ident;
        R->operator_block.indices.tab[0] = y->index;
        R->operator_block.strs.size = 1;
        R->operator_block.indices.size = 1;
      }

    bav_compute_variable_numbers (bav_global.R.ords.size - 1);
  }
  BA0_CATCH
  {
/*
   Annihilates the new ordering in the case of a failure.
*/
    bav_global.R.ords.size--;
    for (i = 0; i < bav_global.R.vars.size; i++)
      bav_global.R.vars.tab[i]->number.size--;

    BA0_RE_RAISE_EXCEPTION;
  }
  BA0_ENDTRY;
  ba0_pull_stack ();
  return bav_global.R.ords.size - 1;
}

/*
 * texinfo: bav_R_copy_ordering
 * Duplicate an already existing ordering and return its identifier.
 */

BAV_DLL bav_Iordering
bav_R_copy_ordering (
    bav_Iordering r)
{
  bav_variable v;
  ba0_int_p i;

  if (bav_R_is_empty () || r < 0 || r >= bav_global.R.ords.size)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_push_stack (&ba0_global.stack.quiet);
/*
   If bav_global.R.ords is resized then so is v->number for any variable v.
*/
  if (bav_global.R.ords.size == bav_global.R.ords.alloc)
    {
      ba0_realloc2_table
          ((ba0_table) & bav_global.R.ords,
          2 * bav_global.R.ords.alloc + 1,
          (ba0_new_function *) & bav_new_ordering);
      for (i = 0; i < bav_global.R.vars.size; i++)
        ba0_realloc_table
            ((ba0_table) & bav_global.R.vars.tab[i]->number,
            bav_global.R.ords.alloc);
    }

  bav_set_ordering (bav_global.R.ords.tab[bav_global.R.ords.size],
      bav_global.R.ords.tab[r]);

  bav_global.R.ords.size++;
  for (i = 0; i < bav_global.R.vars.size; i++)
    {
      v = bav_global.R.vars.tab[i];
      v->number.tab[v->number.size++] = v->number.tab[r];
    }

  ba0_pull_stack ();

  return bav_global.R.ords.size - 1;
}

/*
 * texinfo: bav_R_free_ordering
 * Free the ordering @var{r}.
 * This function requires that @var{r} is the index of the
 * last created ordering.
 */

BAV_DLL void
bav_R_free_ordering (
    bav_Iordering r)
{
  ba0_int_p i;

  if (bav_global.R.ords.size == 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  if (r == bav_global.R.ords.size - 1)
    {
      bav_global.R.ords.size--;
      for (i = 0; i < bav_global.R.vars.size; i++)
        bav_global.R.vars.tab[i]->number.size--;
    }
  else
    BA0_RAISE_EXCEPTION (BA0_ERRNYP);
}

/*
 * texinfo: bav_R_restore_ords_size
 * This function is automatically called when an exception is raised.
 * It frees all the orderings that were created after the exception
 * point was set. See @code{ba0_global.exception.extra_stack}.
 */

BAV_DLL void
bav_R_restore_ords_size (
    ba0_int_p size)
{
  if (size > bav_global.R.ords.size)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  while (bav_global.R.ords.size > size)
    bav_R_free_ordering (bav_global.R.ords.size - 1);
}

/*
 * Return @code{true} if @var{r} corresponds to an existing ordering.
 */

static bool
bav_exists_ordering (
    bav_Iordering r)
{
  return r >= 0 && r < bav_global.R.ords.size;
}

/*
 * texinfo: bav_R_swap_ordering
 * Swap the orderings @var{r} and @var{rbar}.
 * This function may be useful to free an ordering which is not the last
 * created one (see below).
 */

BAV_DLL void
bav_R_swap_ordering (
    bav_Iordering r,
    bav_Iordering rbar)
{
  bav_variable v;
  ba0_int_p i;

  if (!bav_exists_ordering (r) || !bav_exists_ordering (rbar))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  BA0_SWAP (bav_ordering, bav_global.R.ords.tab[r],
      bav_global.R.ords.tab[rbar]);
  for (i = 0; i < bav_global.R.vars.size; i++)
    {
      v = bav_global.R.vars.tab[i];
      BA0_SWAP (bav_Inumber, v->number.tab[r], v->number.tab[rbar]);
    }
}

/*
 * texinfo: bav_R_ordering
 * Return the current ordering.
 */

BAV_DLL bav_ordering
bav_R_ordering (
    void)
{
  return bav_global.R.ords.tab[bav_R_Iordering ()];
}

/*
 * texinfo: bav_R_push_ordering
 * Push @var{r} on the top of the ordering stack
 * @code{bav_global.R.ord_stack}.
 * The ordering @var{r} becomes the current ordering.
 */

BAV_DLL void
bav_R_push_ordering (
    bav_Iordering r)
{
  if (!bav_exists_ordering (r))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  if (bav_global.R.ord_stack.size == bav_global.R.ord_stack.alloc)
    {
      ba0_push_stack (&ba0_global.stack.quiet);
      ba0_realloc_table
          ((ba0_table) & bav_global.R.ord_stack,
          2 * bav_global.R.ord_stack.alloc + 1);
      ba0_pull_stack ();
    }
  bav_global.R.ord_stack.tab[bav_global.R.ord_stack.size++] = r;
}

/*
 * texinfo: bav_R_pull_ordering
 * Undo the last call to @code{bav_R_push_ordering}.
 */

BAV_DLL void
bav_R_pull_ordering (
    void)
{
  if (bav_global.R.ord_stack.size == 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  bav_global.R.ord_stack.size--;
}

/*
 * texinfo: bav_R_Iordering
 * Return the current ordering.
 */

BAV_DLL bav_Inumber
bav_R_Iordering (
    void)
{
  if (bav_global.R.ord_stack.size == 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  return bav_global.R.ord_stack.tab[bav_global.R.ord_stack.size - 1];
}

/*
 * texinfo: bav_R_derivative
 * Return the derivative of @var{v} w.r.t. @var{d}.
 * This low level function is called by @code{bav_diff_variable}.
 */

BAV_DLL bav_variable
bav_R_derivative (
    bav_variable v,
    bav_symbol d)
{
  bav_variable w = BAV_NOT_A_VARIABLE;
  bav_Iordering r;
  ba0_int_p i;

  if (bav_R_is_empty () || (v->root->type != bav_dependent_symbol &&
          v->root->type != bav_operator_symbol))
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
/*
   First check if it already exists
*/
  for (i = 0; i < bav_global.R.vars.size; i++)
    if (bav_global.R.vars.tab[i]->root->type != bav_independent_symbol
        && bav_is_d_derivative (bav_global.R.vars.tab[i], v, d))
      return bav_global.R.vars.tab[i];
/*
   Let's create it.
*/
  ba0_push_stack (&ba0_global.stack.quiet);

  if (bav_global.R.vars.size == bav_global.R.vars.alloc)
    ba0_realloc2_table
        ((ba0_table) & bav_global.R.vars,
        2 * bav_global.R.vars.alloc + 1,
        (ba0_new_function *) & bav_new_variable);

  BA0_TRY
  {
    w = bav_global.R.vars.tab[bav_global.R.vars.size++];

    w->root = v->root;
    w->index = bav_global.R.vars.size - 1;
    ba0_realloc_table ((ba0_table) & w->number, bav_global.R.ords.alloc);
    ba0_realloc_table ((ba0_table) & w->order, bav_global.R.ders.alloc);
    ba0_realloc2_table ((ba0_table) & w->derivative,
        bav_global.R.ders.alloc, (ba0_new_function *) & bav_not_a_variable);
/*
   Update field order.
*/
    for (i = 0; i < v->order.size; i++)
      w->order.tab[i] = v->order.tab[i];
    w->order.tab[d->derivation_index]++;
    w->order.size = v->order.size;
/*
   Update field derivative
*/
    for (i = 0; i < v->derivative.size; i++)
      {
        if (v->derivative.tab[i] == BAV_NOT_A_VARIABLE)
          w->derivative.tab[i] = BAV_NOT_A_VARIABLE;
        else
          {
            bav_variable x = v->derivative.tab[i];
            w->derivative.tab[i] = x->derivative.tab[d->derivation_index];
          }
      }
    w->derivative.size = v->derivative.size;

    w->number.size = bav_global.R.ords.size;
    for (r = 0; r < bav_global.R.ords.size; r++)
      bav_compute_variable_numbers (r);
  }
  BA0_CATCH
  {
    bav_global.R.vars.size--;
    BA0_RE_RAISE_EXCEPTION;
  }
  BA0_ENDTRY;
  ba0_pull_stack ();
  return w;
}

/*
 * texinfo: bav_R_symbol_to_variable
 * Convert the symbol @var{s} to a variable.
 */

BAV_DLL bav_variable
bav_R_symbol_to_variable (
    bav_symbol s)
{
  ba0_int_p i;
  bav_variable v = BAV_NOT_A_VARIABLE;

  switch (s->type)
    {
    case bav_independent_symbol:
      v = bav_global.R.vars.tab[bav_global.R.ders.tab[s->derivation_index]];
      break;
    case bav_operator_symbol:
      v = bav_global.R.vars.tab[bav_global.R.opra];
      break;
    case bav_dependent_symbol:
      v = BAV_NOT_A_VARIABLE;
      for (i = 0; v == BAV_NOT_A_VARIABLE && i < bav_global.R.deps.size; i++)
        if (bav_global.R.vars.tab[bav_global.R.deps.tab[i]]->root == s)
          v = bav_global.R.vars.tab[bav_global.R.deps.tab[i]];
      if (v == BAV_NOT_A_VARIABLE)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);
      break;
    case bav_temporary_symbol:
      v = BAV_NOT_A_VARIABLE;
      for (i = 0; v == BAV_NOT_A_VARIABLE && i < bav_global.R.tmps.size; i++)
        if (bav_global.R.vars.tab[bav_global.R.tmps.tab[i]]->root == s)
          v = bav_global.R.vars.tab[bav_global.R.tmps.tab[i]];
      if (v == BAV_NOT_A_VARIABLE)
        BA0_RAISE_EXCEPTION (BA0_ERRALG);
    }
  return v;
}

/*
 * texinfo: bav_R_string_to_symbol
 * Convert @var{s} to an existing symbol.
 * Return @code{BAV_NOT_A_SYMBOL} if @var{s} does not exist.
 */

BAV_DLL bav_symbol
bav_R_string_to_symbol (
    char *s)
{
  ba0_int_p i;

  for (i = 0; i < bav_global.R.syms.size; i++)
    if (strcmp (s, bav_global.R.syms.tab[i]->ident) == 0)
      return bav_global.R.syms.tab[i];
  return BAV_NOT_A_SYMBOL;
}

/*
 * texinfo: bav_R_string_to_derivation
 * Convert @var{s} to an existing independent symbol.
 * Return @code{BAV_NOT_A_SYMBOL} if @var{s} does not exist.
 */

BAV_DLL bav_symbol
bav_R_string_to_derivation (
    char *s)
{
  ba0_int_p i;
  bav_symbol d;

  for (i = 0; i < bav_global.R.ders.size; i++)
    {
      d = bav_global.R.syms.tab[bav_global.R.ders.tab[i]];
      if (strcmp (s, d->ident) == 0)
        return d;
    }
  return BAV_NOT_A_SYMBOL;
}

/*
 * texinfo: bav_R_string_to_variable
 * Convert @var{s} to a variable (made of existing symbols).
 * Return @code{BAV_NOT_A_VARIABLE} if one of the necessary symbols
 * does not exist.
 */

BAV_DLL bav_variable
bav_R_string_to_variable (
    char *s)
{
  bav_symbol y;

  y = bav_R_string_to_symbol (s);
  if (y == BAV_NOT_A_SYMBOL)
    return BAV_NOT_A_VARIABLE;
  return bav_R_symbol_to_variable (y);
}

/*
 * texinfo: bav_R_derivation_index_to_derivation
 * Return the variable corresponding to the derivation which has index @var{k}
 * in @code{bav_global.R.ders}.
 */

BAV_DLL bav_variable
bav_R_derivation_index_to_derivation (
    ba0_int_p k)
{
  if (k < 0 || k > bav_global.R.ders.size)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  return bav_global.R.vars.tab[bav_global.R.ders.tab[k]];
}

/*
 * texinfo: bav_R_symbol_block_number
 * Return the block number of the dependent symbol @var{s} in the
 * current ranking. If @var{n} is not the zero pointer, *@var{n}
 * is assigned the index of the symbol inside the block.
 * May raise exception @code{BA0_ERRALG}.
 */

BAV_DLL bav_Inumber
bav_R_symbol_block_number (
    bav_symbol s,
    ba0_int_p *n)
{
  ba0_int_p i, j;
  bav_ordering O;

  if (s->type == bav_independent_symbol || bav_global.R.ords.size == 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);
  if (s->type == bav_dependent_symbol)
    {
      O = bav_R_ordering ();
      for (i = 0; i < O->blocks.size; i++)
        for (j = 0; j < O->blocks.tab[i]->strs.size; j++)
          if (s->ident == O->blocks.tab[i]->strs.tab[j])
            {
              if (n != (ba0_int_p *) 0)
                *n = j;
              return i;
            }
      BA0_RAISE_EXCEPTION (BA0_ERRALG);
      return -1;
    }
  else
    return 0;
}

/*
 * texinfo: bav_R_variable_number
 * Return the number of @var{v} w.r.t. the current ordering.
 */

BAV_DLL bav_Iordering
bav_R_variable_number (
    bav_variable v)
{
  return v->number.tab[bav_R_Iordering ()];
}

/*
 * texinfo: bav_R_mark_variables
 * Assign @var{b} to the field @code{hack} of every variable.
 */

BAV_DLL void
bav_R_mark_variables (
    ba0_int_p b)
{
  ba0_int_p i;

  for (i = 0; i < bav_global.R.vars.size; i++)
    bav_global.R.vars.tab[i]->hack = b;
}

/*
 * texinfo: bav_R_marked_variables
 * Assign to @var{T} the set of all variables the @code{hack} field of
 * which has value @var{b}.
 */

BAV_DLL void
bav_R_marked_variables (
    bav_tableof_variable T,
    ba0_int_p b)
{
  ba0_int_p i, n;

  for (i = 0, n = 0; i < bav_global.R.vars.size; i++)
    if (bav_global.R.vars.tab[i]->hack == b)
      n++;
  ba0_reset_table ((ba0_table) T);
  ba0_realloc_table ((ba0_table) T, n);
  for (i = 0; i < bav_global.R.vars.size; i++)
    {
      if (bav_global.R.vars.tab[i]->hack == b)
        T->tab[T->size++] = bav_global.R.vars.tab[i];
    }
}

/*
 * texinfo: bav_R_set_maximal_variable
 * Change the current ordering in such a way that @var{v} becomes
 * the greatest variable (inserts @var{v} at the beginning of the
 * field @code{varmax} of the current ordering).
 * The ordering between other variables is left unchanged.
 */

BAV_DLL void
bav_R_set_maximal_variable (
    bav_variable v)
{
  ba0_int_p i;
  bav_Inumber *p, *q;
  bav_ordering O;

  O = bav_R_ordering ();
  ba0_push_stack (&ba0_global.stack.quiet);
  if (O->varmax.size == O->varmax.alloc)
    ba0_realloc2_table
        ((ba0_table) & O->varmax, 2 * O->varmax.alloc + 1,
        (ba0_new_function *) & bav_not_a_variable);
  ba0_pull_stack ();

  p = &v->number.tab[bav_R_Iordering ()];
  for (i = 0; i < bav_global.R.vars.size; i++)
    {
      q = &bav_global.R.vars.tab[i]->number.tab[bav_R_Iordering ()];
      if (*q > *p)
        (*q)--;
    }
  (*p) = bav_global.R.vars.size - 1;

  memmove (O->varmax.tab + 1, O->varmax.tab,
      O->varmax.size * sizeof (bav_variable));
  O->varmax.size++;
  O->varmax.tab[0] = v;
}
