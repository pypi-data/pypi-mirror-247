#ifndef BAP_DIFF_POLYNOM_mint_hp_H
#   define BAP_DIFF_POLYNOM_mint_hp_H 1

#   include "bap_common.h"

BEGIN_C_DECLS

#   define BAD_FLAG_mint_hp
extern BAP_DLL bool bap_is_constant_polynom_mint_hp (
    struct bap_polynom_mint_hp *,
    struct bav_symbol *,
    struct bav_tableof_parameter *);

extern BAP_DLL bool bap_is_independent_polynom_mint_hp (
    struct bap_polynom_mint_hp *,
    struct bav_tableof_parameter *);

extern BAP_DLL void bap_diff_polynom_mint_hp (
    struct bap_polynom_mint_hp *,
    struct bap_polynom_mint_hp *,
    struct bav_symbol *,
    struct bav_tableof_variable *);

extern BAP_DLL void bap_diff2_polynom_mint_hp (
    struct bap_polynom_mint_hp *,
    struct bap_polynom_mint_hp *,
    struct bav_term *,
    struct bav_tableof_variable *);

extern BAP_DLL void bap_involved_derivations_polynom_mint_hp (
    struct bav_tableof_variable *,
    struct bap_polynom_mint_hp *);

extern BAP_DLL void bap_zero_derivatives_of_tableof_parameter_mint_hp (
    struct bap_tableof_polynom_mint_hp *,
    struct bav_tableof_parameter *);

#   undef  BAD_FLAG_mint_hp

END_C_DECLS
#endif /* !BAP_DIFF_POLYNOM_mint_hp_H */
