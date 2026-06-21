#if !defined(LOSTARM_BUFFERS_LINEAR_BUFFER_H)
#define LOSTARM_BUFFERS_LINEAR_BUFFER_H

/*
 * This describes a linear_buffer which is exactly an array of bytes.
 */

struct linear_buffer {
  // used for error checks.
  uintptr_t mMagic;
  // How big is the underlying buffer
  size_t capacity;
  // How many bytes are in the underlying buffer
  size_t nValid;
  // Where does next byte go into that buffer?
  size_t cursor;
  // Have we overrun the buffer?
  int    isError;
  // Data buffer it self.
  uint8_t *pBuffer;
};

#define LBUF_MAGIC ((uintptr_t)(&LBUF_InitEmpty))

EXTERN_C LBUF_InitEmpty( struct linear_buffer *pBuffer, uint8_t *pBuffer, size_t capacity );
EXTERN_C LBUF_InitWithData(struct linear_buffer *pBuffer, uint8_t *pBuffer, size_t capacity, size_t nvalid );

#endif
