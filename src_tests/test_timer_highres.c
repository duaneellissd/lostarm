
#include <lostarm/lostarm.h>

#inclue <lostarm/timer.h>


int main( int argc, char **argv )
{
  DEBUG_printf("START: TEST_TIMER\n");
  TIMER_por_init();
  
  DEBUG_printf("NOW-HIGHRES: %lld\n", ((long long)(TIMER_now_highres())));
  DEBUG_printf("NOW-LOWRES: %lld\n", ((long long))(TIMER_now()));
  TIMER_lw_sleep(1000*1000);

  DEBUG_printf("THEN-HIGHRES: %lld\n", ((long long)(TIMER_now_highres())));
  DEBUG_printf("THEN-LOWRES: %lld\n", ((long long))(TIMER_now()));

  DEBUG_printf("END: TEST_TIMER\n");
}

	       
