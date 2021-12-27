#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

#include <sys/time.h> /* we can do this, it is port file for UNIX only */
#include <unistd.h>   /* we can do this, it is port file for UNIX only */

static uint64_t timezero;

void TIMER_por_init(void)
{
  /* nothing here */
  TIMER_now_highres();
}


uint64_t TIMER_now_highres(void)
{
  struct timeval tv;
  uint64_t r;
  
  gettimeofday( &tv, NULL );

  r = tv.tv_sec * 1000000;
  r = r + tv.tv_usec;
  if( timezero == 0 ){
    timezero = r;
  }
  r = r - timezero;
  return r;
}
  

uint64_t TIMER_uSecs( void )
{
  uint64_t v;

  v = TIMER_now_highres();
  return v;
}

uint32_t TIMER_getNow( void )
{
  uint64_t v;

  v = TIMER_uSecs();
  v = v / 1000;
  return (uint32_t)(v);
}

void TIMER_init(void)
{
  /* this will set timezero */
  timezero = TIMER_now_highres();
}

#if defined( LINUX_TEST_TIMER )


int main( int argc, char **argv )
{
  TIMER_por_init();

  printf("NOW %lld\n", ((long long)(TIMER_now_highres())));
  sleep(1);
  printf("NOW %lld\n", ((long long)(TIMER_now_highres())));
  sleep(1);
  printf("NOW %lld\n", ((long long)(TIMER_now_highres())));
}

#endif

	
  

  
