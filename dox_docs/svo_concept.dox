/**
 *  @file 
 *  @brief SVO - Subject Verb Object Order, and verb choices
 *  @anchor concept_svo
 *
 *
 * # In general, functions follow this naming convention:
 *
 *      AREA_verbAction()
 *
 * Where AREA (all caps) is effectively a major component or class.
 *
 * Examples include DEBUG_, or UART_, or SPI_, etc.
 *
 *
 * # What is SVO?
 *
 * Wiki Article:  https://en.wikipedia.org/wiki/Subject–object–verb_word_order
 *
 * In the english language we say:  "The RED Dress"
 * However in French, it is "La robe Rouge"
 * (robe = Dress, Rouge = Red)
 *
 * Other examples are:  I eat the apple, verses The Apple is eaten by me
 * Both mean the same thing - but for consistancy we choose 1.
 *
 * # Approved Verbs & Directional Words & Verbs
 *
 * * Hint: Posix rules where possible.
 *
 * * How many ways can you write(spell) a transmit function:
 *
 *    UART_txBytes(), UART_tx_Bytes(), UART_tx_bytes()
 *    UART_send(), UART_xmit(), UART_sendBytes()
 *    UART_transmit()
 *
 * To be consistant, we choose the UNIX UDP function names: UART_send()
 * and UART_recv() over any other.
 *
 * There are exceptions, for example if the technology has a well known
 * and widely used terms - we use that technology specific term.
 * ie: USB "in-packet"  or SPI "mosi-data"
 *
 * * Directional Words
 *
 * What word do we use to describe the direction?
 *
 * Do we SEND, or TRANSMIT, or XMIT, or TX, or PUT, or Write?
 *  Is this the TX data from the other side?
 *  Or is this the RX Data we received?
 *
 * Our rule: The point of reference is always our self unless technology specifies otherwise.
 * ie: The USB OUT-PACKET is very specific.
 *
 * * List of Verbs (paired)
 *
 *  -  get/set - always a pair
 *  -  send/recv - alway a pair
 *  -  open, close - always a pair.
 *
 *  - Oddball things, are handled via an IOCTL() call.
 *    Note: Common things for a device class should be promoted up out of IOCTL nonsense.
 */
