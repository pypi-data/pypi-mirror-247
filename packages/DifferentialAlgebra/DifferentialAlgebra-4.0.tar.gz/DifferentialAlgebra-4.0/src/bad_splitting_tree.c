#include "bad_splitting_tree.h"

/*
 * texinfo: bad_init_splitting_edge
 * Initialize @var{E}a.
 */

BAD_DLL void
bad_init_splitting_edge (
    bad_splitting_edge E)
{
  E->src = 0;
  E->dst = 0;
  E->type = bad_any_edge;
}

/*
 * texinfo: bad_new_splitting_edge
 * Allocate a new edge, initialize it and return it.
 */

BAD_DLL bad_splitting_edge
bad_new_splitting_edge (
    void)
{
  bad_splitting_edge E;

  E = (bad_splitting_edge) ba0_alloc (sizeof (struct bad_splitting_edge));
  bad_init_splitting_edge (E);
  return E;
}

/*
 * texinfo: bad_set_splitting_edge
 * Assign @var{F} to @var{E}.
 */

BAD_DLL void
bad_set_splitting_edge (
    bad_splitting_edge E,
    bad_splitting_edge F)
{
  if (E != F)
    *E = *F;
}

/*
 * texinfo: bad_set_node_type_splitting_edge
 * Assign @var{src}, @var{dst} and @var{type} to the corresponding
 * fields of @var{E}.
 */

BAD_DLL void
bad_set_node_type_splitting_edge (
    bad_splitting_edge E,
    ba0_int_p src,
    ba0_int_p dst,
    enum bad_typeof_splitting_edge type)
{
  E->src = src;
  E->dst = dst;
  E->type = type;
}

/*
 * readonly data
 */

static struct
{
  enum bad_typeof_splitting_edge type;
  char *ident;
} bad_cases[] = { {bad_any_edge, "A"},
{bad_first_edge, "I"},
{bad_redzero_edge, "Z"},
{bad_factor_edge, "F"},
{bad_regularisation_edge, "R"},
{bad_inisep_edge, "S"},
{bad_euclid_edge, "E"},
{bad_reg_characteristic_edge, "C"}
};

/*
 * texinfo: bad_scanf_splitting_edge
 * The parsing function for splitting edges.
 * It is called by @code{ba0_scanf/%splitting_edge}.
 */

BAD_DLL void *
bad_scanf_splitting_edge (
    void *A)
{
  bad_splitting_edge E;
  unsigned ba0_int_p i;
  char buffer[BA0_BUFSIZE];
  bool found;

  if (A == (void *) 0)
    E = bad_new_splitting_edge ();
  else
    E = (bad_splitting_edge) A;

  ba0_scanf ("%s: %d -\\> %d", buffer, &E->src, &E->dst);

  found = false;
  i = 0;
  while (!found && i < sizeof (bad_cases) / sizeof (bad_cases[0]))
    {
      found = ba0_strcasecmp (buffer, bad_cases[i].ident) == 0;
      if (!found)
        i += 1;
    }

  if (found)
    E->type = bad_cases[i].type;
  else
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRSYN);

  return E;
}

/*
 * texinfo: bad_printf_splitting_edge
 * The printing function for splitting edges.
 * It is called by @code{ba0_printf/%splitting_edge}.
 */

BAD_DLL void
bad_printf_splitting_edge (
    void *A)
{
  bad_splitting_edge E = (bad_splitting_edge) A;
  unsigned ba0_int_p i;
  bool found;

  i = 0;
  found = false;
  while (!found && i < sizeof (bad_cases) / sizeof (bad_cases[0]))
    {
      found = E->type == bad_cases[i].type;
      if (!found)
        i += 1;
    }

  if (!found)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_printf ("%s: %d -\\> %d", bad_cases[i].ident, E->src, E->dst);
}

static char _struct_splitting_edge[] = "struct bad_splitting_edge";

BAD_DLL ba0_int_p
bad_garbage1_splitting_edge (
    void *A,
    enum ba0_garbage_code code)
{
  bad_splitting_edge E = (bad_splitting_edge) A;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info
        (E, sizeof (struct bad_splitting_edge), _struct_splitting_edge);
  return n;
}

BAD_DLL void *
bad_garbage2_splitting_edge (
    void *A,
    enum ba0_garbage_code code)
{
  bad_splitting_edge E;

  if (code == ba0_isolated)
    E = (bad_splitting_edge) ba0_new_addr_gc_info (A, _struct_splitting_edge);
  else
    E = (bad_splitting_edge) A;

  return E;
}

