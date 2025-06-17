#include <stdio.h>
#include <lostarm/lostarm.h>
#include <lostarm/debug.h>

int main( int argc, char **argv )
{
	DEBUG_por_init( 0,  115200 );
	for(;;){
		DEBUG_puts_no_nl("hello, world\n");
	}
}
