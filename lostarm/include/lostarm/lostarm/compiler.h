#include "lostarm/lostarm.h"

/* Defines/macros from:
 *   https://sourceforge.net/p/predef/wiki/Compilers/
 */

#if defined(__CC_ARM) /* arm ltd compiler */
#define _LOSTARM_CC_IS   armcc
#include "lostarm/compiler/arm_cc.h"
#endif

#if defined(__clang__)
#define _LOSTARM_CC_IS  clang
#include "lostarm/compiler/clang.h"
#endif

#if defined(__COVERITY__)
#define _LOSTARM_CC_IS_ coverity
#include "lostarm/compiler/coverity.h"
#endif

#if defined(__GNUC__)
#define _LOST_ARM_CC_IS_ gcc
#include "lostarm/compiler/gcc.h"
#endif

#if defined(__IAR_SYSTEMS_CC__)
#define _LOST_ARM_CC_IS_ iar
#include "lostarm/compiler/iar.h"
#endif

#if defined(__KEIL__)
#define _LOST_ARM_CC_IS_ keil
#incluce "lostarm/compler/keil.h"
#endif

#if defined(__MSC_VER)
#define _LOST_ARM_CC_IS_ microsoft
#include "lostarm/compiler/msvc.h"
#endif

#if defined(__MINGW32__) || defined(__MINGW64__)
#define _LOST_ARM_CC_IS_ mingw
#include "lostarm/compler/mingw.h"
#endif

#if !defined(_LOST_ARM_CC_IS_)
#error Unknown compiler! Please read the below.

/* @file compiler.h
 *
 * Every compiler has little oddball things it does differently.
 * A classic example is determining complier endianness.
 *
 * Only because GCC is so widely known, and used we try hard to coherce all 
 * other compilers to look and/or act like GCC, and use the gcc form
 * in all of the lostarm code.
 *
 * In a few cases we can't do that :-( for example the printf() macros
 * that enable checking of the printf() format verses parameters
 * In that case we just have to use two different sets of nasty macros :-(
 *
 * But when it is simple (and it mostly is simple) we would fix 
 * the macro problem with some #ifdef code in the compiler specific file
 * like this:
 *
 *  #define __ORDER_BIG_ENDIAN__    4321 // match gcc & clang
 *  #define __ORDER_LITTLE_ENDIAN__ 1234 // match gcc & clang
 *
 *  // reg_dword is a microsoft specific thing
 *  #if REG_DWORD == REG_DWORD_LITTLE_ENDIAN
 *    // compiler is big endian, make the GCC form appear
 *    #define __BYTE_ORDER__ __ORDER_BIG_ENDIAN
 *  #else
 *    // compiler is little endian, make the GCC form appear
 *    #define __BYTE_ORDER__ __ORDER_LITTLE_ENDIAN
 *  #endif
 *
 */
#endif
