#if !defined(CORE_TIMER_PORT_H)
#define CORE_TIMER_PORT_H "1f56da1b-4637-4c93-a118-90e8e584b423"


#include <lostarm/lostarm.h>

/** Initilize the time subsystem.
 * @file Timer Port Requirements.
 * 
 * The PORT must provide:
 *
 *  1) a function that reads a high speed hardware timer at some frequency.
 *  2) The prefered timer is a 1mhz counter, but others work.
 *     Preferred range 1 to 10 mhz
 *  3) It is prefered that this is at least 32bit (24 is ok)
 *  4) RISCV - this is "mtime", for CortexM3, see: DWT->CYCNT
 *  5) See lostarm_32to64_timer below
 *
 * The port must provide a function to read the hardware timer.
 */
EXTERN_C uint64_t TIMER_getNow_highres(void);

/* This is provided based upon the above high res timer */
EXTERN_C uint32_t TIMER_getNow(void);

/* The port must also provide an initialization function */
EXTERN_C void TIMER_por_init(void);

/** @group _32to64_timer
 * @{
 */

/** This helps a 32bit platform have a 64bit time base.
 * only a few platforms might require this helper.
 */
struct _timer64 {
  uint32_t tlast;          //<! Last reported timer value
  uint64_t tnow;           //<! Current time in high res clock
  uint32_t mask;           //<! precomputed mask for sign extension
  uint32_t clock_nbits;    //<! Number of bits implimented in the high speed clock
  uint32_t clock_freq_hz;  //<! Frequency of the high speed clock.
};

/** For use by the 32to64 helpers */
EXTERN_C struct _timer64 _timer64;

/* the initialization code must call this function to init the above.
 *
 * @param clockbits - number of bits in the highres clock. (16, 24, 32)
 *                  = preference is for a 32bit clock
 * @param clockfreq - frequency in hz of the clock.
 *                  = preference is or a 1 to 10 mhz clock.
 *
 * Limitations:
 *    The pseudo timer must be 'serviced' before the highres timer overflows.
 *
 *    Assumuming 1mhz clock
 *
 * In practice that means:
 *    a 32bit counter overflows after 4294.96 seconds or 71.58 minutes
 *    At 24bits, it overflows every 16.77 seconds
 *    At 16bits every 65 milliseconds (not good)
 *
 * Good examples to use:
 *    RISCV - mtime register.
 *    CortexM3 - DWT->CYCCNT register.
 */
EXTERN_C void TIMER_32to64_init( int clockbits, uint32_t clkfreq );


/** Convert the high speed clock count into microseconds.
 * For example if the main clock is 150mhz, this would
 * simply divide the given value by 150
 */
EXTERN_C uint64_t TIMER_highres_2_usecs(uint64_t value);



#endif
  
