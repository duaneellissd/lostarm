/**
 *  @file 
 *
 *  @anchor concept_debuguart
 *  @anchor concept_debug
 *
 * # Debug Uarts must always work period - otherwise they are useless.
 *
 * The debug uart needs to work no matter what. So for that reason, the
 * DEBUG uart should not use IRQs for transmit purposes.
 *
 * The DEBUG UART thus never uses an interrupt to transmit - this is super important!
 *
 * Why?  Often in an embeded system you are debugging a problem inside an
 * interrupt service routine, and you need to print the value of
 * something, ie: "x = 123" "start-of-irq", and when you do you cannot
 * and you shall not use or require the standard library. 
 *
 * # why not use Printf(), why not use the standard printf() what is DEBUG_pm_printf()?
 * 
 * By design, DEBUG_pm_printf() does not use the standard library features
 * instead it uses its own printf schema. But Why?
 *
 * Reason #1 - Again, you often need to print a message during an
 * interrupt service routine, or when Interrupts are disabled!  And if
 * the debug transmit required interrupts to function it will not work.
 *
 * Reason #2 - Newlib (one of the most common standard libraries) calls
 * Malloc() to create an IO buffer for use by printf() Well, Malloc() is
 * often wrapped with a mutex lock/unlock operation.
 *
 * But - when the OS crashes, where are you and what is going on?
 *
 * - Q: Are interrupts working?
 * - A: No - you are in an exception handler, you cannot turn them on to transmit
 *
 * - Q: But I thought you should not write blocking code in an interrupts service routine?
 * - A: Yea, suck it up my young jedi apprentice, this is debug there are no rules you often break rules in debug.
 *      That's also why we print small tiny messages instead verbose sentences.
 *
 * - Q: printf() calls malloc right? Yes it does to allocate space for a 'File Buffer'
 * - A: Splat/you-are-dead - The malloc variables are often
 *      trashed by now or overwritten with garge, malloc is not going to work anyway.
 *
 * - Q: printf() calls malloc which calls mutex functions.
 * - A: Splat/you-are-dead - again you are in a crashdump and you want everything to 
 *      still work? it is not happening. Your RTOS is not going to accept recursion in side handlers!
 *
 * # What is and is not supported
 *
 * Number 1 - No support for floating point (this might get added later)
 * Number 2 - No support for wide chars (its debug, not consumer printf())
 * Number 3 - No support for locale, or positional parameters (we are not translating debug text, so its not consumer printf())
 *
 * # DEBUG_UART - Circular buffers are 8 bit and 16bits
 *
 * The DEBUG UART for transmit purposes, is an 8bit buffer (x256 suggested depth)
 * The DEBUG UART for RX purposes is 16bit - reason: 16bit is required to support function keys and alt key sequences
 * 
 * The DEBUG_getc() can/will decode teraterm ansi-arrow keys (which are multi-byte) into a single 16bit value
 * Likewise the PC keyboard has many other keys like PgUp and PgDn - these get mapped also in the windows mode
 *
 * DEBUG_printf() part 2
 *
 * Most often in debug you want to print a simple string followed by a number.
 *
 * 
 * You might be debugging something (for example a stack overflow) or other nasty problem.
 * Or your task might have a "small stack" (not a large stack) - printf requires lots of stack space
 *
 * So how do you output a message in a simple form, ie:
 *      ~~~~~~~~~~~{.c}
 *      DEBUG_pm_printf("inside handler, flags=0x%08x\n", flagvalue );
 *      ~~~~~~~~~~~
 * 
 * But - printf() requires lots of stack space - do you have stack space? Are you debugging a stack overflow?
 * Does the current task (or IRQ) have small stack or a large stack? You are stuck right?
 *
 * Thus there are 2 ways to ouptut text, either: (A) DEBUG_pm_printf() or DEBUG_str_hex32() [or simular]
 * What is the difference between these two?
 *
 * The simple function:
 *     ~~~~~~~~~~~~{.c}
 *     void DEBUG_str_hex32( const char *msg, uint32_t param );
 *     ~~~~~~~~~~~~
 *
 * Is implimented like this and requires minimal stack space!
 *
 * ~~~~~~~~~~~~~~~~~{.c}
 * void DEBUG_str_hex32( const cahr *msg, uint32_t param );
 * {
 *      DEBUG_str_colon( msg ); // output msg + ":" + "space"
 *      DEBUG_hex32( param );  // minimal stack space
 *      DEBUG_nl(); // finally the terminal newline
 * }
 * ~~~~~~~~~~~~~~~~~
 * 
 *
 */


