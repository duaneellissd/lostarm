#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

#include <sys/time.h> /* we can do this, it is port file for UNIX only */
#include <unistd.h>   /* we can do this, it is port file for UNIX only */

static uint64_t timezero;

/* really simple convert absolute time into real a 64bit number in uSecs */
uint64_t TIMER64_getNow_highres(void)
{
  struct timeval tv;
  uint64_t r;
  
  gettimeofday( &tv, NULL );

  r = tv.tv_sec * 1000000;
  r = r + tv.tv_usec;

  /* remember the start time */
  if( timezero == 0 ){
    timezero = r;
  }

  /* return time from startup time */
  r = r - timezero;
  return r;
}
  


/* this code is simple, we just use the HIGH RESOULUTION timer for everything */
void TIMER_por_init(void)
{
  /* we call getNow_highres() to set 'timezero' */
  TIMER64_getNow_highres();
}



/* return time in mSecs */
uint32_t TIMER_getNow( void )
{
  uint64_t v;

  v = TIMER_getNow_highres();
  v = v / 1000;
  return (uint32_t)(v);
}
