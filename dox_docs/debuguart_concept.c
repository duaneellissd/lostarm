/**
 *  @file 
 *
 *  @anchor concept_debuguart
 *  @anchor concept_debug
 *
 * # Debug Uarts - requirements
 *
 *  - They must always work period - otherwise they are useless.
 *  - This means when IRQs are disabled
 *  - This means when the system has crashed horribly.
 *
 * # Debug Uarts - derived requirements
 *
 *  - They cannot use IRQs to transmit, they must be 100% polled
 *  - They effectively cannot use a sw buffer, there is no IRQ to transmit.
 *  - They cannot use or require the system "printf()" components
 *  - Reason: printf() often calls malloc and the system has crashed.
 *  - Reason: malloc() may need to call the OS to lock the heap
 *  - Cannot lock the heap in side an IRQ handler..
 *
 * # Debug UART verses the STANDARD UART API
 *  - the DEBUG UART is written as an addon to the standard UART
 *  - Your port should support both polled and irq driven uarts.
 *
 * # Thus - Debug Uarts must work no matter what.
 *
 * DEBUG also (and often) is nothing more then print something like: 'x = 12'
 * or other short and simple output that is not complicated or fancy.
 *
 * Thus there are two ways to print things,
 *  ie: DEBUG_printf() which is costly and/or complex to use but full featured.
 * and simple functions like:  DEBUG_str_hex32( const char *prefix, uint32_t value )
 *
 * Both of these functions boil down to the "DEBUG_VARS" global variable.
 *
 * # DEBUG - reception (not transmission)
 *
 * If possible, the debug UART should support RX interrupts (not required but helpful).
 * The idea is using the DEBUG uart to ymodem-receive a large block of data.
 * Another idea is to support function/arrow keys (multi-byte sequence keys)
 *
 * In both cases the data comes rapidly, and may overflow the UART RX Fifo.
 * (some chips have a 16byte rx fifo, but many older ones have no fifo)
 *
 * The platform needs to supply an DEBUG_rx_poll() function that polls the hardware.
 * That function should in theory play nice with RX data via an RX interrupt.
 *
 * For example - the hw specifc function does the following:
 *   - Disable CPU interrupts.
 *   - Right after the disable, a byte is Received by hardware.
 *   - Two things happen (1) the status bit say DATA READY, and (2) IRQ is asserted.
 *   - The poll code sees the DATA READY and consumes the byte
 *   - The poll code then re-enables the IRQ
 *   - The DEBUG UART RX irq fires (see above)
 *   - The UART RX handler needs to understand maybe there will be NO data (see above)
 *   - Some systems call this a "spurious interrupt" ..
 *   - If you want to accomidate ymodem and arrow keys this might be important for your port.
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
 * # why not use Printf(), why not use the standard printf() what is DEBUG_printf()?
 * 
 * By design, DEBUG_printf() does not use the standard library features
 * instead it uses its own printf schema. But Why?
 *
 * Reason #1 - Again, you often need to print a message during an
 * interrupt service routine, or when Interrupts are disabled!  And if
 * the debug transmit required interrupts to function it will not work.
 *
 * Reason #2 - Newlib (and NANO, the most common standard libraries) calls
 * Malloc() to create an IO buffer for use by printf() Problem is, Malloc() is
 * often wrapped with a mutex lock/unlock operation and what if your OS is dead
 * Or the OS in a state where you cannot use lock/unlock()? what now?
 *
 * Reason #3 When the OS crashes, where are you and what is going on?
 *
 * - Q: Are interrupts working?
 * - A: No - you are in an exception handler, you cannot turn them on to transmit
 *
 * - Q: But I thought you should not write blocking code in an interrupts service routine?
 * - A: Yea, suck it up my young jedi apprentice, this is debug there are no rules you often break rules in debug.
 *      That's also why we print small tiny messages(nmsgs=3) instead verbose sentences (total mesages received: 3)
 *
 * - Q: printf() calls malloc right? Yes it does to allocate space for a 'File Buffer'
 * - A: Splat/you-are-dead - The malloc variables are often
 *      trashed by now or overwritten with garbage, malloc is not going to work anyway.
 *
 * - Q: printf() calls malloc which calls mutex functions.
 * - A: Splat/you-are-dead - again you are in a crashdump and you want everything to 
 *      still work? it is not happening. Your RTOS is not going to accept recursion inside handlers!
 *
 * - Q: DEBUG_printf() often requires a HUGE amount of stack space (500 bytes?) on an embedded system
 *      that can be painful, but it can be planned for. And if this becomes a problem there are alternatives
 *      such as the DEBUG_str_hex16() or DEBUG_str_int() functions you can use.
 *
 * # DEBUG_printf() What is and is not supported
 *
 * Number 1 - No support for floating point (this might get added later)
 * Number 2 - No support for wide chars (its debug, not consumer printf())
 * Number 3 - No support for locale, or positional parameters (again: not a consumer printf() this is debug!)
 *
 * # DEBUG_UART - Circular buffers are 16bits
 *
 * The DEBUG uart uses 8bit TX buffers, and 16bit RX buffers why?
 *
 * On the TX side there is no need for 16bit we only transmit bytes.
 *
 * On the RX side, this is to support ANSI function keys, arrow keys, and other related keys.
 * Thus, a normal key sequene is an 8bit number (0..0xff) but fancy keys are 16bit keys.
 *
 * # DEBUG_UART - decoding fancy keys (arrows and function keys) how?
 *
 * Generally, an arrow key is something like the byte sequence "\x1b[A" or "\x1b[C"
 * And the key sequence is fast - faster then a human can reasonably type.
 *
 * Thus, when the DEBUG_UART sees an ESC, it starts a simple timer
 * If the decode sequence completes FAST (within 10mSECS) it is a fancy key.
 * Otherwise the human is typing the key.
 *
 * # Controlling Debug Stack Space
 * 
 * DEBUG_printf() requires lots of stack space - do you have stack space? Are you debugging a stack overflow?
 * Does the current task (or IRQ) have small stack or a large stack? You are stuck right?
 *
 * There are alternatives: Look at the functions: DEBUG_str_hex32() [or simular]
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
 * void DEBUG_str_hex32( const char *msg, uint32_t param );
 * {
 *      DEBUG_str_colon( msg ); // output msg + ":" + "space"
 *      DEBUG_hex32( param );  // minimal stack space
 *      DEBUG_nl(); //  the terminal newline
 * }
 * ~~~~~~~~~~~~~~~~~
 *
 * It is effectively (but without the stack needs)
 *
 * ~~~~~~~~~~~~~~~~~{.C}
 * void DEBUG_str_hex32( const char *msg, uint32_t param )
 * {
 *      DEBUG_printf("%s: 0x%08x\n", msg, param );
 * }
 * ~~~~~~~~~~~~~~~~~
 *
 */


