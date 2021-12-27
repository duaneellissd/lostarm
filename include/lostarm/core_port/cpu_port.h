#if !defined(CORE_PORT_CPU_H)
#define CORE_PORT_CPU_H

uintptr_t CPU_disable_irq(void);

void CPU_restore_irq( uintptr_t old );

void CPU_enable_irq( void );


#endif
