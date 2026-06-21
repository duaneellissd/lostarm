#if !defined( LOSTARM_RING_BUFFER_H)
#define LOSTARM_RING_BUFFER_H

/*
 * A ring buffer is also known as a FIFO, or circular buffer.
 * Some ring buffer implimentations assume a power of 2 size
 * We do not.
 */

struct ring_buffer {
  uintptr_t mMagic;
  size_t mInsert;
  size_t mRemove;
  size_t mElementSize;
  size_t mBufferSize
  uint8_t *pBuff
};

//
// Initialize a RING Buffer
// Note the ring buffer elements can be any size, 1, 2, bytes anything.
// To simplify the api:
//    you pass the sizeof() the raw buffer
//    you pass the sizeof() a single element.
// 
void RBUF_Init( struct ring_buf *pRbuf, size_t raw_bufsize, void *pBuf, size_t element_size );

void RBUFF_dmaRemove_start( struct ring_buf *pRbuf, void **pData, size_t nElements );
void RBUFF_dmaRemove_complete( struct ring_buf *pRbuf, size_t actual );
