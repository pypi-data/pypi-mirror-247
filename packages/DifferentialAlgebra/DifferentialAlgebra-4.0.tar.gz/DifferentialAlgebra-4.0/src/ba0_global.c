#include "ba0_global.h"

BA0_DLL struct ba0_global ba0_global;

BA0_DLL struct ba0_initialized_global ba0_initialized_global = {
  {ba0_init_level, (void (*)(void)) 0, (time_t) 1, false},
  {false},
  {BA0_SIZE_CELL_MAIN_STACK, BA0_SIZE_CELL_QUIET_STACK,
        BA0_SIZE_CELL_ANALEX_STACK, BA0_NB_CELLS_PER_STACK,
      BA0_SIZE_STACK_OF_STACK, &malloc, &free},
#if defined (BA0_USE_GMP)
  {&mp_set_memory_functions, false, "Integer"},
#else
  {&bam_mp_set_memory_functions, false, "Integer"},
#endif
  {BA0_NBTOKENS}
};
