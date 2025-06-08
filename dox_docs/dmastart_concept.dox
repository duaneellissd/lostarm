/**
 *  @file 
 *  @brief What are these DMA functions for and how Can I use them?
 *  @anchor concept_dmastart
 *
 * Many functions, classes and objects have sometype of a "DmaStart()"
 * along with a DmaComplete() function in a paired style.
 *
 * The exact name may vary, ie: DmaTxStart() or DmaRemoveStart(), the
 * added word in the center should make sense based upon the context,
 * ie: Given a circular buffer a Remove function would indicate the
 * purpose is to remove data from the circular bufffer where as
 * a DmaInsertStart() would indicate inserting data into the buffer.
 *
 * # What is DMA, and what is the goal (hint: it is ZERO Copy)
 *
 * # What is ZERO COPY
 * 
 * ZERO copy is the holy grail of data movement, why copy the data if
 * you do not have to copy the data.
 *
 * Imageing the 7 layer ISO Network model, and imagine the software
 * stack that manages that interface.  As the data crosses each layer
 * in that model the data might need to (or is exacty that) be copied
 * from one memory buffer to another memory buffer
 *
 * For example in an ethernet interface, the hardware wants to insert
 * the rx packet with the Ethernet Header prefixed to the rest of the
 * data.  The DMA might have special requirements (type of memory
 * being used, CPU cache etc)
 *
 * The next layer up, wants to remove the ETHERNET MAC addresses so it
 * copies it Each layer copies again, eventually it reaches the
 * application and it is copied in
 *
 * But, what if you could minimize that copying of data - and copy it
 * exactly zero times - if you can you have reached the holy grail of
 * ZERO COPY
 *
 * These functions are an attempt to help makethat actually happen.
 *
 * # Handling the start Case
 *
 * Consider a UART recieving data or transmitting data.  
 *
 * <B>Source of Confusion:</b> Often modern UARTS have a harware fifo of 16
 * bytes or so, a long time ago, they had no FIFO hardware
 *
 * Often all UARTS have a software circular buffer in CPU RAM space
 * that is much larger then the hardware fifo - but it is still often
 * called a FIFO by software types
 *
 * Thus there are really two different FIFOs (4 if you count tx and
 * rx) There is the TX HW FIFO, the TX SW FIFO, the RX HW FIFO and the
 * RX SW FIFO.
 *
 * This totally confuses our "hardware engineer friends" who Don't
 * undertand there are two types of fifos - one in the hardware but
 * there is also one in the software that we can make as large as we
 * desire. (ie: Often it might be 128 or 256 bytes)
 *
 * Besure to keep this in your mind as you read this document.
 *
 * # Goal - Can we point the HW DMA at the SW FIFO Buffer? 
 *
 * Why of course we can! 
 *
 * That is why this exists:
 *
 * NOTE (1): The below generally uses a UART, with DMA and without DMA
 * to transmit data.  from a circular buffer. The same basic concept
 * works with LINEAR buffers and and various other types of modules
 *
 * The RX side is simular but the function names are corrispondingly
 * different Ie: Remove becomes Insert, etc
 *
 * NOTE (2): While the functions says DMA - and the intent is you can
 * use the DMA to do this that does not mean or require that you use
 * DMA, the same functions and API can be used when preforming
 * "software dma like operations"
 *
 *  ~~~~~~~~~~~~~~~~~~{.c}
 *  EXTERN_C CIRC_BUF_DmaRemoveStart( struct circ_buffer *pBuf, void **vpp, size_t *ppnAvail );
 *  ~~~~~~~~~~~~~~~~~~
 *
 * The above gives you a pointer to the fifo memory buffer at the next
 * byte to transmit (to transmit, we would be removing from the fifo
 * memory buffer) and we would need to know how many bytes we can
 * remove.
 *
 * OPTION 1: Configure the DMA to read directly from the buffer
 *
 * OPTION 2: You can read the data your self and for example fill the
 * HW fifo in the TX side of the UART
 *
 * # Handling Completion.
 *
 * Option 1: (Using the DMA) the DMA reads (or writes) the data
 * directly to/from the TX/RX fifo memory buffer eventually there is
 * an Interrupt from the DMA controller (nActual = number of bytes
 * processed by the DMA)
 *
 * Option 2: Using software - the TX 16byte hardware fifo is full, so
 * nActual = 16 (or something less)
 *
 * In both cases, call this function to complete the process
 *
 * ~~~~~~~~~~~~~~~~~~~{.c}
 * EXTERN_C CIRC_BUF_DmaRemoveComplete( struct circ_buffer *pBuf, size_t nActual );
 * ~~~~~~~~~~~~~~~~~~~
 *
 * The above advances the circular buffer forward by nActual Bytes
 *
 * # Don't circualr buffers wrap? How is that handled
 *
 * You simply call the Circular Buffer code 2 times
 * 
 * Step 1: Call DMA START, this gives you the pointer to the data and
 * the length
 *  
 * If the buffer is not wrapped, the nAvail will be all of the
 * available bytes If the buffer is wrapped, the nAvail will be up
 * until the end of the buffer.
 *
 *
 * Step 2: When the DMA is complete, you call:
 *
 * ~~~~~~~~~~~~~~~~~~{.c}
 * EXTERN_C CIRC_BUF_DmaRemoveCmplete( struct circ_buffer *pBuf, size_t nActual );
 * ~~~~~~~~~~~~~~~~~~
 *
 * But this time you provide the number of actual bytes transfered.
 * the internal read/write pointers into the circular buffer will be
 * adjusted In this explination, it will "wrap" to the start.
 * 
 * Step 3: Call CIRC_BUF_DmaRemoveStart() the second time
 *
 * The pointer you receive will be at the start of the buffer
 *
 * Again, in the transmit case if "nAvail == 0" then there are no more
 * bytes to transfer
 *
 * Step 4: Call CIRC_BUF_DmaRemoveComplete() for the next update
 */
