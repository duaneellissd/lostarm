#include <lostarm/lostarm.h>
#include <lostarm/debug.h>
#include <lostarm/timer.h>
#include <lostarm/wrapped/_unistd.h>
#include <lostarm/wrapped/_stdlib.h>

#include <termios.h>

static struct termios old_termios;
static int need_atexit;

struct debug_context DEBUG_CONTEXT;

static uint16_t debug_rx_buffer[32];

static int my_atexit(void)
{

  if( need_atexit ){
    need_atexit = 0;
    
    if( tcsetattr( STDIN_FILENO, TCSANOW, &old_termios ) != 0 ){
      fprintf( stderr, "Cannot restore old tty settings, error: (%d) %s\n", errno, strerror(errno) );
      exit(1);
    }
  }
}

void DEBUG_fatal_here( const char *filename, int lineno, const char *fmt, ... )
{
  va_list ap;

  va_start( ap, fmt );
  DEBUG_fatal_herev( filename, lineno, fmt, ap );
  va_end(ap);
}

voi DEBUG_fatal_herev( const char *filename, int lineno, const char *fmt, va_list ap )
{
  fprintf( stderr, "%s:%d: ", filename, lineno );
  vfprintf( stderr, fmt, ap );
  fflush( stderr );
  my_atexit();
  exit(1);
}

static void make_raw(void)
{
  if( tcgetattr( STDIN_FILENO, &old_termios ) != 0 ){
    fprintf( stderr, "Cannot get old tty settings, error: (%d) %s\n", errno, strerror(errno) );
    exit(1);
  }

  struct termios new_termios;

  new_termios = old_termios;
  cfmakeraw( &new_termios );
  new_termios.c_cc[VMIN] = 1;
  new_termios.c_cc[VTIME] = 0;

  atexit( my_atexit );
  
  if( tcsetattr( STDIN_FILENO, TCSANOW, &new_termios ) != 0 ){
    fprintf( stderr, "Cannot set new tty settings, error: (%d) %s\n", errno, strerror(errno) );
    exit(1);
  }
  need_atexit = 1;
}

static void posix_debug_tx( struct debug_context *pDBG_CTX, const uint8_t *pBuf, size_t nbytes )
{
  (void)write( STDOUT_FILENO, pBuf, nbytes );
}

static void posix_debug_rx_poll( struct debug_context *pDBG_CTX, uintptr_t tstart, int timeout )
{
  fd_set readable;
  int r;
  int timeremain;

  FD_ZERO( &readable );
  FD_SET( STDIN_FILENO, &readable );

  if( tstart == 0 ){
    tstart = TIMER_LW_start();
  }

  do {
    if( timeout < 0 ){
      // we ignore forever and treat it as 100
      timeout = 100;
    }
    if( timeout > 0 ){
      // we artifically limit this to 100msecs
      if( timeout > 100 ){
	timeout = 100;
      }
      timeout = TIMER_LW_remain( tstart, timeout );
      tv.tv_sec = (time_t)(timeout / 1000);
      tv.tv_usec = (timeout * 1000) % 1000000;
      break;
    }
    if( timeout == 0 ){
      // this is a poll operation, no wait.
      tv.tv_sec = 0;
      tv.tv_usec = 0;
      break;
    }
  } while(0)
    ;
  r = select( STDIN_FILENO + 1, &readable, NULL, NULL, &tv );
  if( FD_ISSET( STDIN_FILENO, &readable ) ){
    uint8_t rxbuf[32];
    r = read( STDIN_FILENO, &rxbuf, sizeof(rxbuf) );
    if( r > 0 ){
      DEBUG_handle_rx_nbytes( pDBG_CTX, rxbuf, r );
    }
  }
}
      
  
  

void DEBUG_UART_Init( uintptr_t not_used, struct debug_context *pDBG_CTX, int baudrate_notused )
{
  (void)(not_used);
  (void)(buadrate_notused);

  make_raw();

  memset( pDBG_CTX, 0, sizeof(*pDBG_CTX) );
  pDBG_CTX->mMagic = (uintptr_t)(&DEBUG_UART_Init);
  pDBG_CTX->mTimeCol0 = 1;
  pDBG_CTX->mRawMode = 0;
  pDBG_CTX->mSigKill = 1;

  RBUF_Init( &(pDBG_CTX->debug_rx_ring_buffer), sizeof( debug_rx_buffer ), sizeof(debug_rx_buffer[0]) );

  pDBG_CTX->pfn_Tx = posix_debug_tx;
  pDBG_CTX->pfn_RxPoll = posix_debug_rx_poll;
}

  
  

  
