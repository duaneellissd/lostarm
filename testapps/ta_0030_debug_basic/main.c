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
  DEBUG_CONTEXT.tx.cooked = 1

  DEBUG_puts("Line1");
  DEBUG_puts_no_nl("Line2\n");

  DEBUG_hex8(  0x00000000 ); DEBUG_nl();
  DEBUG_hex8(  0x00000055 ); DEBUG_nl();
  DEBUG_hex16( 0x00000000 ); DEBUG_nl();
  DEBUG_hex16( 0x0000cafe ); DEBUG_nl();
  DEBUG_hex16( 0x0000babe ); DEBUG_nl();
  DEBUG_hex16( 0x0000ffff ); DEBUG_nl();
  DEBUG_hex32( 0x00000000 ); DEBUG_nl();
  DEBUG_hex32( 0x12345678 ); DEBUG_nl();
  DEBUG_hex32( 0x87654321 ); DEBUG_nl();

  DEBUG_integer(   246350684 ); DEBUG_nl();
  DEBUG_integer(  1371559758 ); DEBUG_nl();
  DEBUG_integer(  -246350684 ); DEBUG_nl();
  DEBUG_integer( -1371559758 ); DEBUG_nl();

  DEBUG_str_hex8( "hex8-0x55", 0x55 );
  DEBUG_str_hex16( "hex16-0xcafe",0xcafe );
  DEBUG_str_hex16( "hex16-0xbabe",0xbabe );
  DEBUG_str_hex32( "hex32-0x87654321", 0x87654321 );

  DEBUG_str_str("hello", "world" );
}

    
  
    
