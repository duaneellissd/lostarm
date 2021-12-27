
/**
 * @file
 *
 * @brief Quick oneline extern C for C++ situations.
 *
 * This macro is often used with C++ and C code
 * It basically does the "extern "C" for you in a simple way
 * this macro is compatible with a number of standard definitions
 * found in a number of libraries (ie: GNU and Microsoft)
 *
 * They often have or use the exact same definition.
 */

#if !defined(EXTERN_C)
#if defined( __cplusplus )
#define EXTERN_C  extern "C"
#else
/** Simplistic solution to the extern "C" prefix in C/C++ code */
#define EXTERN_C  extern
#endif
#endif


