#if !defined(LOSTARM_UART_STRUCTS_H)
#define LOSTARM_UART_STRUCTS_H "c107e554-6901-4ce2-9b6f-25d789e504e7"


struct uart_RAM {
  const struct uart_ROM *pROM;
  /* for socket, this is the socket
   * for ble - the handle
   * for usb - the usb device pointer
   * or what ever bottom layer wants/needs.
   */
  uintptr_t hw_connection;
};

struct uart_HW {
  const char *pName;
  int plat_irqid;
  uintptr_t baseaddress;
  int hw_type;
  /* first 10 are "virtual uarts" */
#define UART_HWTYPE_usbdevice     1 /* host=PC(linux/windows/mac), we=device */
#define UART_HWTYPE_usbhost       2 /* we=host, device=ftdi like chip */
#define UART_HWTYPE_usb_hidtunnel 3 /* we=usb hid device, host=Windows */
#define UART_HWTYPE_bleuart       4
#define UART_HWTYPE_socket        5
#define UART_HWTYPE_udp_uart      6
  
#define UART_HWTYPE_stm32        10
#define UART_HWTYPE_xilinx_ps7   11
#define UART_HWTYPE_ti_cc        12
#define UART_HWTYPE_ti_tiva      13
#define UART_HWTYPE_esp32        14
  /* add more here */
  uintptr_t hw_cookie;
};

struct uart_ROM {
  const struct uart_HW *pHW;
  struct uart_RAM *pRAM;
  struct cbuf *pTxCBuf;
  struct cbuf *pRxCBuf;
};


/** @struct uart_CFG
 *
 * Defines a UART configuration
 *
 * For Even parity, specify the the ascii letter 'E'
 * For fractional stop bits, ie: 1.5, use 15 (ie: x10)
 *
 * NOTE:
 *   Some chips (8051, mode 2) supports a 9bit uart.
 *   Commonly found on 8051s, also known as 9bit mode
 *
 *   This is expressely not well supported here.
 *   Instead, you should create a unique 9bit UART HW Type.
 *
 * If the UART is to communicate be via a Socket
 * Then the open process will create a socket
 *
 * NOTE: newtwork item are BIG ENDIAN (ie: BE)
 * If not using networks, these fields are ignored
 */

struct uart_CFG {
  int baudrate;
  int parityLetter; /**< ascii: N, E, O, 1, 0 */
  int nbits; /**< typically 5 to 8, actual depends on HW */
  int x10_stopbits; /**< 1, 2 or 10, 15 or 20 */
  uint32_t ip_txaddress_BE;
  uint16_t ip_txPort_BE;
  
};

#define UART_cfg_8n1(pCFG) \
   do { (pCFG)->parityletter = 'N'; (pCFG)->nbits = 8; (pCFG)->x10_stopbits = 1; } while(0)
#define UART_cfg_8n1p5(pCFG) /* 1.5 stop bits */ \
   do { (pCFG)->parityletter = 'N'; (pCFG)->nbits = 8; (pCFG)->x10_stopbits = 15; } while(0)

#endif
