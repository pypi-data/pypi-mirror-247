#include "bav_global.h"
#include "bav_symbol.h"
#include "bav_variable.h"
#include "bav_rank.h"

BAV_DLL struct bav_global bav_global;
BAV_DLL struct bav_initialized_global bav_initialized_global = {
  {&bav_unknown_default},
  {&bav_scanf_default_symbol, &bav_printf_default_symbol},
  {&bav_scanf_jet_variable, &bav_printf_jet_variable,
      BAV_JET0_STRING, BAV_TEMP_STRING},
  {&bav_printf_default_rank},
  {"ordering"}
};
