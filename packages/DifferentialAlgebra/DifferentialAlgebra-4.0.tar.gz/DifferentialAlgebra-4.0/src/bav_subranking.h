#ifndef BAV_SUBRANKING_H
#   define BAV_SUBRANKING_H 1

#   include "bav_common.h"
#   include "bav_variable.h"


BEGIN_C_DECLS

/*
 * texinfo: bav_subranking
 * This data type implements a subranking.
 */

struct bav_subranking
{
// the identifier of the subranking (grlexA, degrevlexB, ...)
  char *ident;
// a comparison function (*inf) (v, w, nv, nw, ders)
// Return true if v < w w.r.t. the subranking
// nv and nw are the indices of v and w in their block
// ders is the table of the derivations
  bool (
      *inf) (
      struct bav_variable *,
      struct bav_variable *,
      ba0_int_p,
      ba0_int_p,
      struct bav_tableof_symbol *);
};

extern BAV_DLL bool bav_is_subranking (
    char *,
    struct bav_subranking **);

END_C_DECLS
#endif /* !BAV_SUBRANKING_H */
