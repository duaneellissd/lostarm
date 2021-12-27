
#include <lostarm/lostarm.h>

/* your function must be called this */
struct unit_test_results {
  int n_errors;
  int n_warnings;
  int n_tests;
  int n_success;
};

EXTERN_C struct unit_test_results __utr__;

void UNIT_TEST_START(void) { __utr__.n_errors = __utr__.n_warnings = __utr__.n_tests = 0; }

void UNIT_TEST_ASSERT( X )  if( (X) ){ __utr.n_succes++ } else { 
