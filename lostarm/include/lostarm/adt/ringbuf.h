#if !defined(LOSTARM_ADT_CBUF_H)
#define LOSTARM_ADT_RINGBUF_H "57cb6ad5-3080-422e-9ce4-501947ada5d8"


#include <lostarm/lostarm.h>

/** @file 
 * @brief Basic Abstract data type circular (fifo) buffer.
 *
 * NOTE: Assumed knowledge: (see: \ref concept_dmastart)
 *
 * Assumptions:
 *   There can be many tasks sending (inserting) data.
 *   There is a single task reading (removing) data.
 *
 * NOTE:
 *   These function locks IRQs at the CPU during updates.
 */

/** @brief Basic ADT for circular buffer
 */
struct ringbuf {
  uintptr_t magic; //!< See \ref concept_magic
  union {
    void *vp; //!< generic pointer for the buffer
    uint8_t *p8; //!< scalable pointer for the buffer
  } mPtr; //!< Buffer for the circular data

  size_t BufSize_InElements; 
  volatile size_t mInsertIndex; //!< Where next insert will go, when inserted
  volatile size_t mRemoveIndex; //!< Where next value will come from when removed
  size_t elem_size; //!< Size of one element int the buffer


  void (*pfn_inserted)( struct ringbuf *pThis, size_t n );   /**!< if non-NULL, called when an insert occurs */
  uintptr_t insert_use; //!< For use by insert callback

  void (*pfn_removed)( struct ringbuf *pThis, size_t n );   /**!< if non-NULL, called when a remove occurs */
  uintptr_t remove_use; //!< For use by remove callback.

};

struct ringbuf_init {
  struct ringbuf *pInitThis;
  uint8_t *pBuffer;
  size_t  sizeof_pBuffer_in_bytes;
  size_t  elementy_size_in_bytes;
};


/** Initialize a circular buffer.
 * @param pRingbuf - control struct to init.
 * @param pBase - pointer to memory buffer
 * @param elementSize - Sizeof(element) in the buffer
 * @param nElements - number of elements in the fifo buffer.
 */
EXTERN_C void RINGBUF_Init( struct ringbuf *pRingbuf, void *pBase, size_t elementSize, size_t nElements );

/** Returns number of elements available in the buffer
 * @param pRingbuf - the control structure
 * @returns number of elements in the buffer
 */
EXTERN_C size_t RINGBUF_nDataAvail( const struct ringbuf *pRingbuf );

/** Returns the space that can be inserted (in elements) 
 * @param pRingbuf - the control structure.
 * @returns number of elements (space) available to insert
 */
EXTERN_C size_t RINGBUF_nSpaceAvial( const struct ringbuf *pRingbuf );

/* the Unget16 and Remove16 are helpers for the debug getkey function. */
EXTERN_C int RINGBUF_Unget16( struct ringbuf *pRingbuf, uint16_t keystroke );
EXTERN_C int RINGBUF_Remove16( struct ringbuf *pRingbuf, uint16_t keystroke );

/** Inserts data into the circular buffer
 * @param pRingbuf - the control structure
 * @param vpInsertThis - pointer to data to insert.
 * @param nElements - how many to insert.
 * @returns count of actual inserted, 0 = buffer is full.
 */
EXTERN_C size_t RINGBUF_Insert( struct ringbuf *pRingbuf, const void *vpInsertThis, size_t nElements, int timeout );

/** Remove data fromt he circular buffer.
 * @param pRingbuf - the control structure
 * @param vpPutHere - where to put the data that is/was removed.
 * @param nElements - how many to try to remove
 * @returns count of actual removed
 */
EXTERN_C size_t RINGBUF_Remove( struct ringbuf *pRingbuf, void *vpPutHere, size_t nElements, int timeout );

/** RTOS - Obtain an insertion point into a circular buffer, and lock the buffer
 * @param pRingbuf - the control structure
 * @param vppInsertBufp - the buffer pointer will go here.
 * @param pNElements - the space (in elements) avaialble will be placed here. 
 *
 * @returns -1 on lock timeout
 * @note: This obtains a lock on the RINGBUF, you must call DMA_DONE! to unlock.
 */
EXTERN_C int RINGBUF_DmaInsertStart( struct ringbuf *pRingbuf, void **vppInsertBufp, size_t *pNElements, int timeout );


/** Obtain an insertion point into a circular buffer 
 * @param pRingbuf - the control structure
 * @param vppRemoveBufp - the buffer pointer will go here.
 * @param pNElements - the space avaialble will be placed here.
 * @param timeout - in milliseconds for the lock operation.
 * @returns -1 on lock timeout
 * @note: This obtains a lock on the RINGBUF, you must call DMA_DONE! to unlock.
 */
EXTERN_C void RINGBUF_DmaRemoveStart( struct ringbuf *pRingbuf, void **vppRemoveBufp, size_t *pNElements, int timeout);


/** Complete a DMA Insert into the buffer
 * @param pRingbuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 */
EXTERN_C void RINGBUF_DmaInsertDone( struct ringbuf *pRingbuf, size_t nElementsActual );

/** Complete a DMA Removal into the buffer
 * @param pRingbuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 */
EXTERN_C void RINGBUF_DmaRemoveDone( struct ringbuf *pRingbuf, size_t nElementsActual );


/** Determine how many elements are avaialble in the circular buffer
 * @param pRingbuf - the control structure.
 * @returns 0 to n, the number availalbe.
 */
EXTERN_C size_t RINGBUF_RemoveAvial( const struct ringbuf *pRingbuf );

/** Determine how many elements can be inserted into the circular buffer
 * @param pRingbuf - the control structure.
 * @returns 0 to n, the number spaces available.
 */

EXTERN_C size_t RINGBUF_InsertAvial( const struct ringbuf *pRingbuf );

#endif
