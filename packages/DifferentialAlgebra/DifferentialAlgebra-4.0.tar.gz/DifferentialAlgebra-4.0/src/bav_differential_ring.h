#ifndef BAV_DIFFERENTIAL_RING_H
#   define BAV_DIFFERENTIAL_RING_H 1

#   include "bav_common.h"
#   include "bav_block.h"
#   include "bav_symbol.h"
#   include "bav_variable.h"
#   include "bav_operator.h"
#   include "bav_ordering.h"

#   define BAV_NOT_AN_OPINDEX	-1

/* 
 * ders [i] = the index in vars of the independent variable which has
 * root->derivation_index = i. 
 */

BEGIN_C_DECLS

/*
 * texinfo: bav_differential_ring
 * This data type implements one mathematical differential ring
 * endowed with many different orderings. It is completely
 * stored in @code{ba0_global.stack.quiet}.
 */

struct bav_differential_ring
{
  bool empty;                   // true if the structure is empty
  struct ba0_tableof_string strs;       // all identifiers
  struct bav_tableof_symbol syms;       // all symbols
  struct bav_tableof_variable vars;     // all variables
// the indices of derivations a.k.a. independent variables
// these indices are valid for both syms and vars
  struct ba0_tableof_int_p ders;
// the indices of the differential indeterminates (dependent variables)
// these indices are valid for both syms and vars
  struct ba0_tableof_int_p deps;
// the indices of the temporary variables in vars
  struct ba0_tableof_int_p tmps;
// tmps_in_use[i] is nonzero iff tmps[i] is in use
  struct ba0_tableof_int_p tmps_in_use;
//  -1 or the index in syms of the symbol used for differential operators
  ba0_int_p opra;
// all defined orderings
  struct bav_tableof_ordering ords;
// a stack of indices in ords
// the top element is the index of the current ordering
  struct bav_tableof_Iordering ord_stack;
};

#   if defined (BA0_OLDDEF)
typedef struct bav_differential_ring *bav_differential_ring;
#   endif

extern BAV_DLL void bav_init_differential_ring (
    struct bav_differential_ring *);

extern BAV_DLL struct bav_differential_ring *bav_new_differential_ring (
    void);

extern BAV_DLL unsigned ba0_int_p bav_sizeof_differential_ring (
    struct bav_differential_ring *);

extern BAV_DLL void bav_set_differential_ring (
    struct bav_differential_ring *,
    struct bav_differential_ring *);

extern BAV_DLL void bav_R_init (
    void);

extern BAV_DLL bool bav_R_is_empty (
    void);

extern BAV_DLL void bav_R_create (
    struct ba0_tableof_string *,
    struct bav_tableof_block *,
    struct bav_block *);

extern BAV_DLL bav_Iordering bav_R_new_ranking (
    struct ba0_tableof_string *,
    struct bav_tableof_block *,
    struct bav_block *);

extern BAV_DLL bool bav_R_ambiguous_symbols (
    void);

extern BAV_DLL bav_Iordering bav_R_copy_ordering (
    bav_Iordering);

extern BAV_DLL struct bav_variable *bav_R_new_temporary_variable (
    void);

extern BAV_DLL void bav_R_free_temporary_variable (
    struct bav_variable *);

extern BAV_DLL void bav_R_set_maximal_variable (
    struct bav_variable *);

extern BAV_DLL void bav_R_swap_ordering (
    bav_Iordering,
    bav_Iordering);

extern BAV_DLL void bav_R_free_ordering (
    bav_Iordering);

extern BAV_DLL void bav_R_restore_ords_size (
    ba0_int_p);

extern BAV_DLL void bav_R_push_ordering (
    bav_Iordering);

extern BAV_DLL void bav_R_pull_ordering (
    void);

extern BAV_DLL bav_Iordering bav_R_Iordering (
    void);

extern BAV_DLL struct bav_ordering *bav_R_ordering (
    void);

extern BAV_DLL bav_Inumber bav_R_variable_number (
    struct bav_variable *);

extern BAV_DLL bav_Inumber bav_R_symbol_block_number (
    struct bav_symbol *,
    ba0_int_p *);

extern BAV_DLL struct bav_variable *bav_R_derivative (
    struct bav_variable *,
    struct bav_symbol *);

extern BAV_DLL struct bav_variable *bav_R_symbol_to_variable (
    struct bav_symbol *);

extern BAV_DLL struct bav_symbol *bav_R_string_to_symbol (
    char *);

extern BAV_DLL struct bav_symbol *bav_R_string_to_derivation (
    char *);

extern BAV_DLL struct bav_variable *bav_R_string_to_variable (
    char *);

extern BAV_DLL struct bav_variable *bav_R_derivation_index_to_derivation (
    ba0_int_p);

extern BAV_DLL void bav_R_mark_variables (
    ba0_int_p);

extern BAV_DLL void bav_R_marked_variables (
    struct bav_tableof_variable *,
    ba0_int_p);

END_C_DECLS
#endif /* !BAV_DIFFERENTIAL_RING_H */
