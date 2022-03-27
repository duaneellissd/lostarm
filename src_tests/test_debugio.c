
#include <lostarm/lostarm.h>

#include <lostarm/debug.h>
#include <losarm/unittest.h>


static void test2(void)
{

  int n;
  my_puts("sart: TEST2\n");
  DEBUG_puts_no_nl("prompt> ");

  n = 0;
  for(;;){
    c = DEBUG_getc( 1000 );
    if( c == EOF ){
      DEBUG_puts_no_nl("no-key\n");
      continue;
    }
    DEBUG_str_int("KEYPRESS", c );
    if( c == "done"[n] ){
      n++;
    } else {
      n = 0;
    }
  }
    
  DEBUG_puts_no_nl("TEST1: debug puts no nl");
  DEBUG_puts_no_nl("TEST2: debug puts with nl\n");
  DEBUG_puts("TEST3: puts");
}

static void my_puts( const char *s )
{
  int c;

  for(;;){
    c = *s;
    s++;
    if( c== 0 ){
      break;
    }
    if( c == '\n' ){
      DEBUG_putc_raw('\r' );
    }
    DEBUG_putc_raw( c );
  }
}

       
static void test1(void)
{
  my_puts("start: TEST1\n");
  DEBUG_puts("TEST1 debug_puts()");
  DEBUG_puts_no_nl("TEST2 debug_puts_no_nl()\n");
  my_puts("end: TEST1\n");
}


int main( int argc, char **argv )
{
  DEBUG_por_init( 0, 115200 );
  test1();
  test2();

  exit(0);
}

