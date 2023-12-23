#if ! defined (BAZ_EVAL_POLYSPEC_MPZ_H)
#   define BAZ_EVAL_POLYSPEC_MPZ_H 1

#   include "baz_common.h"

BEGIN_C_DECLS

extern BAZ_DLL void baz_eval_polynom_point_interval_mpq_mpz (
    struct ba0_interval_mpq *,
    struct bap_polynom_mpz *,
    struct bav_point_interval_mpq *);

END_C_DECLS
#endif /* !BAZ_EVAL_POLYSPEC_MPZ_H */
