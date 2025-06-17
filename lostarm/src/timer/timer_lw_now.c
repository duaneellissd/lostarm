#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

uint32_t TIMER_getNow(void)
{
  uint64_t t;

  t = TIMER64_getNow_highres();

  t = t / 1000;
  return t;
}
