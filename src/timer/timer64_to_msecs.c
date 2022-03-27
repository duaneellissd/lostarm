#include <lostarm/lostarm.h>
#include <lostarm/timer.h>


 uint64_t TIMER64_to_mSecs(uint64_t tstamp)
 {
   tstamp = tstamp / (_timer64.clock_freq_hz / 1000);
   return tstamp;
 }
