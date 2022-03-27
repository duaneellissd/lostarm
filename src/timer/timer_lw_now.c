#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

uint32_t TIMER_now(void)
{
  uint64_t t;

  t = TIMER64_now();

  t = t / 1000;
  return t;
}
