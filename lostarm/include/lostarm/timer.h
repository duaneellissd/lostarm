#if !defined(LOSTARM_TIMER_H)
#define LOSTARM_TIMER_H "b78e38e1-053b-4b75-8ea9-b3a0ace22056"

#include <lostarm/lostarm.h>

#include <lostarm/core_port/timer_port.h>

EXTERN_C uint64_t TIMER64_getNow_highres(void); /* return now in higher resolution then milliseconds */
EXTERN_C uint32_t TIMER_getNow(void); /* return now in milli-seconds */
EXTERN_C uintptr_t TIMER_LW_start(void);
EXTERN_C uint32_t  TIMER_LW_now(void);
EXTERN_C int  TIMER_LW_isExpired( uintptr_t tstart, int period_msecs );
EXTERN_C int  TIMER_LW_consumed(uintptr_t tstart);
EXTERN_C int  TIMER_LW_remain(uintptr_t tstart, int period_msecs );

#endif
