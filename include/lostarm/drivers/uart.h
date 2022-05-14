#include <lostarm/lostarm.h>

struct uart_ROM;
struct uart_RAM;
struct uart_CONFIG;

#include "lostarm/drivers/uart_structs.h"

/**
 * \file 
 * @brief Basic UART IO functions.
 *
 * Common Things
 *
 * From a hardware point of view there are many common things to uarts.
 *
 * All UARTS (tx and rx) have a transmit and receive circular buffer.
 * The core code places (copies) all data through the circular buffer.
 *
 * Simple means to transmit:
 *
 *   struct uart_RAM *pHandle;
 *
 *   pHandle = UART_open( "namehere", &uart_cfg );
 *   DEBUG_ASSERT( pHandle != NULL );
 *
 *   // NOTE: this is blocking until the string is in the tx sw fifo.
 *   UART_write( pHandle, "Hello, world\n", 13 );
 *
 *   Or
 *	void *vp;
 *  	size_t n;
 *   	UART_txDmaStart( pHandle, &vp, n );
 *   	DEBUG_ASSERT( n >= 13 );
 *   	memcpy( vp, "Hello, world\n", 13 );
 *   	DEBUG_txDmaComplete( pHandle, 13 );
 *
 *   // To read
 *   ch = UART_getch( pHandle, 100 );
 *   if( ch == -1 ){
 *        DEBUG_printf("timeout...");
 *   } else {
 *        DEBUG_hex8( "rx-char", ch );
 *   }
 *
 *   or
 *     int n;
 *     char buf[10];
 *     // 100msec wait timeout 
 *     n = UART_read( pHandle, buf, sizeof(buf), 100 );
 *     if( n < 0 ){
 *         DEBUG_printf("Timeout\n");
 *     } else {
 *         DEBUG_printf("Received %d bytes\n", n );
 *         DEBUG_hexdump8( 0, &buf[0], n );
 *     }
 *
 *  // Still transmitting? then wait
 *  while( UART_isTxBusy( pHandle ) )
 *      ; 
 *  UART_close( pHandle );
 *
 * Also see: \ref concept_dmastart to understand how the DmaStart functions work
 *
 * How the uart driver works internally:
 *
 * To transmit, the UART_CORE code, copies/inserts the data to transmit
 * into the tx circular buffer then - calls the uart specific driver
 * to *start* the transmission, or "prime the interrupt pump".
 *
 * The driver has 3 choices:
 *
 *   1) IRQ based
 *
 *      Load the UART fifo and enable interrupts
 *      Then during the TX IRQ (fifo empty) load more
 *      this continues until transmission is complete.
 *      (This is acomplished via the UART DMA functions
 *      eventhough there is no DMA going on)
 *
 *   2) DMA Based (with IRQ)
 *
 *      Call the UART DMA Operation function obtain a pointer and count.
 *      And configure the DMA to tansmit from the pointer and for count bytes.
 *      When the DMA raises the DONE IRQ, just like the IRQ based load up more.
 *      Eventually shut down the DMA when the transmission is complete.
 *
 *   3) Polled/Blocking.
 *
 *      Option 1 - is to block until transmission is complete
 *      (Again, using the DMA functions to access the tx buffer)
 *      Calling again and again to load more bytes into the tx HW fifo.
 *
 *      Option 2 - arrange for a 'callback' to occur later
 *      that callback could/should would poll and refill the tx uart channel.
 *
 * NOTE: About the TX and RX software fifos.
 *
 *   As one would expect the TX and RX uart channels are backed by
 *   an application Circular buffer of application defined size.
 *   This means your driver neeeds to deal with wrapped circular buffers.
 *
 *   All circular buffers "wrap" around, this means, and this is how
 *   you handle it
 *
 *   Step 1: the first time your DMA based driver calls DMA_Start(),
 *   you will get a pointer to the tail end of the buffer and a length.
 *
 *   This is a pointer to a linear chunk of memory (no wrap) and a
 *   count of bytes upto the point where the buffer warps. Effectively
 *   your pointer is pointing at the 'end part' of the buffer before
 *   the wrap, and the length is number of bytes upto the wrap point.
 *
 *   Step 2: Transmission occurs and progresses.
 *   Eventually, you can call DMA_Complete(), this completes the "buffer end"
 *
 *   Provided all of the bytes are used, the buffer will no longer be
 *   wrapped, buffer will be back at the start.
 *
 *   Step 3: The second time you call DMA_Start() you will get a pointer to
 *   the start of the buffer, and a length of all available bytes.
 *
 * If more data is ready for transmission, it will be added to the buffer
 * And the hardware txstart will be called again
 *
 * The same basic process works for the RX process.
 *
 */

/** Basic hardware UART driver transmit callback (low level IO function)
 * 
 * This should write the bytes (raw) to the debug IO channel (UART)
 * Some notes:
 *   This should be a blocking call
 *   This should return when the last byte of data is in the UART fifo.
 *   This should not use or require interrupts.
 *   Note that CR/LF - mapping has already been done above this.
 *
 * @param pRamThis - pointer to the RAM portion of the struct.
 *
 * @return (often ignored, but not always) actual number of bytes transmitted.
 * @return negative is an error
 *
 * This function should call UART_txDmaStart() to obtain data
 * and later call UART_txDmaComplete() when finished
 */
typedef int fn_dbg_io_txstart( struct uart_RAM *pRamThis );

/** Basic hardware UART driver receive function (low level IO function)
 *
 * This should read bytes (raw) from the debug IO channel (UART)
 * * The timeout parameter controls how long the function blocks.
 * * If timeout is negative, the function blocks for ever.
 * * if timeout is zero, the function does not block.
 * * if timeout is positive, the function blocks for at most (N) milliseconds.
 * Implimenentations can ignore the timeout value, or use it as a hint.
 *
 * @param pRamThis - pointer to the RAM portion of this struct.
 * @param timeout - how long this functions should wait before returning.
 *
 * @return The number of bytes actually received, 0 in case of timeout with nothing
 *
 */

typedef int fn_dbg_io_rxpoll( struct uart_RAM *pRamThis, int timeout);


/* Unget16 is used by debug uart only */
EXTERN_C int UART_ungetc16( struct uart_RAM *pUartRam, int value );

/* standard 8bit uart ungetc */
EXTERN_C int UART_ungetc( struct uart_RAM *pUartRam, int value );

/* get a 16bit value from uart (used by DEBUG uart) */
EXTERN_C int UART_getch16( struct uart_RAM *pUartRam, int timeout );

/* get an 8bit value from uart */
EXTERN_C int UART_getch( struct uart_RAM *pUartRam, int timeout );
