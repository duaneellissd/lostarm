#include "lostarm/lostarm.h"
#include "lostarm/debug.h"
#include "the_board.h"

/*
 * This unit test verifies that the DEBUG_RAW output works.
 */

static void my_puts( const char *s )
{
  /* We have not tested or brough up DEBUG_puts or DEBUG_puts_no_nl()
   * So - we cannot use these yet, so we have our own function here.
   */
  while(*s){
    if( *s == '\n' ){
      DEBUG_putc_raw('\r');
    }
    DEBUG_putc_raw(*s);
    s++;
  }
}

static int _hex4( uint32_t v )
{
  v = v & 0x0f;
  if( v > 10 ){
    v = v - 10;
    v = v + 'a';
  } else {
    v = v + '0';
  }
  return v;
}

static my_str_hex32( const char *s, uint32_t value )
{
  my_puts(s);
  my_puts(": 0x");
  DEBUG_putc_raw( _hex4( value >> 28 ) );
  DEBUG_putc_raw( _hex4( value >> 24 ) );
  DEBUG_putc_raw( _hex4( value >> 20 ) );
  DEBUG_putc_raw( _hex4( value >> 16 ) );
  DEBUG_putc_raw( _hex4( value >> 12 ) );
  DEBUG_putc_raw( _hex4( value >>  8 ) );
  DEBUG_putc_raw( _hex4( value >>  4 ) );
  DEBUG_putc_raw( _hex4( value >>  0 ) );
  my_puts('\r\n');
}
      

int main( int argc, char **argv )
{
  int x;
  BOARD_DEBUG_POR_Init();
  TIMER_LW_Init();

  my_str_hex32( "start-10-sec", TIMER_LW_getNow() );
  TIMER_LW_sleep(10*1000);
  my_str_hex32( "end-10-sec", TIMER_LW_getNow() );
  exit(0);
}

    
  
    
