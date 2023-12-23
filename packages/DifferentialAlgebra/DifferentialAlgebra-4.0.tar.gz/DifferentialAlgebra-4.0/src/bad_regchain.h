#ifndef BAD_REGCHAIN_H
#   define BAD_REGCHAIN_H 1

#   include "bad_common.h"
#   include "bad_attchain.h"

BEGIN_C_DECLS

struct bad_base_field;

/*
 * texinfo: bad_regchain
 * This data type implements regular chains.
 * Mathematically, a regular chain @math{A} defines an ideal which
 * is either @math{(A):I_A^\infty} in the nondifferential case, or
 * @math{[A]:H_A^\infty} in the differential case.
 */

struct bad_regchain
{
// the node number in splitting trees
  ba0_int_p number;
// the attributes of the regular chain
  struct bad_attchain attrib;
// the polynomial set A, sorted increasingly w.r.t. the chain ordering
  struct bap_tableof_polynom_mpz decision_system;
};

#   if defined (BA0_OLDDEF)
typedef struct bad_regchain *bad_regchain;
#   endif

struct bad_tableof_regchain
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bad_regchain **tab;
};

#   if defined (BA0_OLDDEF)
typedef struct bad_tableof_regchain *bad_tableof_regchain;
#   endif

extern BAD_DLL void bad_init_regchain (
    struct bad_regchain *);

extern BAD_DLL void bad_reset_regchain (
    struct bad_regchain *);

extern BAD_DLL struct bad_regchain *bad_new_regchain (
    void);

extern BAD_DLL void bad_realloc_regchain (
    struct bad_regchain *,
    ba0_int_p);

extern BAD_DLL void bad_set_regchain (
    struct bad_regchain *,
    struct bad_regchain *);

extern BAD_DLL ba0_int_p bad_product_of_leading_degrees_regchain (
    struct bad_regchain *);

extern BAD_DLL void
bad_remove_zero_derivatives_of_tableof_parameter_from_regchain (
    struct bad_regchain *,
    struct bad_regchain *,
    struct bav_tableof_parameter *);

extern BAD_DLL void bad_set_and_extend_regchain_tableof_polynom_mpz (
    struct bad_regchain *,
    struct bap_tableof_polynom_mpz *,
    struct bav_tableof_parameter *,
    struct ba0_tableof_string *,
    bool,
    bool);

extern BAD_DLL void bad_set_and_extend_regchain_tableof_ratfrac_mpz (
    struct bad_regchain *,
    struct baz_tableof_ratfrac *,
    struct bav_tableof_parameter *,
    struct ba0_tableof_string *,
    bool,
    bool);

extern BAD_DLL void bad_fast_primality_test_regchain (
    struct bad_regchain *);

extern BAD_DLL void bad_set_number_regchain (
    struct bad_regchain *,
    ba0_int_p);

extern BAD_DLL void bad_set_property_regchain (
    struct bad_regchain *,
    enum bad_property_attchain);

extern BAD_DLL void bad_set_properties_regchain (
    struct bad_regchain *,
    struct ba0_tableof_string *);

extern BAD_DLL void bad_set_properties_regchain (
    struct bad_regchain *,
    struct ba0_tableof_string *);

extern BAD_DLL bool bad_has_property_regchain (
    struct bad_regchain *,
    enum bad_property_attchain);

extern BAD_DLL bool bad_defines_a_differential_ideal_regchain (
    struct bad_regchain *);

extern BAD_DLL bool bad_defines_a_prime_ideal_regchain (
    struct bad_regchain *);

extern BAD_DLL void bad_inequations_regchain (
    struct bap_tableof_polynom_mpz *,
    struct bad_regchain *);

extern BAD_DLL void bad_sort_regchain (
    struct bad_regchain *,
    struct bad_regchain *);

extern BAD_DLL bav_Iordering bad_ordering_eliminating_leaders_of_regchain (
    struct bad_regchain *);

extern BAD_DLL bool bad_is_rank_of_regchain (
    struct bav_rank *,
    struct bad_regchain *,
    ba0_int_p *);

extern BAD_DLL bool bad_is_leader_of_regchain (
    struct bav_variable *,
    struct bad_regchain *,
    ba0_int_p *);

extern BAD_DLL bool bad_depends_on_leader_of_regchain (
    struct bap_polynom_mpz *,
    struct bad_regchain *);

extern BAD_DLL bool bad_is_derivative_of_leader_of_regchain (
    struct bav_variable *,
    struct bad_regchain *,
    ba0_int_p *);

extern BAD_DLL bool bad_is_solved_regchain (
    struct bad_regchain *);

extern BAD_DLL bool bad_is_orthonomic_regchain (
    struct bad_regchain *);

extern BAD_DLL bool bad_is_explicit_regchain (
    struct bad_regchain *);

extern BAD_DLL bool bad_is_zero_regchain (
    struct bad_regchain *);

extern BAD_DLL ba0_int_p bad_codimension_regchain (
    struct bad_regchain *,
    struct bad_base_field *);

extern BAD_DLL unsigned ba0_int_p bad_sizeof_regchain (
    struct bad_regchain *);

extern BAD_DLL void bad_switch_ring_regchain (
    struct bad_regchain *,
    struct bav_differential_ring *);

extern BAD_DLL ba0_scanf_function bad_scanf_regchain;

extern BAD_DLL ba0_scanf_function bad_scanf_pretend_regchain;

extern BAD_DLL ba0_printf_function bad_printf_regchain;

extern BAD_DLL ba0_printf_function bad_printf_regchain_equations;

extern BAD_DLL ba0_garbage1_function bad_garbage1_inline_regchain;

extern BAD_DLL ba0_garbage2_function bad_garbage2_inline_regchain;

extern BAD_DLL ba0_garbage1_function bad_garbage1_regchain;

extern BAD_DLL ba0_garbage2_function bad_garbage2_regchain;

extern BAD_DLL ba0_copy_function bad_copy_regchain;

END_C_DECLS
#endif /* !BAD_REGCHAIN_H */
