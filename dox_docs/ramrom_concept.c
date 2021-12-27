/** \file 
 * 
 * \anchor concept_ramrom
 * 
 * Often you will come across a structure that contain the suffix _RAM or _ROM, or something simular.
 * 
 * The intent and goal of these two types of data structures is to
 * seperate that which is constant from that which is read/write.
 * 
 * Take for instance, a UART driver. There are several things that are
 * never going to change.  For example these items can be placed in the
 * FLASH ROM, and placed in the Uart_ROM structure:
 * 
 * - the base address of the UART,
 * - the interrupt number used by the UART
 * - The address of the circular queu buffer used by the uart driver.
 * 
 * In contrast, these items must live in the RAM
 * 
 * - The Read/Write indexes for the circular buffer
 * - The current state (ie: open or closed) for a UART
 * - Telemetry counts (ie: num bytes transmitted, numb bytes received)
 * 
 * The above items would be found in the Uart_RAM structure.
 */
