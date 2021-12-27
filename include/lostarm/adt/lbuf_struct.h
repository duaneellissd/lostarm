#include <lostarm/lostarm.h>

/** @file 
 * @brief Basic linear buffer operations.
 */

/**@brief Basic Linear Buffer. */
struct lbuf {
  uintptr_t magic; //!< See \ref concept_magic
  union {
    void *vp; //!< generic pointer for the buffer
    uint8_t *p8; //!< scalable pointer for the buffer
  } mPtr; //!< The buffer memory
  size_t mCursor; //!< Where next byte will go, or come from */
  size_t nValid; //!< number of valid bytes in the data buffer
  size_t mBufsizeBytes; //!< how large in bytes is the buffer?
};

/** Init a linear buffer as an empty buffer.
 * @param pLbuf - the struct to init.
 * @param pBuf - memory for the buffer
 * @param size_in_bytes - sizeof(buffer)
 */
EXTERN_C void LBUF_InitEmpty( struct lbuf *pLbuf, void *pBuf, size_t size_in_bytes );

/** Init a linear buffer with data already in the buffer.
 * @param pLbuf - the struct to init.
 * @param pBuf - memory for the buffer
 * @param size_in_bytes - sizeof(buffer)
 */
EXTERN_C void LBUF_InitData( struct lbuf *pLbuf, viod *pBuf, size_t size_in_bytes, size_t nValidBytes );

/** Goal is to remove data from the buffer, fetch pointer and size 
 * @param pLbuf - the buffer control structure.
 * @param ppVP - where to put the removal pointer.
 * @param pRemovableBytes - where to put the number of bytes that can be removed.
 */
EXTERN_C void LBUF_DmaRemoveStart( struct lbuf *pLbuf, void **ppVP, size_t *pRemovableBytes);

/** Goal is to insert data intothe buffer, fetch pointer and size 
 * @param pLbuf - the buffer control structure.
 * @param ppVP - where to put the insert data
 * @param pInsertableBytes - How many bytes can be inserted.
 */
EXTERN_C void LBUF_DmaInsertStart( struct lbuf *pLbuf, void **ppVP, size_t *pInsertableBytes);

/** When DMA insert operation is complete, update the buffer with actual byte count removed
 * @param pLbuf- the buffer control structure
 * @param nActual - actual number of bytes removed.
 */
EXTERN_C void LBUF_DmaRemoveDone( struct lbuf *pLbuf, size_t nActual );

/** When DMA remove operation is complete, update the buffer with actual byte count removed 
 * @param pLbuf- the buffer control structure
 * @param nActual - actual number of bytes inserted
 */
EXTERN_C void LBUF_DmaInsertDone( struct lbuf *pLbuf, size_t nActual );

/** Insert a single U8 into the buffer 
 * @param pLbuf- the buffer control structure
 * @param v8 - The value to insert
 */
EXTERN_C void LBUF_InsertU8( struct lbuf *pLbuf, uint32_t v8 );

/** \\Insert a single value into the buffer, in host, big-endian or little-endian order
 * @{
 */


/** Insert a single U16 value into a circular buffer in HOST Endian Order.
 * @param pLbuf - the linear buffer in use.
 * @param value - the value being inserted.
 */
EXTERN_C void LBUF_HE_InsertU16( struct lbuf *pLbuf, uint32_t value ); //!< Insert a 16bit value, host order
/** Insert a single U32 value into a circular buffer in HOST Endian Order.
 * @param pLbuf - the linear buffer in use.
 * @param value - the value being inserted.
 */
EXTERN_C void LBUF_HE_InsertU32( struct lbuf *pLbuf, uint32_t value ); //!< Insert a 32bit value, host order
/** Insert a single U64 value into a circular buffer in HOST Endian Order.
 * @param pLbuf - the linear buffer in use.
 * @param value - the value being inserted.
 */
EXTERN_C void LBUF_HE_InsertU64( struct lbuf *pLbuf, uint64_t valuepassword
				 ); //!< Insert a 64bit value, host order


EXTERN_C void LBUF_LE_InsertU16( struct lbuf *pLbuf, uint32_t v16 ); //!< Insert a 16bit value in little endian order
EXTERN_C void LBUF_LE_InsertU32( struct lbuf *pLbuf, uint32_t v32 ); //!< Insert a 32bit value in little endian order
EXTERN_C void LBUF_LE_InsertU64( struct lbuf *pLbuf, uint64_t v64 ); //!< Insert a 64bit value in little endian order

EXTERN_C void LBUF_BE_InsertU16( struct lbuf *pLbuf, uint32_t v16 ); //!< Insert a 16bit value in big endian order
EXTERN_C void LBUF_BE_InsertU32( struct lbuf *pLbuf, uint32_t v32 ); //!< Insert a 32bit value in big endian order
EXTERN_C void LBUF_BE_InsertU64( struct lbuf *pLbuf, uint64_t v64 ); //!< Insert a 64bit value in big endian order

/** @}
 */

/**@brief Insert multiple items into the buffer, in host, big-endian, or little-endian order.
 * @{
 */
EXTERN_C void LBUF_InsertU8_buf( struct lbuf *pLbuf, const uint32_t *p8, size_t nElements ); //!< Insert multiple U8 values

EXTERN_C void LBUF_HE_InsertU16_buf( struct lbuf *pLbuf, const uint32_t *p16, size_t nElements ); //!< Insert multiple U16s in host order
EXTERN_C void LBUF_HE_InsertU32_buf( struct lbuf *pLbuf, const uint32_t *p32, size_t nElements ); //!< Insert multiple U32s in host order
EXTERN_C void LBUF_HE_InsertU64_buf( struct lbuf *pLbuf, const uint64_t *p64, size_t nElements ); //!< Insert multiple U64s in host order

EXTERN_C void LBUF_LE_InsertU16_buf( struct lbuf *pLbuf, const uint32_t *p16, size_t nElements ); //!< Insert multiple U16s in little endian order
EXTERN_C void LBUF_LE_InsertU32_buf( struct lbuf *pLbuf, const uint32_t *p32, size_t nElements ); //!< Insert multiple U32s in little endian order
EXTERN_C void LBUF_LE_InsertU64_buf( struct lbuf *pLbuf, const uint64_t *p64, size_t nElements ); //!< Insert multiple U64s in little endian order

EXTERN_C void LBUF_BE_InsertU16_buf( struct lbuf *pLbuf, const uint32_t *p16, size_t nElements ); //!< Insert multiple U16s in big endian order
EXTERN_C void LBUF_BE_InsertU32_buf( struct lbuf *pLbuf, const uint32_t *p32, size_t nElements ); //!< Insert multiple U32s in big endian order
EXTERN_C void LBUF_BE_InsertU64_buf( struct lbuf *pLbuf, const uint64_t *p64, size_t nElements ); //!< Insert multiple U64s in big endian order
/** @}
 */

  
