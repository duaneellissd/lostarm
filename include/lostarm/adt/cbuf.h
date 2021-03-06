#if !defined(LOSTARM_ADT_CBUF_H)
#define LOSTARM_ADT_CBUF_H "57cb6ad5-3080-422e-9ce4-501947ada5d8"


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
struct cbuf {
  uintptr_t magic; //!< See \ref concept_magic
  union {
    void *vp; //!< generic pointer for the buffer
    uint8_t *p8; //!< scalable pointer for the buffer
  } mPtr; //!< Buffer for the circular data

  size_t BufSize_InElements; 
  volatile size_t mInsertIndex; //!< Where next insert will go, when inserted
  volatile size_t mRemoveIndex; //!< Where next value will come from when removed
  size_t elem_size; //!< Size of one element int the buffer


  void (*pfn_inserted)( struct cbuf *pThis, size_t n );   /**!< if non-NULL, called when an insert occurs */
  uintptr_t insert_use; //!< For use by insert callback

  void (*pfn_removed)( struct cbuf *pThis, size_t n );   /**!< if non-NULL, called when a remove occurs */
  uintptr_t remove_use; //!< For use by remove callback.

};


/** Initialize a circular buffer.
 * @param pCBuf - control struct to init.
 * @param pBase - pointer to memory buffer
 * @param elementSize - Sizeof(element) in the buffer
 * @param nElements - number of elements in the fifo buffer.
 */
EXTERN_C void CBUF_Init( struct cbuf *pCBuf, void *pBase, size_t elementSize, size_t nElements );

/** Returns number of elements available in the buffer
 * @param pCBuf - the control structure
 * @returns number of elements in the buffer
 */
EXTERN_C size_t CBUF_nDataAvail( const struct cbuf *pCBuf );

/** Returns the space that can be inserted (in elements) 
 * @param pCBuf - the control structure.
 * @returns number of elements (space) available to insert
 */
EXTERN_C size_t CBUF_nSpaceAvial( const struct cbuf *pCBuf );

/* the Unget16 and Remove16 are helpers for the debug getkey function. */
EXTERN_C int CBUF_Unget16( struct cbuf *pCbuf, uint16_t keystroke );
EXTERN_C int CBUF_Remove16( struct cbuf *pCBuf, uint16_t keystroke );

/** Inserts data into the circular buffer
 * @param pCBuf - the control structure
 * @param vpInsertThis - pointer to data to insert.
 * @param nElements - how many to insert.
 * @returns count of actual inserted, 0 = buffer is full.
 */
EXTERN_C size_t CBUF_Insert( struct cbuf *pCBuf, const void *vpInsertThis, size_t nElements, int timeout );

/** Remove data fromt he circular buffer.
 * @param pCBuf - the control structure
 * @param vpPutHere - where to put the data that is/was removed.
 * @param nElements - how many to try to remove
 * @returns count of actual removed
 */
EXTERN_C size_t CBUF_Remove( struct cbuf *pCBuf, void *vpPutHere, size_t nElements, int timeout );

/** RTOS - Obtain an insertion point into a circular buffer, and lock the buffer
 * @param pCBuf - the control structure
 * @param vppInsertBufp - the buffer pointer will go here.
 * @param pNElements - the space (in elements) avaialble will be placed here. 
 *
 * @returns -1 on lock timeout
 * @note: This obtains a lock on the CBUF, you must call DMA_DONE! to unlock.
 */
EXTERN_C int CBUF_DmaInsertStart( struct cbuf *pCBuf, void **vppInsertBufp, size_t *pNElements, int timeout );


/** Obtain an insertion point into a circular buffer 
 * @param pCBuf - the control structure
 * @param vppRemoveBufp - the buffer pointer will go here.
 * @param pNElements - the space avaialble will be placed here.
 * @param timeout - in milliseconds for the lock operation.
 * @returns -1 on lock timeout
 * @note: This obtains a lock on the CBUF, you must call DMA_DONE! to unlock.
 */
EXTERN_C void CBUF_DmaRemoveStart( struct cbuf *pCBuf, void **vppRemoveBufp, size_t *pNElements, int timeout);


/** Complete a DMA Insert into the buffer
 * @param pCBuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 */
EXTERN_C void CBUF_DmaInsertDone( struct cbuf *pCBuf, size_t nElementsActual );

/** Complete a DMA Removal into the buffer
 * @param pCBuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 */
EXTERN_C void CBUF_DmaRemoveDone( struct cbuf *pCBuf, size_t nElementsActual );


/** Determine how many elements are avaialble in the circular buffer
 * @param pCBuf - the control structure.
 * @returns 0 to n, the number availalbe.
 */
EXTERN_C size_t CBUF_RemoveAvial( const struct cbuf *pCBuf );

/** Determine how many elements can be inserted into the circular buffer
 * @param pCBuf - the control structure.
 * @returns 0 to n, the number spaces available.
 */

EXTERN_C size_t CBUF_InsertAvial( const struct cbuf *pCBuf );

#endif
