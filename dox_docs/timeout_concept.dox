/**
 *  @file 
 *  @brief All timeouts are in milliseconds unless explcit in the function name, 0=do not block <0 block for ever.
 *  @anchor concept_timeout
 *
 * # Timeouts are in milliseconds and are 32bit signed numbers
 *
 * In general, all timeout parameters are measured in milliseconds
 *
 * If the timeout parameter is 0, it is a non-blocking call.
 * ie:  MUTEX_lock( ) with a 0 timeout will fail immeidately if the lock cannot be locked.
 *
 * If the timeout parameter is negative, it blocks for ever.
 * 
 * If the timeout parameter is positive, that is the best estimate timeout
 *
 * All timeouts generally use the TIMER_LW_start() schemea
 *
 * # Limits - no timeout can be longer then 0x7fffffff milliseconds or 24.85 days.
 * 
 * # Unsigned Math and timeouts
 *
 * To create a light weight timer, we only require the current time in milliseconds
 * We do not need to free or release this timer (big advantage!)
 * We use the concept of "unsigned math" to make this work.
 *
 * People ofen do not trust "unsigned math" and are concerned with roll over.
 * So - to remove that fear, let us walk through the math
 *
 * for 32bits the max timeout is: 2,147,483,647 milliseconds
 * We'll use 4 bits, not 32 bits - the concept is the same
 * Thus we have -8 = 0x08, to 0x7 = 7 is our range 
 *
 * Consider
 * Senario
 *    Time at start is 0x04 millisecond
 *    Timeout is at in 6 milliseconds, or when the counter gets to 0x0a
 *    But 0x0a = -6 right? how does that work?
 *
 * The answer is simple: 
 *   Step 1 - Perform the subtraction using unsigned
 *   Step 2 - cast result to signed 
 *
 *  Thus at start, the time = 0x04 over the next 3 milliseconds
 *  the time will be 5, 6 and 7, and "5-4", "6-4" and "7-4" are all positive and < 5
 *  So there is no problem, but what about 0x08, thats minus 8 right (-8)
 *  Do the math unsigned:  0x08 - 0x04 = 4, its still good, no timeout!
 *  Again at 0x09 we have 0x09 - 0x04 = 5, not there yet still good, no timeout!
 *  And next is 0x0a we have 0x0a - 0x04 = 6, that is > 5 we have a timeout!
 *
 * Alternate scenario:
 *
 *  Now what if we start at 0x0e, which is -2 using 4bit math
 *  The timeout will occur when time reaches 4 right?
 *  So, take the current time: (0x0e) and subtract, 0x0e  - 0x0e = 0, no timeout
 *  Again at 0x0f - 0x0e - we have 1
 *  But now it rolls over, 0x0f becomes 0x00 right?
 *  Unsigned math: 0x00 - 0x0e -> 2 right? (use your calculator if you need to)
 *  Unsigned math: 0x01 - 0x0e -> 3 right? (it just works)
 *
 * When does this fail?
 *  It fails if the timeout is >= the signed value (or 0x7fffffff, or 214743647 milliseconds)
 *  And how long is that?  About 24.8 days
 *
 *  We could have used at 16bit number, that would have a maximum of 32.767 seconds
 *
 *  Thus the basic rule: if your timeout is long, (like days, hours, etc) you are using
 *  the wrong tool in your tool box, you should use an alarm instead.
 * 
 */


