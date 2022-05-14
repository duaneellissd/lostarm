#if !defined(CORE_DEBUG_IO_PORT_H)
#define CORE_DEBUG_IO_PORT_H "14d38d60-0299-42f4-afda-3a7139a1fe17"


/* @file debug_io_port.h
   @brief Bare minimum IO support for debug input/output.

   Details

   These items must be written specifically for the target platform.
   Generally, these write bytes to, or read bytes from the DEBUG UART.

   * NOTE: DEBUG circular buffer for RX is always a 16bit buffer
   * BUT - Tx Buffer is always a 8bit buffer 

   Generally, we assume 115200 baud, 8Bits, No Parity
*/

#include "lostarm/lostarm.h"
#include "lostarm/debug/debug_structs.h"

EXTERN_C struct debug_context DEBUG_CONTEXT;

/* initialize the debug uart/console at this baudrate, using 8bits, no parity, 1 stopbit */
void DEBUG_por_init( uintptr_t hwspecific, int baudrate );

/* the debug pollrx calls this to provide bytes */
void DEBUG_rxDMA_Start( struct debug_context *pCtx, uint16_t **ppbuf, size_t *nSpace );
void DEBUG_rxDMA_Complete( struct debug_context *pCtx, size_t actual );

void DEBUG_txDMA_Start( struct debug_context *pCtx, uint8_t **ppBuf, size_t *nAvail );
void DEBUG_txDMA_Complete(struct debug_context *pCtx, size_t actual );


#endif
