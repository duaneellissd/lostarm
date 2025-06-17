#include "lostarm/lostarm.h"
#include "lostarm/debug.h"
#include "the_board.h"

/*
 * This unit test verifies that the DEBUG_RAW output works.
 */

int main( int argc, char **argv )
{
  int x;
  BOARD_DEBUG_POR_Init();

  for( x = 'A' ; x < 'Z' ; x++ ){
    DEBUG_putc_raw(x);
  }
  DEBUG_putc_raw('\r');
  DEBUG_putc_raw('\n');

  DEBUG_write_raw( "abcdefghijklmnopqrstuvwxyz\r\n" );
  
  return 0;
}

    
  
    
