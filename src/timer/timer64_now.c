#include <lostarm/lostarm.h>
#include <lostarm/timer.h>


uint32_t TIMER_getNow(void)
{
  uint64_t v;
  
  v = TIMER64_getNow_highres();
  v = v / 1000;
  return v;
}

   
