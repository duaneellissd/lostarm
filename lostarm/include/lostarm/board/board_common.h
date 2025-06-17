#if !defined(BOARD_COMMON_H)
#if !defined(IN_THE_BOARD_H)
#error You should not include this directly.
#error This file should be included by your "the_board.h" file.
#endif

#include "lostarm/lostarm.h"
/*
 *========================================
 * Think twice before modifying this file.
 *========================================
 * You probably should be editing "the_board.h" instead.
 *
 * Because lots of things are "very common" across boards.
 * We have this file, hence the name: "board_common.h"
 *
 * For example: 
 *   We assume that all boards have some type of DEBUG uart
 *   And this will work with the DEBUG_various() functions.
 * 
 * Often things like this are duplicated in every the_board.h file
 * To avoid that, we have board_common.h
 *
 * Your "the_board.h" - should include this, then your board
 * should add what ever it needs that are specific to your board.
 *
 *========================================
 * If you are consolidating and refactoring multiple files
 * and trying to clean up lots of duplication *THEN*
 * You are probaly in the correct file.
 *========================================
 */

/* Configure the DEBUG output serial port to work.
 * This is a board specific function.
 *
 * @param uart_id = A very board specific value as defined by "the_board.h"
 * @param baudrate = I normally use 115200
 */
EXTERN_C void BOARD_DEBUG_POR_Init(uintptr_t uart_id, int baudrate );
