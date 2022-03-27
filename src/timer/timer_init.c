#include <lostarm/lostarm.h>
#include <lostarm/debug.h>
#include <lostarm/timer.h>

struct lostarm_timer64 _timer64;

void TIMER64_init( int nbits, uint32_t clock_freq )
{
  TIMER_por_init();
  memset( &(_timer64), 0, sizeof(_timer64) );

  _timer64.nbits = nbits;
  DEBUG_ASSERT1( nbits <= 32 );
  _timer64.clock_freq_hz = clock_freq;
  DEBUG_ASSERT1( clock_freq > 1000 ); /* at least 1khz */
}

