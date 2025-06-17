#if !defined(LOSTARM_UNITTEST_H)
#define LOSTARM_UNITTEST_H "3707aa56-751d-4a31-a9b1-b8e92e44a15d"

#include <lostarm/lostarm.h>
#include <lostarm/wrapped/_setjmp.h>

/* your function must be called this */
typedef void unit_test_function(void);

struct unit_test_entry {
  const char *name;
  const char *filename;
  unit_test_function *pHandler;
};

struct cli_context {
  struct debug_context *pDbgCtx;
  char cmdline[100];
  char *argv[10];
  int  argc;
  jmp_buf errjmp;
  const char *prompt;
};

EXTERN_C void CLI_printf( struct cli_context *pCtx, const char *fmt, ... );
EXTERN_C void CLI_vprintf( struct cli_context *pCtx, const char *fmt, va_list ap);
EXTERN_C void CLI_gets( struct cli_context *pCtx );
EXTERN_C void CLI_parse( struct cli_context *pCtx );
EXTERN_C const char *CLI_next_arg( struct cli_context *pCtx );


struct unit_test_context {
  struct debug_context *pDbgCtx;
  int n_errors;
  int n_success;
  const struct unit_test_entry *pCurTest;
  struct cli_context *pCliCtx;
  char *argv[10];
  int argc;
  char cmdline[50];
  jmp_buf errjmp;
};

EXTERN_C const struct unit_test_entry UNIT_TEST_TABLE[];

EXTERN_C struct unit_test_context UNIT_TEST_CONTEXT;

EXTERN_C void UNIT_TEST_main(void);
EXTERN_C void UNIT_TEST_printf( const char *fmt, ... );
EXTERN_C void UNIT_TEST_vprintf( const char *fmt, va_list ap );
EXTERN_C void UNIT_TEST_fail( const char *fmt, ... );
EXTERN_C void UNIT_TEST_progress( const char *fmt, ... );
EXTERN_C void UNIT_TEST_success(void);

EXTERN_C void UNIT_TEST_gets(void);
EXTERN_C void UNIT_TEST_parse(void);
EXTERN_C const char *UNIT_TEST_next_arg(const char *name);
EXTERN_C int UNIT_TEST_next_int( const char *name );
EXTERN_C uint8_t UNIT_TEST_next_u8( const char *name );
EXTERN_C uint16_t UNIT_TEST_next_u16( const char *name );
EXTERN_C uint32_t UNIT_TEST_next_u32( const char *name );
EXTERN_C uint64_t UNIT_TEST_next_u64( const char *name );
EXTERN_C double UNIT_TEST_next_double( const char *name );


#define DECLARE_UNIT_TEST( name, quotename, quotefilename ) \
  EXTERN_C void UNIT_TEST_ ## name(void);


#define UNIT_TEST_TABLE_DECL(N) \
  extern const struct unit_test_entry UNIT_TEST_TABLE[N];

#define UNIT_TEST_TABLE_START(N) \
  const struct unit_test_entry UNIT_TEST_TABLE[] = {

#define UNIT_TEST_TABLE_ENTRY( funcname, qname, qfilename ) \
  { .name = qname, .filename = qfilename, .pHander = UNIT_TEST_ ## funcname  },

#define UNIT_TEST_TABLE_END()  { .

#endif
  
