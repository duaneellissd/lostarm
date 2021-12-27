#include "lostarm/lostarm.h"
#include "lostarm/wrapped/_string.h"


char *strrev( char *s )
{
  return strnrev( s, strlen(s) );
}

char *strnrev( char *s, size_t n )
{
  int lhs, rhs;

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


void TEST_CASE_strrev( void ) 
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
    
