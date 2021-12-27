#include <lostarm/lostarm.h>

struct Uart_ROM;
struct Uart_RAM;


/**
 * \file 
 * @brief Basic UART IO functions.
 *
 * Things in common;
 *
 * All UARTS (tx and rx) have a transmit and receive circular buffer.
 * The core code places (copies) all data throught the circular buffer.
 *
 * There is an accessor function:  UART_txDmaStart(), this function
 * will obtain a pointer to a buffer and a count of bytes to transmit.
 * If this function returns 0 as the count of bytes to transmit there is
 * nothing more to send.
 *
 * Also see: \ref concept_dmastart to understand how the DmaStart functions work
 *
 * To transmit, the UART_CORE code, copies/inserts the data to transmit
 * into the tx circular buffer then - calls the uart specific driver
 * callback that starts the uart transmitting.
 *
 * Case: Normal (non-DEBUG_UART), this function should call UART_txDmaStart()
 * and load up the UART FIFO and enable the TX_IRQ and return.
 * Lastly, this should update the uart circular buffer by calling UART_txDmaComplete()
 * Effectively, the DEBUG UART is always transmit blocking.
 *
 * When the TX_IRQ occurs, the IRQ calls: UART_txDmaStart() to obtain the next
 * buffer, it then can load the UART fifo with more data, and updates
 * the circular buffer by callign UART_txDmaComplete()
 *
 * This process repeats until UART_txDmaStart() indicates 0 bytes to transmit.
 * That is when the TX IRQ would normaly be disabled.
 *
 * To receive: The Nomal UART would use an RX-IRQ, and when the RX IRQ
 * occurs, the Driver should call UART_rxDmaStart() to obtain the
 * pointer into the rx circular buffer and space avaialble.  The
 * driver should fill the avaialble space with what ever data is
 * available.  Then update the uart rx dicrcular buffer by calling
 * UART_rxDmaComplete()
 *
 * If there are still more bytes to receive the driver should call
 * UART_rxDmaStart() a second time to handle the "wrapped buffer"
 * special case and then insert the remaining data into the buffer.
 *
 * If there are still more bytes to receive (3rd attempt) the UART
 * driver should discard all incomming data and flag an OVER RUN error.
 * by calling UART_setOE_ERR()
 * 
 * In the DEBUG UART case, the DEBUG UART normally does not use IRQs
 * instead the DEBUG UART is polled, thus the application will arrange 
 * to have the uart driver rx poll function called sufficently often enough.
 *
 * NOTE: That is not to say the DEBUG UART cannot use the RX IRQ
 *       The DEBUG uart can use the RX IRQ and insert data into the
 *       debug rx circular buffer.
 *       
 * For the Non-Normal uart (the debug uart) which cannot use
 * IRQs for transmit, this is a blocking function and should not
 * return until all bytes in the uart tx circle buffer are transmitted.
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
typedef int fn_dbg_io_txstart( struct UART_RAM *pRamThis );

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

typedef int fn_dbg_io_rxpoll( struct UART_RAM *pRamThis, int timeout);



