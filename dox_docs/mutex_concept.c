/**
 *  @file 
 *
 *  @anchor concept_mutex
 *
 * # Basic MUTEX Mutual Exclusion RTOS concept.
 *
 * TL;DR -> standard mutex, with lock/unlock, supports recursion.
 * recursion = same task/thread can relock a mutex.
 *
 * These guys are crazy and don't live in a real world.
 * http://www.fieryrobot.com/blog/2008/10/14/recursive-locks-will-kill-you/
 * https://mjtsai.com/blog/2012/03/12/recursive-mutexes-considered-harmful/
 *
 * The timeout parameter is always measured in milliseconds using standard lostarm rules.
 *
 *
 */


