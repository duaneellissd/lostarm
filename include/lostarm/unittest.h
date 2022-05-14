#if !defined(LOSTARM_UNITTEST_H)
#define LOSTARM_UNITTEST_H "3707aa56-751d-4a31-a9b1-b8e92e44a15d"

#include <lostarm/lostarm.h>
#include <lostarm/wrapped/_setjmp.h>

/* your function must be called this */
struct unit_test_results {
  int n_errors;
  int n_warnings;
  int n_tests;
  int n_success;
};

struct unit_test_context {
  struct debug_context *pCtx;
  char cmdline[100];
  char *argv;
  int  argc;
  jmp_buf errjmp;
};

typedef void unit_test_function(void);


struct unit_test_entry {
  const char *name;
  const char *filename;
  unit_test_function *pHandler;
};

EXTERN_C void UNIT_TEST_printf( const char *fmt, ... );
EXTERN_C void UNIT_TEST_fail( const char *fmt, ... );
EXTERN_C void UNIT_TEST_progress( const char *fmt, ... );
EXTERN_C void UNIT_TEST_success(void);

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
  
