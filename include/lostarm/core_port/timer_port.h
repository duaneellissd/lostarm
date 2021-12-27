#if !defined(CORE_TIMER_PORT_H)
#define CORE_TIMER_PORT_H

#include <lostarm/lostarm.h>

/** Initilize the time subsystem.
 * @file Timer Port Requirements.
 * 
 * Also see: \ref concept_timeout
 *
 * There are different approaches for timing one can use/take.
 *
 * Ultimately the best solution is a 32bit free running counter at 1mhz.
 * Or - a 32bt free running counter at any speed >= 1mhz
 * this supplies a highresolution clock, which a lowres clock can use.
 *
 * The timer scheme purposely does not use an IRQ, many platforms use a hardware
 * timer with an interrupt to generate time - this purposely does not.
 *
 * But what should you use for this clock?
 *
 * For most ARM CortexM series, you can use the Cycle Count
 * register in the DWT (debug, watch, trace) module.
 * (provide the chip actually impliments such a feature! some do not)
 *
 * NOTE: The ARM CycleCount register burns power - not a good solution for batteries!
 *
 * for RiscV - the "mtime" register is possible depending on how you use it.
 * The mtime counts from zero and rolls over after 2^XLEN counts, some implimentations
 * also reset the timer every system tick (this cause problems with this code)
 *
 */

/** @group _32to64_timer
 * @{
 */

/** This helps a 32bit platform have a 64bit time base.
 * only a few platforms might require this helper.
 */
struct lostarm_32to64_timer {
  uint32_t tlast;          //<! Last reported timer value
  uint64_t tnow;           //<! Current time in high res clock
  uint32_t mask;           //<! precomputed mask for sign extension
  uint32_t clock_nbits;    //<! Number of bits implimented in the high speed clock
  uint32_t clock_freq_hz;  //<! Frequency of the high speed clock.
};

/** For use by the 32to64 helpers */
EXTERN_C struct lostarm_32to64_timer _32to64_timer;

/** Initialzie the 32to64 helpers
 *
 * @param nbits - How many bits long is the high speed counter.
 * @param highsped_freq_hz - frequency in hz the high speed clock runs at.
 *
 * The most optimal is if the high speed clock runs at 1mhz.
 */
EXTERN_C void TIMER_32to64_init( int nbits, uint32_t highspeed_freq_hz );

/** Update the 32to64 timer with a new reading from the high speed clock.
 * @param new_timer_value - the value of the hardware timer
 * @returns updated 64bit high speed timer.
 */
EXTERN_C uint64_t TIMER_32to64_update( uint32_t new_timer_value );


/** convert the highresolution time count to milliseconds
 * @param highspeed_time
 * @returns time converted to milliseconds.
 */
EXTERN_C uint64_t TIMER_32to64_to_mSecs( uint64_t highspeed_time );

/** convert the highresolution time count to milliseconds
 * @param highspeed_time
 * @returns time converted to milliseconds.
 */
EXTERN_C uint64_t TIMER_32to64_to_uSecs( uint64_t highspeed_time );

/*
 * @}
 */


/** Required function, initialize the hardware timer
 * This function may use the 32to64 helpers (above)
 */
EXTERN_C void TIMER_por_init(void);

/** Required function, returns the current time in some high resolution clock.
 * Porting note: this must be as fast as possible.
 */
EXTERN_C uint64_t TIMER_now_highres(void);

/** Convert the high speed clock count into microseconds.
 * For example if the main clock is 150mhz, this would
 * simply divide the given value by 150
 */
EXTERN_C uint64_t TIMER_highres_2_usecs(uint64_t value);


#if defined(__linux__) || (__APPLE_CC__)
/* we lie here */
#define LOSTARM_PORT_HIGHRES_NBITS 32
/* we normalize this to 1mhz */
#define LOSTARM_PORT_HIGHRES_FREQ_HZ 1000000
#endif
  
#if !defined(LOSTARM_PORT_HIGHRES_NBITS)
#error Missing define LOSTARM_HIGHRES_NBITS
#endif

#if !defined(LOSTARM_PORT_HIGHRES_FREQ_HZ)
#error Missing define LOSTARM_PORT_HIGHRES_FREQ_HZ - the frequency of the high resolution clock.
#endif

#endif
  
