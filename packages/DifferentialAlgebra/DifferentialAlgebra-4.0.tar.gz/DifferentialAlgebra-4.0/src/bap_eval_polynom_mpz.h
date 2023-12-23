#ifndef BAP_EVAL_POLYNOM_mpz_H
#   define BAP_EVAL_POLYNOM_mpz_H 1

#   include "bap_polynom_mpz.h"

BEGIN_C_DECLS

#   define BAD_FLAG_mpz
#   if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpzm) || defined (BAD_FLAG_mpq)

extern BAP_DLL void bap_set_point_polynom_mpz (
    struct ba0_point *,
    struct bap_polynom_mpz *,
    bool);

extern BAP_DLL void bap_eval_polynom_numeric_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *,
    ba0_mpz_t);

extern BAP_DLL void bap_eval_polynom_polynom_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *,
    struct bap_polynom_mpz *);
#   endif

#   if defined (BAD_FLAG_mpz) || defined (BAD_FLAG_mpzm)
extern BAP_DLL void bap_eval_polynom_value_int_p_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_value_int_p *);

extern BAP_DLL void bap_eval_polynom_point_int_p_mpz (
    ba0_mpz_t *,
    struct bap_polynom_mpz *,
    struct bav_point_int_p *);

extern BAP_DLL void bap_evalcoeff_polynom_point_int_p_mpz (
    struct bap_polynom_mpz *,
    struct bap_polynom_mpz *,
    struct bav_point_int_p *);
#   endif
#   undef  BAD_FLAG_mpz

END_C_DECLS
#endif /* !BAP_EVAL_POLYNOM_mpz_H */
