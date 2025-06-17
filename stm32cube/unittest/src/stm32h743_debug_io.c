/*
 * stm32h743_debug_io.c
 *
 *  Created on: Jul 2, 2022
 *      Author: duane
 */

#include <lostarm/lostarm.h>
#include <lostarm/debug.h>
#include <lostarm/wrapped/_string.h>

struct debug_context DEBUG_CONTEXT;

static void

void DEBUG_por_init(uintptr_t hwaddress, int baudrate )
{
	memset( (void *)(&DEBUG_CONTEXT), 0, sizeof(DEBUG_CONTEXT) );


	DEBUG_CONTEXT.pfn_tx = stm32_debug_tx;
	DEBUG_CONTEXT.pfn_rx = stm32_debug_rx;


}
