#ifndef BAP_EVAL_POLYNOM_mpzm_H
#   define BAP_EVAL_POLYNOM_mpzm_H 1

#   include "bap_polynom_mpzm.h"

BEGIN_C_DECLS

#   define BAD_FLAG_mpzm
#   if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpzm) || defined (BAD_FLAG_mpq)

extern BAP_DLL void bap_set_point_polynom_mpzm (
    struct ba0_point *,
    struct bap_polynom_mpzm *,
    bool);

extern BAP_DLL void bap_eval_polynom_numeric_mpzm (
    struct bap_polynom_mpzm *,
    struct bap_polynom_mpzm *,
    struct bav_variable *,
    ba0_mpzm_t);

extern BAP_DLL void bap_eval_polynom_polynom_mpzm (
    struct bap_polynom_mpzm *,
    struct bap_polynom_mpzm *,
    struct bav_variable *,
    struct bap_polynom_mpzm *);
#   endif

#   if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpzm)
extern BAP_DLL void bap_eval_polynom_value_int_p_mpzm (
    struct bap_polynom_mpzm *,
    struct bap_polynom_mpzm *,
    struct bav_value_int_p *);

extern BAP_DLL void bap_eval_polynom_point_int_p_mpzm (
    ba0_mpzm_t *,
    struct bap_polynom_mpzm *,
    struct bav_point_int_p *);

extern BAP_DLL void bap_evalcoeff_polynom_point_int_p_mpzm (
    struct bap_polynom_mpzm *,
    struct bap_polynom_mpzm *,
    struct bav_point_int_p *);
#   endif
#   undef  BAD_FLAG_mpzm

END_C_DECLS
#endif /* !BAP_EVAL_POLYNOM_mpzm_H */
