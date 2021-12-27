#include <lostarm/lostarm.h>

/** @file 
 * @brief Basic Abstract data type circular (fifo) buffer.
 *
 * NOTE: Using the DMA feature (see: \ref concept_dmastart)
 * may require 2 operations to insert all of your data.
 *
 * Consider the case where the data in the buffer is wrapped The first
 * call (aka:DMA START) provides a pointer to the space at the end of
 * the buffer, then DMA_Complete - moves and wraps the pointer to the
 * start of the circular buffer. The second call to DMA START provides
 * the pointer to the staring of the buffer.
 */

/** @brief Basic ADT for circular buffer
 */
struct cbuf {
  uintptr_t magic; //!< See \ref concept_magic
  union {
    void *vp; //!< generic pointer for the buffer
    uint8_t *p8; //!< scalable pointer for the buffer
  } mPtr; //!< Buffer for the circular data

  size_t nBufSize_InBytes; //!< sizeof(buffer)
  size_t mWrIndex; //!< Where next insert will go, when inserted
  size_t mRdIndex; //!< Where next value will come from when removed
  size_t elem_size; //!< Size of one element int the buffer

};

/** @brief an rtos aware Circular buffer */
struct rtos_cbuf {
  struct cbuf cbuf; //!< Core/common circular buffer
  uintptr_t os_Mutex; //!< used by WrLock/WrUnlock, assumed to be a \ref concept_rtos object
  uintptr_t os_WaitSemaphore; //<! something a thread can wait on.
};

/** Initialize a circular buffer.
 * @param pCBuf - control struct to init.
 * @param pBase - pointer to memory buffer
 * @param elementSize - Sizeof(element) in the buffer
 * @param nElements - number of elements in the fifo buffer.
 */
EXTERN_C void CBUF_Init( struct cbuf *pCBuf, void *pBase, size_t elementSize, size_t nElements );

/** Initilize a circular buffer with RTOS (locks,etc)
 * @param pCBuf - control struct to init.
 * @param mutex_name - if null no mutex is obtained
 * @param sem_name - if null no semaphore is obtained
 * @param pBase - pointer to memory buffer
 * @param elementSize - Sizeof(element) in the buffer
 * @param nElements - number of elements in the fifo buffer.
 */
EXTERN_C void RTOS_CBUF_Init( struct rtos_cbuf *pCBuf, const char *mutex_name, const char *sem_name, void *pBase, size_t elementSize, size_t nElements, int  );

/** Lock the rtos, returns -1 on timeout
 * @param pCBuf - control structure
 * @param timeout - in milliseconds.
 * @returns -1 on error, 0 success
 */
EXTERN_C int RTOS_CBUF_Lock( struct rtos_cbuf *pCBuf, int timeout );
/** Unlock the circular buffer
 * @param pCBuf - the control structure
 */
EXTERN_C void RTOS_CBUF_UnLock( struct rtos_cbuf *pCBuf );

/** Returns number of elements available in the buffer
 * @param pCBuf - the control structure
 * @returns number of elements in the buffer
 */
EXTERN_C size_t CBUF_nDataAvial( const struct cbuf *pCBuf );
/** Returns the space that can be inserted (in elements) 
 * @param pCBuf - the control structure.
 * @returns number of elements (space) available to insert
 */
EXTERN_C size_t CBUF_nSpaceAvial( const struct cbuf *pCBuf );

/** Inserts data into the circular buffer
 * @param pCBuf - the control structure
 * @param vpInsertThis - pointer to data to insert.
 * @param nElements - how many to insert.
 * @returns count of actual inserted
 */
EXTERN_C size_t CBUF_Insert( struct cbuf *pCBuf, const void *vpInsertThis, size_t nElements );

/** Remove data fromt he circular buffer.
 * @param pCBuf - the control structure
 * @param vpPutHere - where to put the data that is/was removed.
 * @param nElements - how many to try to remove
 * @returns count of actual removed
 */
