#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

int TIMER_LW_remain( uintptr_t token, int period_msecs )
{
  int r;
  uint32_t tnow;
  uint32_t tbefore;

  tbefore = (uint32_t)(token);
  tnow = TIMER_getNow();
  
  int tmp;

  tmp = (int)(tnow - tbefore);

  r = (int)(tmp - period_msecs);

  if( r < 0 ){
    r = 0;
  }

  return r;
}
