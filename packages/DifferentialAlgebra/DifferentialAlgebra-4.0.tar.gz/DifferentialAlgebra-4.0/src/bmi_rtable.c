#include "blad.h"
#include "bmi_gmp.h"
#include "bmi_rtable.h"

/***********************************************************************
 * Management of data stored in MAPLE rtables
 *
 * First creation of rtables
 ***********************************************************************/

/*
 * Creates an empty rtable with data block of size bytes
 */

static ALGEB
bmi_empty_rtable (
    MKernelVector kv,
    ba0_int_p size)
{
  RTableSettings bmi_table_settings;
  void *cell;
  M_INT bmi_bounds[2];
  ALGEB res;

  bmi_push_maple_gmp_allocators ();

  cell = MapleAlloc (kv, (long) size);

  RTableGetDefaults (kv, &bmi_table_settings);
  bmi_table_settings.data_type = RTABLE_INTEGER32;
  bmi_table_settings.order = RTABLE_C;
  bmi_table_settings.read_only = true;
  bmi_table_settings.num_dimensions = 1;
  bmi_bounds[0] = 0;
  bmi_bounds[1] = (M_INT) (size / sizeof (UINTEGER32) - 1);
  res = RTableCreate (kv, &bmi_table_settings, cell, bmi_bounds);

  bmi_pull_maple_gmp_allocators ();

  return res;
}

/*
 * Creates a rtable involving
 *
 * A ba0_table T of 2 elements.
 * T[0] = a bav_differential_ring 
 * T[1] = a bav_tableof_parameter
 */

ALGEB
bmi_rtable_differential_ring (
    MKernelVector kv,
    char *f,
    int l)
{
  struct ba0_stack H;
  ba0_table T;
  ba0_int_p size;
  void *res, *cell;
/*
 * Though actually not important here
 */
  bmi_check_blad_gmp_allocators (f, l);

  T = ba0_new_table ();
  ba0_realloc_table (T, 2);
  T->size = 2;

  size = ba0_sizeof_table (T);
  size += bav_sizeof_differential_ring (&bav_global.R);
  size += bav_sizeof_parameters (&bav_global.parameters);

  res = bmi_empty_rtable (kv, size);

  cell = RTableDataBlock (kv, (ALGEB) res);
  ba0_init_one_cell_stack (&H, "maple", cell, size);
  ba0_push_stack (&H);

  T = ba0_new_table ();
  ba0_realloc_table (T, 2);
  T->size = 2;

  T->tab[0] = bav_new_differential_ring ();
  bav_set_differential_ring ((bav_differential_ring) T->tab[0],
      &bav_global.R);

  T->tab[1] = bav_new_parameters ();
  bav_set_parameters ((bav_tableof_parameter) T->tab[1],
      &bav_global.parameters);
  bav_switch_ring_parameters ((bav_tableof_parameter) T->tab[1],
      (bav_differential_ring) T->tab[0]);
  ba0_pull_stack ();
  ba0_clear_one_cell_stack (&H);

  return res;
}

/*
static void bmi_check_regchain (bad_regchain C, struct ba0_stack* H)
{   ba0_int_p i;

    if (! ba0_in_stack (C, H))
    {	fprintf (stderr, "error\n");
	exit (1);
    }
    if (C->decision_system.size > 0 &&
			! ba0_in_stack (C->decision_system.tab, H))
    {   fprintf (stderr, "error\n");
        exit (1);
    }
    for (i = 0; i < C->decision_system.size; i++)
    {	struct bap_itermon_clot_mpz iter;
	bap_polynom_mpz p = C->decision_system.tab [i];
	mpz_t* c;

	if (! ba0_in_stack (p, H))
	{   fprintf (stderr, "error\n");
	    exit (1);
	}
	if (! ba0_in_stack (p->clot, H))
	{   fprintf (stderr, "error\n");
	    exit (1);
	}
	bap_begin_itermon_clot_mpz (&iter, p->clot);
	while (! bap_outof_itermon_clot_mpz (&iter))
	{   c = bap_coeff_itermon_clot_mpz (&iter);
	    if (! ba0_in_stack ((*c)->_mp_d, H))
	    {   fprintf (stderr, "error\n");
		exit (1);
	    }
	    bap_next_itermon_clot_mpz (&iter);
	}
    }
}
*/

