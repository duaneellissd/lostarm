#include <lostarm/lostarm.h>
#include <lostarm/timer.h>


 uint64_t TIMER64_now(void)
 {
   uint32_t nv;
   uint64_t r;
   
   nv = TIMER64_hw_read();
   TIMER64_update(nv);

   r = _timer64.thigh;
   r = r << _timer64.nbits;
   nv = _timer64.tlow;
   nv = nv & _timer64.tmask;
   r = r | nv;
   return r;
 }
