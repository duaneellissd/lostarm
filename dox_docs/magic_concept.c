/**
 * @file
 * @brief magic structure elements, what are they for?
 *
 *
 * @anchor concept_magic
 *
 * Often - one passes a pointer of sometype as the primary class or structure
 * that is being used or manipulated.
 * 
 * Often that pointer is hidden behind a "void *" or a "uintptr_t" and
 * alot of casting occurs and you end up pointing something else and not
 * what you think. This provides a means to verify (via asserts) that
 * the class/struct is what you think it is
 *
 * What you should do:
 *
 * In eaach major thing, create a THING_fromVP, THING_fromCVP, or THING_fromUINT
 * this function should (A) take a void pointer (VP) or (B) const void pointer
 * or (C) a uintptr_t (D) valdiate the structure and if and only if that pointer
 * is valid return the item cast to the appropriate item.
 * 
 * The general format would be:
 * 
 *
 *@code
 *
 *struct debug_vars *DEBUG_VARS_fromUINT( uintptr_t thing )
 *{
 *	struct debug_vars *pVars;
 *
 *	pVars = (struct debug_vars *)(thing);
 *
 *	// Make sure the magic is correct
 *	DEBUG_ASSERT1( pVars->magic == SOMEVALUE ){
 *	return pVars;
 *}
 *
 * @endcode
 *
 *
 * The problem is what should the "magic" value be?
 * 
 * Ultimately it is your choice, often I use the address of the THING_init()
 * function cast to a uintptr_t.
 * 
 * Why this? Value: First, it is a unique numeric value for the platform
 * that function must live within the address space and it is the only
 * function at that address, thus it becomes a unique value.
 * 
 * Why not a \#define?  Because often people copy/paste code, don't
 * undertand what they are using or doing, and any hard coded
 * numeric value in a \#define will be duplicated
 * 
 * By using an address of a function - it is generally 100% always unique
 * even if the person copied and pasted that function
 */


