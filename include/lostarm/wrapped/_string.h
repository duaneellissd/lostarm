#if !defined(_WRAPPED_STRING_H)
#define _WRAPPED_STRING_H
#include <string.h>

#define strrev(s)  MISSING_strrev(s)
#define strnrev(s,n)  MISSING_strnrev(s,n)

/** 
 * @brief reverse a string
 * @param s - string to reverse
 * @return the string 
 */
char *MISSING_strrev( const char *s );

/**
 * @brief reverse the first N chars of a string.
 * @param  s - the string to reverse
 * @param  n - limit of reversal.
 * @return the string.
 */
char *MISSING_strnrev( const char *s, size_t n );


#endif
