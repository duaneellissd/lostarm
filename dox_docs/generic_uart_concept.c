/**
 *  @file 
 *
 *  @anchor concept_generic_uart
 *
 *
 * # Generic UARTS - (interrupt driven)
 *
 * Note: Also see \ref concept_debug_uart for information about debug uarts.
 *
 * There are two parts to the UART driver, the generic part and the HW Specific portion.
 *
 * The GENERIC part handles the RX and TX circular buffers
 * The HW SPECIFIC part handles the actual receipt and transmission of bytes.
 *
 * # Required Hardware functions.
 *
 * * Initialization
 * There must be a function that initializes the UART in some form.
 * For example, baudrate, Parity, n-databits, n-stop bits etc
 * This function would also enable IRQs as needed.
 *
 * * Transmission process
 *
 * The Application layer calls UART_send_buf() to send (transmit).
 *
 * The generic layer copies what it can of that buffer into the TX
 * circular buffer.
 *
 * Next, the generic layer calls the HW SPECIFIC send_start function.
 * The send start function must:
 *    Option A) Block until all bytes are transmitted [debug uart case]
 *    Option B) Begin the interrupt uart transmission process.
 *
 * Often to support IRQ transmission, the UART process is as follows:
 *
 *    Get a pointer to the transmit buffer and the length (number of bytes)
 *    Load the tx fifo with what you can
 *    Update the tx buffer with "n-actual-sent"
 *    Enable the TX IRQ
 *    Wait for the TX IRQ to occur.
 *
 * On TX IRQ
 *    Get a pointer to the (now updated) transmit buffer and length (number of bytes)
 *    load the tx fifo with what you can
 *    Update the tx buffer with n-actual-sent
 *    If there are more bytes to send.. re-enable the TX IRQ
 *    Otherwise possibly disable the TX IRQ
 *
 * For TX DMA based operations:
 *
 * To start:
 *    Get a pointer to the (now updated) transmit buffer and length (number of bytes)
 *    Configure the DMA to point to that buffer and that length
 *    if needed Configure DMA channel to service the UART
 *    Update the tx fifo with n-actually sent
 *    Enable the TX-DMA irq
 *
 * On DMA IRQ:
 *    is generally the same process as the start process
 *
 *    Get pointer to the (now updated) transmit buffer and length (number of bytes)
 *    Update the DMA (same process as start), update the TX FIFO with n-actually sent
 *    re-enable the TX DMA - or if it is done, disable the TX-DMA
 *
 *
 * * Reception Process
 *
 * Polled Mode:
 *
 *   - Get a pointer to the RX circular buffer and availabe space in the buffer.
 *   - In a loop, read the UART status - if no data - break.
 *   - Read dat byte, and add to the circular buffer
 *   - When done, update the RX circular buffer FIFO counts
 *
 * Important functions the hardware driver should use:
 *
 * void UART_driver_tx_dmaStart( struct uart_RAM *pUart, void **pBuffer, size_t *nAvailable );
 * void UART_driver_tx_dmaComplete( struct uart_RAM *pUart, size_t n_actual );
 * 
 * void UART_driver_rx_dmaStart( struct uart_RAM *pUart, void **pBuffer, size_t *nSpaceAvailabe );
 * void UART_driver_rx_dmaComplete( struct uart_RAM *pUart, size_t n_actual );
 *
 */