/*
 * Creates a rtable involving
 *
 * A ba0_table T of 3 elements
 * T[0] = a bav_differential_ring
 * T[1] = a bav_tableof_parameter
 * T[2] = a bad_regchain
 */

ALGEB
bmi_rtable_regchain (
    MKernelVector kv,
    bad_regchain C,
    char *f,
    int l)
{
  struct ba0_stack H;
/*
    struct ba0_mark A, B;
    ba0_int_p actual_size, max_alloc;
*/
  ba0_table T;
  ba0_int_p size;
  void *res, *cell;

  bmi_check_blad_gmp_allocators (f, l);

  T = ba0_new_table ();
  ba0_realloc_table (T, 3);
  T->size = 3;

  size = ba0_sizeof_table (T);
  size += bav_sizeof_differential_ring (&bav_global.R);
  size += bav_sizeof_parameters (&bav_global.parameters);
  size += bad_sizeof_regchain (C);

  res = bmi_empty_rtable (kv, size + 0);
  cell = RTableDataBlock (kv, (ALGEB) res);

  ba0_init_one_cell_stack (&H, "maple", cell, size + 0);
  ba0_push_stack (&H);
/*
ba0_record (&A);
*/
  T = ba0_new_table ();
  ba0_realloc_table (T, 3);
  T->size = 3;
/*
 * FIX ME.
 * Temporarily, the number of allocated bytes exceeds the size of the data
 */
  T->tab[2] = bad_new_regchain ();
  bad_set_regchain ((bad_regchain) T->tab[2], C);

  T->tab[0] = bav_new_differential_ring ();
  bav_set_differential_ring ((bav_differential_ring) T->tab[0],
      &bav_global.R);

  T->tab[1] = bav_new_parameters ();
  bav_set_parameters ((bav_tableof_parameter) T->tab[1],
      &bav_global.parameters);
  bav_switch_ring_parameters ((bav_tableof_parameter) T->tab[1],
      (bav_differential_ring) T->tab[0]);

  bad_switch_ring_regchain
      ((bad_regchain) T->tab[2], (bav_differential_ring) T->tab[0]);
/*
ba0_record (&B);
actual_size = ba0_range_mark (&A, &B);
max_alloc = ba0_max_alloc_stack (&H);
fprintf (stderr, "size = %ld, actual_size = %ld, max_alloc = %ld\n",
		(unsigned long)size,
		(unsigned long)actual_size,
		(unsigned long)max_alloc);
*/
  ba0_pull_stack ();
/*
    bmi_check_regchain ((bad_regchain)T->tab [2], &H);
*/
  ba0_clear_one_cell_stack (&H);

  return res;
}

/***********************************************************************
 * Management of data stored in MAPLE rtables
 *
 * Second extracting informations from rtables
 ***********************************************************************/

/*
 * op (k, callback) is a MAPLE table.
 * This tables may either be a DifferentialRing or a RegularChain.
 *
 * Extracts a rtable from this table (entry Ordering/Equations)
 * This rtable was created by bmi_rtable_ordering or bmi_rtable_regchain
 *
 * Load the bav_differential_ring and the bav_tableof_parameter that
 * it contains. The current ordering is returned.
 */

bav_Iordering
bmi_set_ordering (
    long k,
    struct bmi_callback *callback,
    char *f,
    int l)
{
  bav_differential_ring R;
  bav_tableof_parameter P;
  bav_Iordering r;
  ba0_table T;
  ALGEB rtable;

  bmi_check_blad_gmp_allocators (f, l);

  if (bmi_is_regchain_op (k, callback))
    rtable = bmi_table_equations_op (k, callback);
  else
    rtable = bmi_table_ordering_op (k, callback);

  bmi_push_maple_gmp_allocators ();
  T = (ba0_table) RTableDataBlock (callback->kv, rtable);
  bmi_pull_maple_gmp_allocators ();

  R = (bav_differential_ring) T->tab[0];
  P = (bav_tableof_parameter) T->tab[1];
  ba0_push_stack (&ba0_global.stack.quiet);
  bav_set_differential_ring (&bav_global.R, R);
  ba0_pull_stack ();
  r = bav_R_Iordering ();
  bav_set_parameters (&bav_global.parameters, P);
  bav_switch_ring_parameters (&bav_global.parameters, &bav_global.R);
  return r;
}

