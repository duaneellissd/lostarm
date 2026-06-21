#if !defined( LOSTARM_LOSTARM_H )
#define LOSTARM_LOSTARM_H

#include <lostarm/compiler.h>

#if defined(_MSC_VER)
#include <windows.h> // YUCK!
#endif

#include <lostarm/wrapped/_stdio.h>
#include <lostarm/wrapped/_stdint.h>

#if !defined(EXTERN_C)
#if defined(__cplusplus)
#define EXTERN_C  extern "C"
#else
#define EXTERN_C extern
#endif // cplusplus
#endif // EXTERN_C

