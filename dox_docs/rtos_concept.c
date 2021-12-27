/**
 *  @file 
 * @brief How Basic RTOS features supported by LostArm
 *
 * # RTOS Objects are simple pointer like things inside a uintptr_t
 *  @anchor concept_rtos
 *
 * Also see: @ref concept_mutex
 * Also see: @ref concept_semaphore
 *
 * RTOS elements are effectively pointers hidden inside a "uintptr_t"
 *
 * WHY? 
 *   Because often one must include a large number of files for an RTOS elements.
 *   These often cause many problems when porting code across platforms (ugh)
 *   A "void *" works, but - not all OSes items use pointers, some use integers.
 *
 * For example some RTOSes - require certian elements to be pre-allocated
 * ahead of time at startup or at compile time, and thus we are talking about
 * the "NTH" mutex (which is an integer right) so we use a uintptr_t 
 * as the basic type for all rtos elements.
 *
 * Think of it as a handle to a thread, or a semaphore or a mutex.
 *
 */
