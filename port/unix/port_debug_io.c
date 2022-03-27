#include <lostarm/lostarm.h>
#include <lostarm/debug.h>


#include <termios.h> /* unix only */
#include <stdlib.h> /* this is a unix only file */
#include <sys/ioctl.h>
#include <unistd.h> /* this is a unix only file */
#include <sys/select.h> /* unix only */

struct debug_context DEBUG_CONTEXT;
struct termios orig_termios_STDIN;
struct termios orig_termios_STDOUT;

static void unix_debug_tx( struct debug_context *pCtx, uint8_t *pBytes, size_t nbytes )
{
  /* this layer does not do CR/LF mapping */
  write( STDOUT_FILENO, pBytes, nbytes );
}

static void reset_terminal_mode(void)
{
  tcsetattr( STDIN_FILENO, TCSANOW, &orig_termios_STDIN );
  tcsetattr( STDOUT_FILENO, TCSANOW, &orig_termios_STDOUT);
}

void raw_console(struct debug_context *pCtx)
{
  struct termios new_termios_STDIN;
  struct termios new_termios_STDOUT;
    FILE *fp;

    /* take two copies - one for now, one for later */
    tcgetattr(STDIN_FILENO,  &orig_termios_STDIN);
    tcgetattr(STDOUT_FILENO, &orig_termios_STDOUT);
    tcgetattr(STDIN_FILENO, &new_termios_STDIN);
    tcgetattr(STDOUT_FILENO, &new_termios_STDOUT);

    /* register cleanup handler, and set the new terminal mode */
    atexit(reset_terminal_mode);
    cfmakeraw(&new_termios_STDIN);
    cfmakeraw(&new_termios_STDOUT);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_termios_STDIN);
    tcsetattr(STDOUT_FILENO, TCSANOW, &new_termios_STDOUT);
}  


static int kbhit(void) {
    static bool initflag = false;
    int nbbytes;
    ioctl(STDIN_FILENO, FIONREAD, &nbbytes);  // 0 is STDIN_FILENO
    return nbbytes;
}

static int unix_debug_rx( struct debug_context *pCtx )
{
  (void)(pCtx);
  char c;
  int r;
  
  if( kbhit() == 0 ){
    return EOF;
  }

  r = read( STDIN_FILENO, &c,1 );
  /* remove sign extend */
  r = (int)(c) & 0x0ff;
  return r;
}

      
  


void DEBUG_por_init( uintptr_t hwspecific, int baudrate )
{
  if( DEBUG_CONTEXT.magic == ((uintptr_t)(DEBUG_por_init)) ){
    return;
  }
  
  memset( &(DEBUG_CONTEXT), 0, sizeof(DEBUG_CONTEXT) );

  DEBUG_CONTEXT.magic = ((uintptr_t)(DEBUG_por_init));
  DEBUG_CONTEXT.hw_token = (uintptr_t)(stdout);

  /* make the console raw*/
  raw_console(&DEBUG_CONTEXT);

  DEBUG_CONTEXT.time_col0 = 1;
  DEBUG_CONTEXT.tabwidth = 4;

  DEBUG_CONTEXT.pfn_tx = unix_debug_tx;
  DEBUG_CONTEXT.pfn_rx = unix_debug_rx;
}

