#if !defined(CORE_TIMER_PORT_H)
#define CORE_TIMER_PORT_H "1f56da1b-4637-4c93-a118-90e8e584b423"


#include <lostarm/lostarm.h>

/** Initilize the time subsystem.
 * @file Timer Port Requirements.
 * 
 * Each PORT must provide the functions in this file.
 */

/** This PORT function supplies the high res timer value.
 *
 * The HIGHRES time should never be an interrupt based timer.
 * The best type of timer is a freerunning hardware timer.
 * 
 * On an ARM CortexM series a good selection is the
 * DWT_CYCCNT - which per ARM is described as follows:
 *
 * The basic cycle counter DWT_CYCCNT increments on each [CPU] clock
 * cycle when the processor is not halted in debug state.
 */

struct LL_TIMER_vars {
  struct ll_timer_private {
    uint32_t last_value;
    uint64_t mask;
#define LL_TIMER32_MASK 0xFFFFffff
#define LL_TIMER24_MASK 0x00FFffff
#define LL_TIMER16_MASK 0x0000ffff
    uint32_t freq;
  } highres

class LostArmHighResTimer : public LostArmHighResTimerVars {
 public:
  /* Returns current high res time */
  uint64_t HIGHRES_getNow(void);

  /* Helper optionally used by implimentations
   * Step 1 - read your free running hardware timer.
   * Step 2 - call this function, passing:
   *         a) new timer value 
   *         b) the maxcount mask.
   *
   *         If your hardware counter is a 32bit counter.
   *         then pass HIGHRES_COUNTER32_MASK
   *         likewise for HIGHRES_COUNTER24_MASK (arm systick)
   *         likewise for HIGHRES_COUNTER16_MASK
   */
  unit64_t HIGHRES_getNow_helper( uint32_t newvalue, uint32_t maxcountmask );
  uint64_t HIGHRES_helper_arm_systick24( uint32_t newvalue );

  uint32_t LOWRES_getNow(void);
  uint32_t LOWERS_helper_generic32bit( uint32_t newvalue )
    
  

EXTERN_C uint64_t PORT_TIMER_getnow_highres(void);

// This function is helps a port impliment get_now_high_res

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
  
