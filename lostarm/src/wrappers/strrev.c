#include "lostarm/lostarm.h"
#include "lostarm/debug.h"
#include "lostarm/wrapped/_string.h"

/* This exists because some compilers do not include "strrev" */

char *MISSING_strrev( char *s )
{
  return strnrev( s, strlen(s) );
}

char *MISSING_strnrev( char *s, size_t n )
{
  size_t lhs, rhs;
  size_t tmp;

  tmp = strlen(s);
  if( n > tmp ){
    n = tmp;
  }

  lhs = 0;
  rhs = n-1;
  
  while( lhs < rhs ){
    tmp = s[lhs];
    s[lhs] = s[rhs];
    s[rhs] = tmp;
    lhs++;
    rhs--;
  }

  return s;
}

void
UNITTEST_strrev( void ) 
{
  char buf[10];
  char *r;
  
  strcpy(buf, "xyzabc" );
  r = strrev( buf );
  DEBUG_ASSERT1( r == buf );
  DEBUG_ASSERT1( 0 == strcmp( "cbazyx", buf ) );

  strcpy(buf, "XYZ1ABC" );
  r = strrev( buf );
  DEBUG_ASSERT1( r == buf );
  DEBUG_ASSERT1( 0 == strcmp( "CBA1ZYX", buf ) );


}
    
