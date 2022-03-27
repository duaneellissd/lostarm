#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

uintptr_t TIMER_LW_start_update( void )
{
  uint32_t t;

  t = TIMER_now();

  return (uintptr_t)(t);
}


