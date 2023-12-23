#ifndef BA0_ANALEX_H
#   define BA0_ANALEX_H 1

/* 
 * Lexical analyzer.
 * Catches tokens on ba0_input
 * Makes use of its own stack.
 * Numbers are stored as strings (temporarily)
 */

#   include "ba0_common.h"

/* 
 * The different types of tokens
 */

BEGIN_C_DECLS

enum ba0_typeof_token
{
  ba0_no_token,
  ba0_integer_token,
  ba0_sign_token,
  ba0_string_token
};

/* 
 * One token
 */

struct ba0_token
{
  enum ba0_typeof_token type;
  bool spaces_before;
  char *value;
};

/* 
 * FIFO of tokens
 */

struct ba0_analex_token_fifo
{
  struct ba0_token *fifo;
  ba0_int_p first, last, counter;
};

/* 
 * The max length of the FIFO
 */

#   define BA0_NBTOKENS    20

/* 
 * The length of the error context string
 */

#   define BA0_CONTEXT_LMAX 60

extern BA0_DLL void ba0_set_settings_analex (
    ba0_int_p);

extern BA0_DLL void ba0_get_settings_analex (
    ba0_int_p *);

extern BA0_DLL char *ba0_get_context_analex (
    void);

extern BA0_DLL void ba0_write_context_analex (
    void);

extern BA0_DLL void ba0_init_analex (
    void);

extern BA0_DLL void ba0_clear_analex (
    void);

extern BA0_DLL void ba0_reset_analex (
    void);

extern BA0_DLL void ba0_record_analex (
    void);

extern BA0_DLL void ba0_restore_analex (
    void);

extern BA0_DLL void ba0_set_analex_FILE (
    FILE *);

extern BA0_DLL void ba0_set_analex_string (
    char *);

extern BA0_DLL ba0_int_p ba0_get_counter_analex (
    void);

extern BA0_DLL void ba0_get_token_analex (
    void);

extern BA0_DLL void ba0_unget_token_analex (
    ba0_int_p);

extern BA0_DLL void ba0_unget_given_token_analex (
    char *,
    enum ba0_typeof_token,
    bool);

extern BA0_DLL bool ba0_sign_token_analex (
    char *);

extern BA0_DLL bool ba0_spaces_before_token_analex (
    void);

extern BA0_DLL enum ba0_typeof_token ba0_type_token_analex (
    void);

extern BA0_DLL char *ba0_value_token_analex (
    void);

END_C_DECLS
#endif /* !BA0_ANALEX_H */