EXTERN_C size_t CBUF_Remove( struct cbuf *pCBuf, void *vpPutHere, size_t nElements );

/** Obtain an insertion point into a circular buffer
 * @param pCBuf - the control structure
 * @param vppInsertBufp - the buffer pointer will go here.
 * @param pNElements - the space avaialble will be placed here.
 */
EXTERN_C void CBUF_DmaInsertStart( struct cbuf *pCBuf, void **vppInsertBufp, size_t *pNElements );

/** RTOS - Obtain an insertion point into a circular buffer, and lock the buffer
 * @param pCBuf - the control structure
 * @param vppInsertBufp - the buffer pointer will go here.
 * @param pNElements - the space avaialble will be placed here. 
 * @param timeout - in milliseconds for the lock
 *
 * @returns -1 on lock timeout
 * @note: This obtains a lock on the CBUF, you must call DMA_DONE! to unlock.
 */
EXTERN_C int RTOS_CBUF_DmaInsertStart( struct rtos_cbuf *pCBuf, void **vppInsertBufp, size_t *pNElements, int timeout );


/** Obtain an insertion point into a circular buffer
 * @param pCBuf - the control structure
 * @param vppRemoveBufp - the buffer pointer will go here.
 * @param pNElements - the space avaialble will be placed here.
 */
EXTERN_C void CBUF_DmaRemoveStart( struct cbuf *pCBuf, void **vppRemoveBufp, size_t *pNElements );

/** RTOS Obtain an insertion point into a circular buffer 
 * @param pCBuf - the control structure
 * @param vppRemoveBufp - the buffer pointer will go here.
 * @param pNElements - the space avaialble will be placed here.
 * @param timeout - in milliseconds for the lock operation.
 * @returns -1 on lock timeout
 * @note: This obtains a lock on the CBUF, you must call DMA_DONE! to unlock.
 */
EXTERN_C void RTOS_CBUF_DmaRemoveStart( struct cbuf *pCBuf, void **vppRemoveBufp, size_t *pNElements, int timeout);


/** Complete a DMA Insert into the buffer
 * @param pCBuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 */
EXTERN_C void CBUF_DmaInsertDone( struct cbuf *pCBuf, size_t nElementsActual );

/** RTOS Complete a DMA Insert into the buffer
 * @param pCBuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 *
 * @note: This releases the lock on the circular buffer and "produces" to the semaphore if defined.
 */
EXTERN_C void RTOS_CBUF_DmaInsertDone( struct rtos_cbuf *pCBuf, size_t nElementsActual );

/** Complete a DMA Removal into the buffer
 * @param pCBuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 */
EXTERN_C void CBUF_DmaRemoveDone( struct cbuf *pCBuf, size_t nElementsActual );

/** RTOS Complete a DMA Removal into the buffer
 * @param pCBuf - the control structure
 * @param nElementsActual - number of actually inserted elementsl
 * @note: This releases the lock on the circular buffer and "produces" to the semaphore if defined.
 */
EXTERN_C void RTOS_CBUF_DmaRemoveDone( struct rtos_cbuf *pCBuf, size_t nElementsActual );

/** Determine how many elements are avaialble in the circular buffer
 * @param pCBuf - the control structure.
 * @returns 0 to n, the number availalbe.
 */
EXTERN_C size_t CBUF_RemoveAvial( const struct cbuf *pCBuf );

/** RTOS varient, Determine how many elements can be inserted into the circular buffer
 * @param pCBuf - the control structure.
 * @returns 0 to n, the number spaces available.
 */

EXTERN_C size_t RTOS_CBUF_InsertAvial( const struct cbuf *pCBuf );

/** RTOS varient, Determine how many elements can be removed from the circular buffer
 * @param pCBuf - the control structure.
 * @returns 0 to n, the number of elements available.
 */
EXTERN_C size_t RTOS_CBUF_RemoveAvial( const struct rtos_cbuf *pCBuf );
