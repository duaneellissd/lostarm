# What is ZeroCopy? and What are these DMA functions?

The hope is to provide a reasonably fast way of accessing a buffer.

One could call - in a loop call:

```
    for( x = 0 ; x < 100 ; x++ ){
    	 // Lots of overhead for 100 calls
	 RBUF_insert_u8( pLBUF, buffer[x] );
    }
```
OR - one could do this:
```
   int nDone = 0;
   while( nDone < 100 ){
	RBUF_DMA_insertStart( pLBUF, &vp, &count );
	if( count == 0 ){
	    // Done - Full
	    break;
	}

	memcpy( vp, buffer, count );
	nDone = nDone + count;
	// loop for more.
   }
```


Sometimes you want to use a DMA to transfer the data.  To use a DMA
one needs a raw pointer into the guts of the ring buffer.

That is the purpose of the DMA functions.

The in general the process is as follows:

    - Step 1: call: DMA_insertStart() or DMA_removeStart()
    - Step 2: Perform what ever IO you need on the buffer.
    - Step 3: When the transfer is complete call (ie: your DMA IRQ)
    - Step 4: The DMA_insertComplete(), or DMA_removeComplete()

For the LINEAR BUFFER (LBUF) - thats all there is to it.

For the RING (circular) buffer, you must deal with a wrapped buffer.
You must effectively, 'loop' over the buffer. Why?  Recall that the
data space in a circular buffer might: 'wrap around' - thus the first
call gets the buffer at the end of the physical buffer, the second
call gets the wrapped buffer at the start.

More interestingly - some DMAs support a "scatter/gather mode".  The
concept is: Step 1 - you configure the first DMA transfer which
handles the "end of the ring buffer" - then if need you can configure
a Step 2 - Second DMA transfer that handles the portion that has
wrapped around. To accomplish this, you the calls are as follows:

```
	DMA_removeStart(pBUF, &vp1, &pass1_bytes );
	// Configure the first DMA transfer
	
	DMA_removeStart2( pBUF, &vp2, &pass2_bytes, pass1_bytes );
	// Configure the second DMA transfer
```

The second call: DMA_removeStart2() - acts as if the earlier DMA has
completed, thus it synetically moves the index forwared.

Tangental Discussion:

    This also supports some "odd dma" requirements. For example some
    systems do not support crossing page boundaries with the DMA.

    Thus, when the first DMA_removeStart() returns, the 'pass1_bytes'
    might indicate thousands of bytes, but you might limit the
    transfer to say 128 bytes or up until the memory address crosses a
    page boundary.

Once the first transfer completes (ie: The DMA IRQ is raised), call
this:

```      DMA_removeComplete( pBUF, pass1_bytes );```

Once the second transfer completes, call this again

```     DMA_removeComplete( pBuf, pass2_bytes );```

The same applies to insert varients of the function.



