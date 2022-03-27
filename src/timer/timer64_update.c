#include <lostarm/lostarm.h>
#include <lostarm/timer.h>

void TIMER64_update( uint32_t new_timer_value )
{
  uint32_t v32;

  /* if the new value MSB is 0 */
  v32 = new_timer_value;
  v32 = v32 >> (_timer64.nbits-1);
  v32 &= 1;

  /* if MSB is 0 */
  if( v32 == 0 ){
    v32 = _timer64.tlow;
    v32 = v32 >> (_timer64.nbits-1);
    v32 &= 1;
    if( v32 ){
      /* Old MSB was high, so simulate a carry */
      _timer64.thigh +=1;
    }
  }
}

 
