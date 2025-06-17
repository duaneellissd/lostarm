#if !defined(LOST_ARM_LOST_ARM_H)
#define LOST_ARM_LOST_ARM_H "a49023e8-229c-42c1-90da-010fd57157fc"

/* @file
 * @brief This is the primary file everything must include as the first include file.
 *        It provides a few things and handles odd things across compilers.
 *
 */
#if defined(LOST_ARM_FORCE_INCLUDE_H)
#include LOST_ARM_FORCE_INCLUDE_H
#endif

#include <lostarm/lostarm/compiler.h>
#include <lostarm/lostarm/cplusplus.h>
#include <lostarm/bits.h>
#include <lostarm/wrapped/_stdio.h>
#include <lostarm/wrapped/_string.h>
#include <lostarm/wrapped/_stdbool.h>
#include <lostarm/wrapped/_inttypes.h>

#include <lostarm/core_port/cpu_port.h>
#include <lostarm/unittest.h>

/* this is generated from source code ... */
//#include <generated_unittest.h>

typedef void UNIT_TEST_FUNCTION(void);

/* All unit tests are listed in this array */
EXTERN_C const UNIT_TEST_FUNCTION *ALL_UNIT_TESTS[];

/* This is the unit test main function */
EXTERN_C void UNIT_TEST_main(void);


#endif