BAD_DLL void *
bad_copy_splitting_edge (
    void *A)
{
  bad_splitting_edge E;

  E = bad_new_splitting_edge ();
  bad_set_splitting_edge (E, (bad_splitting_edge) A);
  return E;
}

/****************************************************************************
 * SPLITTING TREE
 ****************************************************************************/

/*
 * texinfo: bad_init_splitting_tree
 * Initialize @var{T} to an inactive splitting tree.
 */

BAD_DLL void
bad_init_splitting_tree (
    bad_splitting_tree T)
{
  T->active = false;
  ba0_init_table ((ba0_table) & T->edges);
  T->node_number = 1;
}

/*
 * texinfo: bad_new_splitting_tree
 * Allocate a new splitting tree, initialize it and return it.
 */

BAD_DLL bad_splitting_tree
bad_new_splitting_tree (
    void)
{
  bad_splitting_tree T;

  T = (bad_splitting_tree) ba0_alloc (sizeof (struct bad_splitting_tree));
  bad_init_splitting_tree (T);
  return T;
}

/*
 * texinfo: bad_activate_splitting_tree
 * Activate @var{T}.
 */

BAD_DLL void
bad_activate_splitting_tree (
    struct bad_splitting_tree *T)
{
  T->active = true;
}

/*
 * texinfo: bad_is_active_splitting_tree
 * Return @code{true} if @var{T} is active else @code{false}.
 */

BAD_DLL bool
bad_is_active_splitting_tree (
    struct bad_splitting_tree *T)
{
  return T->active;
}

static void
bad_realloc_tableof_splitting_edge (
    bad_tableof_splitting_edge T,
    ba0_int_p n)
{
  ba0_realloc2_table ((ba0_table) T, n,
      (ba0_new_function *) & bad_new_splitting_edge);
}


static void
bad_set_tableof_splitting_edge (
    bad_tableof_splitting_edge T,
    bad_tableof_splitting_edge U)
{
  ba0_int_p i;

  if (T != U)
    {
      bad_realloc_tableof_splitting_edge (T, U->size);
      for (i = 0; i < U->size; i++)
        bad_set_splitting_edge (T->tab[i], U->tab[i]);
      T->size = U->size;
    }
}

/*
 * texinfo: bad_set_splitting_tree
 * Assign @var{U} to @var{T}.
 */

BAD_DLL void
bad_set_splitting_tree (
    bad_splitting_tree T,
    bad_splitting_tree U)
{
  if (T != U)
    {
      T->active = U->active;
      bad_set_tableof_splitting_edge (&T->edges, &U->edges);
      T->node_number = U->node_number;
    }
}

/*
 * texinfo: bad_next_node_splitting_tree
 * Increase by @math{1} the field @code{node_number} of @var{T}.
 */

BAD_DLL ba0_int_p
bad_next_node_splitting_tree (
    bad_splitting_tree T)
{
  return T->node_number++;
}

/*
 * texinfo: bad_append_edge_splitting_tree
 * Assign to @var{T} the splitting tree obtaining by appending the
 * edge (@var{src}, @var{dst}, @var{type}) to @var{U}.
 */

BAD_DLL void
bad_append_edge_splitting_tree (
    bad_splitting_tree T,
    bad_splitting_tree U,
    ba0_int_p src,
    ba0_int_p dst,
    enum bad_typeof_splitting_edge type)
{
  if (!T->active)
    return;

  if (U->edges.size >= T->edges.alloc)
    bad_realloc_tableof_splitting_edge (&T->edges, 2 * U->edges.size + 1);
  bad_set_splitting_tree (T, U);
  bad_set_node_type_splitting_edge
      (T->edges.tab[T->edges.size], src, dst, type);
  T->edges.size += 1;
}

/*
 * Assign to newnode the first successor of node (possibly node itself)
 * which has not exactly one child.
 * Assign to childhood the number of children.
 */

static void
node_analysis (
    struct ba0_tableof_int_p *between,
    ba0_int_p *numberof_children,
    ba0_int_p *newnode,
    bad_splitting_tree T,
    ba0_int_p node)
{
  ba0_int_p succ, cour, nb, i;

  ba0_reset_table ((ba0_table) between);
  succ = node;
  do
    {
      cour = succ;
      nb = 0;
      for (i = 0; i < T->edges.size; i++)
        {
          if (T->edges.tab[i]->src == cour)
            {
              succ = T->edges.tab[i]->dst;
              nb += 1;
            }
        }
      if (nb == 1)
        {
          ba0_realloc_table ((ba0_table) between, between->size + 1);
          between->tab[between->size] = cour;
          between->size += 1;
        }
    }
  while (nb == 1);
  *newnode = cour;
  *numberof_children = nb;
}

