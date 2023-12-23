#include "bav_symbol.h"
#include "bav_variable.h"
#include "bav_subranking.h"

/*
   There is one function per subranking.
   Each function returns true if v < w w.r.t. the subranking.
   It is assumed that v and w belong to the same block.
   nv is the index of v in the block.
   nw is the index of w in the block.
   ders is the table of the derivations (the order matters).
*/

static bool
inf_grlexA (
    bav_variable v,
    bav_variable w,
    ba0_int_p nv,
    ba0_int_p nw,
    bav_tableof_symbol ders)
{
  bav_Iorder v_order, w_order;
  ba0_int_p i, d;

  v_order = bav_total_order_variable (v);
  w_order = bav_total_order_variable (w);

  if (v_order < w_order)
    return true;
  else if (v_order > w_order)
    return false;

  if (nv > nw)
    return true;
  else if (nv < nw)
    return false;

  for (i = 0; i < ders->size; i++)
    {
      d = ders->tab[i]->derivation_index;
      if (v->order.tab[d] < w->order.tab[d])
        return true;
      else if (v->order.tab[d] > w->order.tab[d])
        return false;
    }

  return false;
}

static bool
inf_grlexB (
    bav_variable v,
    bav_variable w,
    ba0_int_p nv,
    ba0_int_p nw,
    bav_tableof_symbol ders)
{
  bav_Iorder v_order, w_order;
  ba0_int_p i, d;

  v_order = bav_total_order_variable (v);
  w_order = bav_total_order_variable (w);

  if (v_order < w_order)
    return true;
  else if (v_order > w_order)
    return false;

  for (i = 0; i < ders->size; i++)
    {
      d = ders->tab[i]->derivation_index;
      if (v->order.tab[d] < w->order.tab[d])
        return true;
      else if (v->order.tab[d] > w->order.tab[d])
        return false;
    }

  if (nv > nw)
    return true;
  else if (nv < nw)
    return false;

  return false;
}

static bool
inf_degrevlexA (
    bav_variable v,
    bav_variable w,
    ba0_int_p nv,
    ba0_int_p nw,
    bav_tableof_symbol ders)
{
  bav_Iorder v_order, w_order;
  ba0_int_p i, d;

  v_order = bav_total_order_variable (v);
  w_order = bav_total_order_variable (w);

  if (v_order < w_order)
    return true;
  else if (v_order > w_order)
    return false;

  if (nv > nw)
    return true;
  else if (nv < nw)
    return false;

  for (i = ders->size - 1; i >= 0; i--)
    {
      d = ders->tab[i]->derivation_index;
      if (v->order.tab[d] > w->order.tab[d])
        return true;
      else if (v->order.tab[d] < w->order.tab[d])
        return false;
    }

  return false;
}

static bool
inf_degrevlexB (
    bav_variable v,
    bav_variable w,
    ba0_int_p nv,
    ba0_int_p nw,
    bav_tableof_symbol ders)
{
  bav_Iorder v_order, w_order;
  ba0_int_p i, d;

  v_order = bav_total_order_variable (v);
  w_order = bav_total_order_variable (w);

  if (v_order < w_order)
    return true;
  else if (v_order > w_order)
    return false;

  for (i = ders->size - 1; i >= 0; i--)
    {
      d = ders->tab[i]->derivation_index;
      if (v->order.tab[d] > w->order.tab[d])
        return true;
      else if (v->order.tab[d] < w->order.tab[d])
        return false;
    }

  if (nv > nw)
    return true;
  else if (nv < nw)
    return false;

  return false;
}

static bool
inf_lex (
    bav_variable v,
    bav_variable w,
    ba0_int_p nv,
    ba0_int_p nw,
    bav_tableof_symbol ders)
{
  ba0_int_p i, d;

  for (i = 0; i < ders->size; i++)
    {
      d = ders->tab[i]->derivation_index;
      if (v->order.tab[d] < w->order.tab[d])
        return true;
      else if (v->order.tab[d] > w->order.tab[d])
        return false;
    }

  if (nv > nw)
    return true;
  else if (nv < nw)
    return false;

  return false;
}

/*
 * Readonly data structure.
 * Read also in bav_block.
 */

static struct bav_subranking bav_subranking_table[] = {
  {"grlexA", inf_grlexA},
  {"grlexB", inf_grlexB},
  {"degrevlexA", inf_degrevlexA},
  {"degrevlexB", inf_degrevlexB},
  {"lex", inf_lex}
};

#define BAV_NB_SUBRANKINGS	\
	(sizeof (bav_subranking_table) / sizeof (struct bav_subranking))

/*
 * texinfo: bav_is_subranking
 * Return @code{true} if @var{ident} is the identifier of a subranking.
 * If so, @var{subranking} is assigned the corresponding
 * value, read from a static readonly array.
 */

BAV_DLL bool
bav_is_subranking (
    char *ident,
    struct bav_subranking **subranking)
{
  ba0_int_p i;

  for (i = 0; i < (ba0_int_p) BAV_NB_SUBRANKINGS; i++)
    {
      if (ba0_strcasecmp (ident, bav_subranking_table[i].ident) == 0)
        {
          *subranking = &bav_subranking_table[i];
          return true;
        }
    }
  return false;
}