/*
 * op (k, callback) is a MAPLE table.
 * It is a RegularChain.
 *
 * Extracts a rtable from this table (entry Equations)
 * This rtable was created by bmi_rtable_regchain
 *
 * Load the bav_differential_ring, the bav_tableof_parameter 
 * and the bad_regchain that it contains. 
 *
 * The current ordering is returned.
 */

bav_Iordering
bmi_set_ordering_and_regchain (
    bad_regchain C,
    long k,
    struct bmi_callback *callback,
    char *f,
    int l)
{
  bav_differential_ring R;
  bav_tableof_parameter P;
  bad_regchain D;
  bav_Iordering r;
  ba0_table T;
  ALGEB rtable;

  bmi_check_blad_gmp_allocators (f, l);

  rtable = bmi_table_equations_op (k, callback);

  bmi_push_maple_gmp_allocators ();
  T = (ba0_table) RTableDataBlock (callback->kv, rtable);
  bmi_pull_maple_gmp_allocators ();

  R = (bav_differential_ring) T->tab[0];
  P = (bav_tableof_parameter) T->tab[1];
  D = (bad_regchain) T->tab[2];

  ba0_push_stack (&ba0_global.stack.quiet);
  bav_set_differential_ring (&bav_global.R, R);
  ba0_pull_stack ();
  r = bav_R_Iordering ();
  bav_set_parameters (&bav_global.parameters, P);
  bav_switch_ring_parameters (&bav_global.parameters, &bav_global.R);
  bad_init_regchain (C);
  bad_set_regchain (C, D);
  bad_switch_ring_regchain (C, &bav_global.R);
  return r;
}

/*
 * op (k, callback) ... op (nops (callback), callback) are MAPLE tables.
 * They are RegularChain.
 *
 * Extracts the rtables from these tables (entries Equations)
 * These rtables were created by bmi_rtable_regchain
 *
 * Load the bav_differential_ring and the bav_tableof_parameter 
 * from the first rtable.
 *
 * Load the bad_regchain(s) from each rtable.
 *
 * The current ordering is returned.
 */

bav_Iordering
bmi_set_ordering_and_intersectof_regchain (
    bad_intersectof_regchain tabC,
    long k,
    struct bmi_callback *callback,
    char *f,
    int l)
{
  bav_differential_ring R;
  bav_tableof_parameter P;
  bad_regchain D;
  bav_Iordering r;
  ba0_table T;
  ALGEB rtable;
  ba0_int_p i, nops;

  bmi_check_blad_gmp_allocators (f, l);

  rtable = bmi_table_equations_op (k, callback);

  bmi_push_maple_gmp_allocators ();
  T = (ba0_table) RTableDataBlock (callback->kv, rtable);
  bmi_pull_maple_gmp_allocators ();
/*
 * The differential ring
 */
  R = (bav_differential_ring) T->tab[0];
  P = (bav_tableof_parameter) T->tab[1];

  ba0_push_stack (&ba0_global.stack.quiet);
  bav_set_differential_ring (&bav_global.R, R);
  ba0_pull_stack ();

  r = bav_R_Iordering ();
  bav_set_parameters (&bav_global.parameters, P);
  bav_switch_ring_parameters (&bav_global.parameters, &bav_global.R);
/*
 * The regular chains
 */
  nops = bmi_nops (callback);

  bad_init_intersectof_regchain (tabC);
  bad_realloc_intersectof_regchain (tabC, nops - k + 1);

  for (i = k; i <= nops; i++)
    {
      rtable = bmi_table_equations_op (i, callback);

      bmi_push_maple_gmp_allocators ();
      T = (ba0_table) RTableDataBlock (callback->kv, rtable);
      bmi_pull_maple_gmp_allocators ();

      D = (bad_regchain) T->tab[2];
      bad_set_regchain (tabC->inter.tab[tabC->inter.size], D);
      bad_switch_ring_regchain (tabC->inter.tab[tabC->inter.size],
          &bav_global.R);
      tabC->inter.size += 1;
    }

  bad_set_attchain (&tabC->attrib, &tabC->inter.tab[0]->attrib);
  return r;
}
