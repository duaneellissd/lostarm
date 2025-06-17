#if !defined(_WRAPPED_STRING_H)
#define _WRAPPED_STRING_H "58f5fc6f-5f73-4c5f-9e76-28f4c07498a1"

#include <string.h>

#define strrev(s)  MISSING_strrev(s)
#define strnrev(s,n)  MISSING_strnrev(s,n)

/** 
 * @brief reverse a string
 * @param s - string to reverse(will be modified)
 * @return the string 
 */
EXTERN_C char *MISSING_strrev( char *s );

/**
 * @brief reverse the first N chars of a string.
 * @param  s - the string to reverse(will be modified)
 * @param  n - limit of reversal.
 * @return the string.
 */
EXTERN_C char *MISSING_strnrev( char *s, size_t n );


#endif
