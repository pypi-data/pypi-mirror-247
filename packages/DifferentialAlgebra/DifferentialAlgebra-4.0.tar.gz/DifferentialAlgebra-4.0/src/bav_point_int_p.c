#include "bav_differential_ring.h"
#include "bav_point_int_p.h"

BAV_DLL int
bav_inv_comp_value_int_p (
    const void *x,
    const void *y)
{
  struct bav_value_int_p *r = *(struct bav_value_int_p **) x;
  struct bav_value_int_p *s = *(struct bav_value_int_p **) y;
  bav_Inumber n, m;

  if (r->var == s->var)
    return 0;

  n = bav_R_variable_number (r->var);
  m = bav_R_variable_number (s->var);

  return n < m ? 1 : -1;
}

/*
 * texinfo: bav_sort_point_int_p
 * Sort @var{T} by increasing addresses of the variables.
 */

BAV_DLL void
bav_sort_point_int_p (
    struct bav_point_int_p *T)
{
  qsort (T->tab, T->size, sizeof (struct bav_value_int_p *),
      &bav_inv_comp_value_int_p);
}
