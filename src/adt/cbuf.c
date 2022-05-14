#include <lostarm/lostarm.h>
#include <lostarm/debug.h>
#include <lostarm/adt/cbuf.h>
#include <lostarm/wrapped/_string.h>

void CBUF_Init( struct cbuf *pCbuf, void *pBase, size_t elementSize, size_t nElements )
{
  memset( (void *)(pCbuf), 0, sizeof(*pCbuf) );

  pCbuf->magic = (uintptr_t)(&CBUF_Init);
  pCbuf->mPtr.vp = pBase;
  pCbuf->mInsertIndex = 1;
  pCbuf->mRemoveIndex = 0;
  pCbuf->elem_size = elementSize;
  pCbuf->BufSize_InElements = nElements;
}

size_t CBUF_nDataAvail( const struct cbuf *pCbuf )
{
  size_t result;
  uintptr_t tmp;

  tmp = CPU_irq_disable();

  result = (pCbuf->mInsertIndex + pCbuf->BufSize_InElements - pCbuf->mRemoveIndex) % pCbuf->BufSize_InElements;

  CPU_irq_restore(tmp);

  DEBUG_ASSERT1( pCbuf->elem_size != 0 );
  result = result / pCbuf->elem_size;

  return result;
}

size_t CBUF_nSpaceAvial( const struct cbuf *pCbuf )
{
  size_t result;
  uintptr_t tmp;

  tmp = CPU_irq_disable();

  result = (pCbuf->mInsertIndex + pCbuf->BufSize_InElements - pCbuf->mRemoveIndex) % pCbuf->BufSize_InElements;

  CPU_irq_restore(tmp);

  result = pCbuf->BufSize_InElements - result;

  result = result / pCbuf->elem_size;

  return result;
}


size_t CBUF_Insert( struct cbuf *pCbuf, const void *vpInsertThis, size_t nElements, int timeout )
{
  void *pPutHere;
  size_t space;
  size_t nbytes;
  size_t actual;
  int pass;

  actual = 0;

  for( pass = 0 ; (pass < 2) && (nElements > 0) ; pass++ ){
    CBUF_DmaInsertStart( pCbuf, &pPutHere, &space, timeout );
    if( space == 0 ){
      break;
    }

    if( space > nElements ){
      space = nElements;
    }

    nbytes = space * pCbuf->elem_size;
    memcpy( pPutHere, vpInsertThis, nbytes );
    CBUF_DmaInsertDone( pCbuf, space );
    actual += space;
    nElements -= space;
    vpInsertThis = ((void *)(  ((uint8_t *)(vpInsertThis)) + nbytes ));
  }

  return actual;
}

void CBUF_DmaRemoveDone( struct cbuf *pCbuf, size_t nActual )
{
  uintptr_t tmp;
  size_t newidx;

  tmp = CPU_irq_disable();

  newidx = pCbuf->mRemoveIndex + nActual;
  if( newidx > pCbuf->BufSize_InElements ){
    newidx -= pCbuf->BufSize_InElements;
  }

  CPU_irq_restore(tmp);

  if( pCbuf->pfn_removed ){
    (*(pCbuf->pfn_removed))( pCbuf, nActual );
  }
}

size_t CBUF_Remove( struct cbuf *pCbuf, void *puthere, size_t nElements, int timeout )
{
  int pass;
  size_t actual;
  size_t nAvial;
  size_t nbytes;
  void *pData;

  actual = 0;
  for( pass = 0 ; (pass < 2) && (nElements > 0) ; pass++ ){

    CBUF_DmaRemoveStart( pCbuf, &pData, &nAvial, timeout );

    if( nAvial == 0 ){
      break;
    }

    if( nAvial > nElements ){
      nAvial = nElements;
    }

    nbytes = (size_t)(nAvial * pCbuf->elem_size);
    memcpy( puthere, pData, nbytes );

    /* update circular buffer */
    CBUF_DmaRemoveDone( pCbuf, nAvial );
    
    puthere = ((void *)(  ((uint8_t *)(puthere)) + nbytes ));
    nElements -= nAvial;
    actual += nAvial;
  }
  return actual;
}

void CBUF_DmaInsertDone( struct cbuf *pCbuf, size_t nActual )
{
  uintptr_t tmp;
  size_t newidx;

  tmp = CPU_irq_disable();
  newidx = (pCbuf->mInsertIndex + nActual);
  if( newidx >=  pCbuf->BufSize_InElements ){
    newidx = newidx - pCbuf->BufSize_InElements;
  }

  pCbuf->mInsertIndex = newidx;
  CPU_irq_restore(tmp);

  if( pCbuf->pfn_inserted ){
    (*(pCbuf->pfn_inserted))( pCbuf, nActual );
  }
}

int CBUF_DmaInsertStart( struct cbuf *pCbuf, void **ppTakeHere, size_t *pSpace, int timeout )
{
  uintptr_t tmp;
  tmp = CPU_irq_disable();
  *ppTakeHere = (pCbuf->mPtr.p8 + (pCbuf->mInsertIndex * pCbuf->elem_size));
  if( pCbuf->mInsertIndex > pCbuf->mRemoveIndex ){
    *pSpace = pCbuf->BufSize_InElements - pCbuf->mInsertIndex;
  } else {
    *pSpace = pCbuf->mRemoveIndex;
  }
  CPU_irq_restore(tmp);
  return 0;
}

size_t test_In, test_Rn;

static void I_callback( struct cbuf *p, size_t n )
{
  test_In = n;
}

static void R_callback( struct cbuf *p, size_t n )
{
  test_Rn = n;
}
  

void
UNIT_TEST_cbuf(void)
{
  static struct cbuf dut;
  uint16_t dut_buf[10];
  uint16_t data[10];
  int x,y;
  
#define CLEAR_DATA()  memset( data, 0, sizeof(data)); test_Rn =0; test_In=0

  CBUF_Init( &dut, &dut_buf, sizeof(dut_buf[0]), ARRAY_SIZE(dut_buf) );
  dut.pfn_inserted = I_callback;
  dut.pfn_removed  = R_callback;

  CLEAR_DATA();
  for( x = 0 ; x < 11 ; x++ ){
    data[1] = 1234+x;
    y = CBUF_Insert( &dut, &data[1], 1, 0 );
    if( x == 11 ){
      DEBUG_ASSERT1( y == 0 );
      DEBUG_ASSERT1( CBUF_nDataAvail(&dut) == 10 );
    } else {
      DEBUG_ASSERT1( y == 1 );
      DEBUG_ASSERT1( CBUF_nDataAvail(&dut) == 1 );
    }
    
    for( y = 0 ; y < 10 ; y++ ){
      if( y <= x ){
	DEBUG_ASSERT1( dut_buf[y] == (1234+y) );
	DEBUG_ASSERT1( test_In == 1 );
	DEBUG_ASSERT1( test_Rn == 0 );
	test_In = 0;
      }
    
      DEBUG_ASSERT1( CBUF_nSpaceAvial(&dut) == 9 );
  
    }
  }
}

