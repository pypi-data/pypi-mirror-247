#include "ba0_exception.h"
#include "ba0_stack.h"
#include "ba0_int_p.h"
#include "ba0_basic_io.h"
#include "ba0_analex.h"

BA0_DLL void *
ba0_scanf_int_p (
    void *z)
{
  ba0_int_p *e;
  bool oppose;

  if (z == (void *) 0)
    e = (ba0_int_p *) ba0_alloc (sizeof (ba0_int_p));
  else
    e = (ba0_int_p *) z;

  if (ba0_sign_token_analex ("-"))
    {
      ba0_get_token_analex ();
      oppose = true;
    }
  else
    oppose = false;

  if (ba0_type_token_analex () != ba0_integer_token)
    BA0_RAISE_PARSER_EXCEPTION (BA0_ERRINT);

  *e = atoi (ba0_value_token_analex ());
  if (oppose)
    *e = -*e;
  return e;
}

BA0_DLL void
ba0_printf_int_p (
    void *z)
{
  ba0_put_int_p ((ba0_int_p) z);
}

BA0_DLL void *
ba0_scanf_hexint_p (
    void *z)
{
  BA0_RAISE_EXCEPTION (BA0_ERRNYP);
  return z;
}

BA0_DLL void
ba0_printf_hexint_p (
    void *z)
{
  ba0_put_hexint_p ((ba0_int_p) z);
}
