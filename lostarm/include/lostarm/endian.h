#if !defined(LOSTARM_ENDIAN_H)
#define LOST_ARM_ENDIAN_H "4f708181-ebd4-4821-a0c6-eee5b59ea851"

#include <lostarm/lostarm.h>

/** @file
 * This file has some standardized Endian functions.
 *
 * Many would argue that this exists in a unix platform
 * with functions like:  htons() (host to network order short)
 *
 * Sorry, thats nice but ... often what is needed is the output to be in
 * a very specific order - that is the goal and purpose of this.
 *
 * The initials:  HE -> Host endian, LE -> Little Endian, BE -> Big Endian.
 *
 */

#if !defined(__BYTE_ORDER__)
#error compiler.h did not define __BYTE_ORDER__
#endif

#if !defined(__ORDER_LITTLE_ENDIAN__)
#error compiler.h did not define this.
#endif

#if !defined(__ORDER_BIG_ENDIAN__)
#error compiler.h did not define this.
#endif

/**@brief Basic Byte swap functions.
 * @{
 */

EXTERN_C uint16_t  ENDIAN_swap16( uint16_t v16 );
EXTERN_C uint32_t  ENDIAN_swap32( uint32_t v32 );
EXTERN_C uint64_t  ENDIAN_swap64( uint64_t v64 );
/** @}
 */

/**@brief Host 2 Big/Little by size
 * @{
 */
EXTERN_C uint16_t  ENDIAN_H2B_16( uint16_t v16 );
EXTERN_C uint16_t  ENDIAN_H2L_16( uint16_t v16);

EXTERN_C uint32_t  ENDIAN_H2B_32( uint32_t v32 );
EXTERN_C uint32_t  ENDIAN_H2L_32( uint32_t v32);

EXTERN_C uint64_t  ENDIAN_H2B_64( uint64_t v64 );
EXTERN_C uint64_t  ENDIAN_H2L_64( uint64_t v64);
/** @}
 */

/**@brief Swap a buffer inplace
 * @{
 */
EXTERN_C void  ENDIAN_inplace_swap16( uint16_t *pBuffer, size_t nelement );
EXTERN_C void  ENDIAN_inplace_swap32( uint32_t *pBuffer, size_t nelement );
EXTERN_C void  ENDIAN_inplace_swap64( uint64_t *pBuffer, size_t nelement );

EXTERN_C void  ENDIAN_inplace_H2B_16( uint16_t *pBuffer, size_t nelement );
EXTERN_C void  ENDIAN_inplace_H2B_32( uint32_t *pBuffer, size_t nelement );
EXTERN_C void  ENDIAN_inplace_H2B_64( uint64_t *pBuffer, size_t nelement );

EXTERN_C void  ENDIAN_inplace_H2L_16( uint16_t *pBuffer, size_t nelement );
EXTERN_C void  ENDIAN_inplace_H2L_32( uint32_t *pBuffer, size_t nelement );
EXTERN_C void  ENDIAN_inplace_H2L_64( uint64_t *pBuffer, size_t nelement );
/** @}
 */


/**@brief copy a buffer and swap byte order
 * @{
 */
EXTERN_C void  ENDIAN_memmove_swap16( uint16_t *pDestBuffer, const uint16_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_swap32( uint32_t *pDestBuffer, const uint32_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_swap64( uint64_t *pDestBuffer, const uint64_t *pSrcBuffer, size_t nelement );

EXTERN_C void  ENDIAN_memmove_H2B_16( uint16_t *pDestBuffer, const uint16_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_H2B_32( uint32_t *pDestBuffer, const uint32_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_H2B_64( uint64_t *pDestBuffer, const uint64_t *pSrcBuffer, size_t nelement );

EXTERN_C void  ENDIAN_memmove_B2H_16( uint16_t *pDestBuffer, const uint16_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_B2H_32( uint32_t *pDestBuffer, const uint32_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_B2H_64( uint64_t *pDestBuffer, const uint64_t *pSrcBuffer, size_t nelement );

EXTERN_C void  ENDIAN_memmove_H2L_16( uint16_t *pDestBuffer, const uint16_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_H2L_32( uint32_t *pDestBuffer, const uint32_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_H2L_64( uint64_t *pDestBuffer, const uint64_t *pSrcBuffer, size_t nelement );

EXTERN_C void  ENDIAN_memmove_L2H_16( uint16_t *pDestBuffer, const uint16_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_L2H_32( uint32_t *pDestBuffer, const uint32_t *pSrcBuffer, size_t nelement );
EXTERN_C void  ENDIAN_memmove_L2H_64( uint64_t *pDestBuffer, const uint64_t *pSrcBuffer, size_t nelement );
/** @}
 */



#endif
