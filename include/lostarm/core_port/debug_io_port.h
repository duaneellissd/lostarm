#if !defined(CORE_DEBUG_IO_PORT_H)
#define CORE_DEBUG_IO_PORT_H

/* @file debug_io_port.h
   @brief Bare minimum IO support for debug input/output.

   Details

   These items must be written specifically for the target platform.
   Generally, these write bytes to, or read bytes from the DEBUG UART.

   Generally, we assume 115200 baud, 8Bits, No Parity
*/

#include "lostarm/lostarm.h"

struct DebugIoPortRam;
struct DebugIoPortRom;

/**
 * \brief This is the read only portion of the DEBUG runtime variables.
 * Also see \ref concept_ramrom
 */
struct DebugIoPortROM {

#define DEBUGIO_MAGIC  _ascii_magic( 'D', 'B', 'I', 'O', 'P', 'O', 'R', 'T' )
  uintptr_t magic; ///< See \ref concept_magic

  struct uart_rom *pUart_ROM; ///< The uart ROM for the underlying uart
  struct DebugIoPortRAM *pRAM; ///< ram for the debug interface
};

/* initialize the debug uart/console at this baudrate, using 8bits, no parity, 1 stopbit */
void DEBUG_por_init( uintptr_t hwspecific, int baudrate );

/* the debug pollrx calls this to provide bytes */
void DEBUG_handle_rxbuf( struct DebugIoPortRam *pRamThis, uint8_t *pbuf, size_t nbytes );

void DEBUG_txDMA_Start( struct DebugIoPortRam *pRamThis, uint8_t **ppBuf, size_t *pNBytes );
void DEBUG_txDMA_Complete(struct DebugIoPortRam *pRamThis, size_t actual );


#endif
