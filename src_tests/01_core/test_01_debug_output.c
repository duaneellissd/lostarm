#include <lostarm/lostarm.h>
#include <lostarm/debug.h>
#include <lostarm/wrapped/_string.h>

static void my_puts( const char *s )
{
  size_t n;
  n = strlen(s);
  (*(DEBUG_CONTEXT.pfn_tx))( &DEBUG_CONTEXT, (uint8_t *)s );
}

static my_str_hex8( const char *s, int c )
{
  char buf[8];
  my_puts(s);

  buf[0] = ':';
  buf[1] = ' ';
  buf[2] = _hex(c >> 4);
  buf[3] = _hex(c >> 0);
  buf[4] = '\n';
  buf[5] = 0;

  my_puts( &buf[0] );
}

int main( int argc, char **argv )
{
  DEBUG_por_init( (uintptr_t)(stdout), 115200 );

  /* the quintessential/obligitoryobligatory hello world */
  (*(DEBUG_CONTEXT.pfn_tx))( &DEBUG_CONTEXT, (uint8_t *)"STEP 1: Hello, world\n", 21 );
  
  int x,c;

  x = 0;
  my_puts( "STEP 2: Type abc\n", 17 );
  while( x < 3 ){
    c = (*(DEBUG_CONTEXT.pfn_rx))(&DEBUG_CONTEXT);
    if( c == EOF ){
      continue;
    }
    my_str_hex8( "you pressed", c );
    my_str_hex8( "x-count-is", x );
	    
    printf("you pressed %d, x=%d\n", c,x );
    switch( x ){
    case 0:
      if( c == 'a' ) x++ ; else x = 0; break;
    case 1:
      if( c == 'b' ) x++ ; else x = 0; break;
    case 2:
      if( c == 'c' ) x++ ; else x = 0; break;
    }
  }
  
  (*(DEBUG_CONTEXT.pfn_tx))(&DEBUG_CONTEXT, (uint8_t *)"TEST COMPLETE\n", 14 );
}
