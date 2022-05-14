#if !defined(CORE_PORT_CPU_H)
#define CORE_PORT_CPU_H "20033f5a-b9ce-4cb0-bcea-1b38f04db999"

/*
 * Fairly standard baremetal operation
 * Disable all IRQs at the CPU, aka: critical section.
 *
 * Return old state, sutible for CPU_irq_restore()
 */
uintptr_t CPU_irq_disable(void);

/*
 * Restore the old state from a CPU_irq_disable() call.
 */
void CPU_irq_restore( uintptr_t old );


/*
 * At power on reset (POR) it is assumed the
 * CPU has the IRQs disabled, this enables the
 * CPU irq.
 */
void CPU_irq_enable( void );


#endif
