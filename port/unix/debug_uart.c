#include <lostarm/lostarm.h>
#include <lostarm/debug.h>

#include <termios.h> /* unix only */
#include <stdlib.h>

struct debug_context DEBUG_CONTEXT;
struct termios orig_termios

static unix_debug_tx( struct debug_context *pCtx, uint8_t *pBytes, size_t nbytes )
{
  fwrite( pBytes, 1, nbytes, (FILE *)(pCtx->hw_token));
  fflush( (FILE *)(pCtx->hw_token));
}

static void reset_terminal_mode(void)
{
  tcsetattr( fileno(stdin), TCSANOW, &orig_termios );
}

void raw_console(struct debug_context *pCtx)
{
    struct termios new_termios;
    FILE *fp;

    fp = (FILE *)(pCtx->hw_token);

    /* take two copies - one for now, one for later */
    tcgetattr(fileno(fp), &orig_termios);
    tcgetattr(fileno(fp), &new_termios);

    /* register cleanup handler, and set the new terminal mode */
    atexit(reset_terminal_mode);
    cfmakeraw(&new_termios);
    tcsetattr(0, TCSANOW, &new_termios);
}  

int unix_debug_rx( struct debug_context *pCtx )
{
  struct timeval tv = { 0L, 0L };
  fd_set fds;
  FILE *fp;
  int fn;

  fp = (FILE *)(pCtx->hw_token);
  if( fp == stdout ){
    fp = stdin;
  }
  fn = fileno(fp);
  FD_ZERO(&fds);
  FD_SET( fn, &fds);
  if (select( fn+1, &fds, NULL, NULL, &tv) <= 0 ){
    return EOF;
  }

  c = fgetc( fp );
  return c;
}
      
  


void DEBUG_port_init( uintptr_t hwspecific, int baudrate )
{
  if( DEBUG_CONTEXT.magic == ((uintptr_t)(DEBUG_por_init)) ){
    return;
  }
  raw_console();
  memset( &(DEBUG_CONTEXT), 0, sizeof(DEBUG_CONTEXT) );
  DEBUG_CONTEXT.magic = ((uintptr_t)(DEBUG_por_init));
  DEBUG_CONTEXT.time_col0 = 1;
  DEBUG_CONTEXT.tabwidth = 4;

  DEBUG_CONTEXT.hw_token = (uintptr_t)(stdout);
  DEBUG_CONTEXT.pfn_tx = unix_debug_tx;
  DEBUG_CONTEXT.pfn_rx = unix_debug_rx;
  /* make the console raw*/
  raw_console();
}


#if defined(DEBUG_UART_TEST)
int main( int argc, char **argv )
{
  DEBUG_por_init( (uintptr_t)(stdout), 115200 );

  (*(DEBUG_CONTEXT.pfn_tx))( &DEBUG_CONTEXT, "Hello, world\n");
  
  