/*
 * texinfo: bad_dot_splitting_tree
 * Print @var{T} as a directed graph, following the syntax 
 * of @code{graphviz/dot}. Leaves displayed as squares correspond
 * to consistent terminal systems i.e. regular differential chains.
 */

BAD_DLL void
bad_dot_splitting_tree (
    bad_splitting_tree T)
{
  ba0_int_p *Q;
  ba0_int_p i, ancestor, child, N, deb, fin, numberof_children;
  struct ba0_tableof_int_p between;
  struct ba0_mark M;

  if (!T->active)
    return;

  ba0_record (&M);
  ba0_init_table ((ba0_table) & between);

  ba0_printf ("digraph G \\{\n");
  for (i = 0; i < T->edges.size; i++)
    {
      if (T->edges.tab[i]->type == bad_reg_characteristic_edge)
        ba0_printf ("\t%d [shape=box];\n", T->edges.tab[i]->dst);
    }
  N = T->node_number + 1;
  Q = ba0_alloc (N * sizeof (ba0_int_p));
  deb = 0;
  fin = 0;
  Q[fin] = 0;
  fin = (fin + 1) % N;
  while (deb != fin)
    {
      ancestor = Q[deb];
      deb = (deb + 1) % N;
      for (i = 0; i < T->edges.size; i++)
        {
          if (T->edges.tab[i]->src == ancestor)
            {
              node_analysis (&between, &numberof_children, &child, T,
                  T->edges.tab[i]->dst);
              if (between.size > 0)
                ba0_printf ("%d -\\> %d \\[label=\"%t[%d]\"\\];\n",
                    ancestor, child, &between);
              else
                ba0_printf ("%d -\\> %d;\n", ancestor, child);
              if (numberof_children > 0)
                {
                  Q[fin] = child;
                  fin = (fin + 1) % N;
                }
            }
        }
    }
  ba0_printf ("\\}\n");

  ba0_restore (&M);
}

/*
 * texinfo: bad_scanf_splitting_tree
 * The parsing function for splitting trees.
 * It is called by @code{ba0_scanf/%splitting_tree}.
 * The read splitting tree is active.
 */

BAD_DLL void *
bad_scanf_splitting_tree (
    void *A)
{
  bad_splitting_tree T;

  if (A == (void *) 0)
    T = bad_new_splitting_tree ();
  else
    T = (bad_splitting_tree) A;

  ba0_scanf ("<node = %d, edges = %t[%splitting_edge]>",
      &T->node_number, &T->edges);

  T->active = true;

  return T;
}

/*
 * texinfo: bad_printf_splitting_tree
 * The printing function for splitting trees.
 * It is called by @code{ba0_printf/%splitting_tree}.
 */

BAD_DLL void
bad_printf_splitting_tree (
    void *A)
{
  bad_splitting_tree T = (bad_splitting_tree) A;

  if (T->active)
    ba0_printf ("<node = %d, edges = %t[%splitting_edge]>",
        T->node_number, &T->edges);
  else
    ba0_printf ("inactive splitting tree");
}

static char _struct_splitting_tree[] = "struct bad_splitting_tree";

BAD_DLL ba0_int_p
bad_garbage1_splitting_tree (
    void *A,
    enum ba0_garbage_code code)
{
  bad_splitting_tree T = (bad_splitting_tree) A;
  ba0_int_p n = 0;

  if (code == ba0_isolated)
    n += ba0_new_gc_info
        (T, sizeof (struct bad_splitting_tree), _struct_splitting_tree);
  n += ba0_garbage1 ("%t[%splitting_edge]", &T->edges, ba0_embedded);
  return n;
}

BAD_DLL void *
bad_garbage2_splitting_tree (
    void *A,
    enum ba0_garbage_code code)
{
  bad_splitting_tree T;

  if (code == ba0_isolated)
    T = (bad_splitting_tree) ba0_new_addr_gc_info (A, _struct_splitting_tree);
  else
    T = (bad_splitting_tree) A;
  ba0_garbage2 ("%t[%splitting_edge]", &T->edges, ba0_embedded);
  return T;
}

BAD_DLL void *
bad_copy_splitting_tree (
    void *A)
{
  bad_splitting_tree T;

  T = bad_new_splitting_tree ();
  bad_set_splitting_tree (T, (bad_splitting_tree) A);
  return T;
}
