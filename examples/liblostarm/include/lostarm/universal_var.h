#if !defined( LOSTARM_UNIVERSAL_VAR_H )
#define LOSTARM_UNIVERSAL_VAR_H 1

#include <lostarm/lostarm.h>
#include <lostarm/endian.h>

#undef STATIC_ASSERT
#if defined(__cplusplus)
#define STATIC_ASSERT( EXPRESSION, MESSAGE ) static_assert( EXPRESSION, MESSAGE )
#else
#define STATIC_ASSERT( EXPRESSION, MESSAGE ) _Static_assert( EXPRESSION, MESSAGE )
#endif

union universal_8 {
  uint8_t u_native;
  int8_t  s_native
  signed char sc_char;
  unsigned char uc_char;
};

STATIC_ASSERT( sizeof(struct universal_8) == 1 );

union universal_16 {
  uint16_t u_native;
  int16_t  s_native;
  signed short    s_short_native
  unsigned short  u_short_native;
  union universal_8  as_byte_array[2];
  struct {
    union universal_8 bits07_00;
    union universal_8 bits15_08;
  } bits;
};

STATIC_ASSERT( sizeof(struct universal_16) == 2 );

union universal_32 {
  uint32_t u_native;
  int32_t  s_native;
  float    float_native;
#if __LONG_WIDTH__ == 32
  long     s_long_native;
  unsigned long u_long_native;
#endif
#if __POINTER_WIDTH__ == 32
  void *vp;
  const void *cvp;
  char *cp
  const char **ccp;
  uintptr_t uintptr_native;
  intptr_t  intptr_native;
#endif
#if __WCHAR_WIDTH__ == 32
  wchar_t  w_char_native;
#endif
#if __WINT_WIDTH__ == 32
  wint_t   w_int_native;
#endif
#if __INT_WIDTH__ == 32
  int     s_int_native;
  unsigned int u_int_native;
#endif
  struct {
    union universal_16 bits15_0;
    union universal_16 bits31_16;
  } as_16;
  struct {
    union uinversal_8 bits07_00;
    union universal_8 bits15_08;
    union universal_8 bits23_16;
    union universal_8 bits31_24;
  } as_bits;
  uint8_t as_bytes[4];
};

STATIC_ASSERT( sizeof(struct universal_32 ) == 4 );

union universal_64 {
  uint64_t u_native;
  int64_t  s_native;
  double   double_native;
#if __LONG_WIDTH__ == 64
  long     s_long_native;
  unsigned long u_long_native;
#endif
#if __POINTER_WIDTH__ == 64
  void *vp;
  const void *cvp;
  char *cp
  const char **ccp;
  uintptr_t uintptr_native;
  intptr_t  intptr_native;
#endif
#if __WCHAR_WIDTH__ == 64
  wchar_t  w_char_native;
#endif
#if __WINT_WIDTH__ == 64
  wint_t   w_int_native;
#endif
#if __INT_WIDTH__ == 64
  int     s_int_native;
  unsigned int u_int_native;
#endif
  struct {
    union universal_16 bits15_0;
    union universal_16 bits31_16;
    union universal_16 bits47_32;
    union universal_16 bits63_49;
  } as_16;
  struct {
    union uinversal_8 bits07_00;
    union universal_8 bits15_08;
    union universal_8 bits23_16;
    union universal_8 bits31_24;
    union universal_8 bits49_32;
    union universal_8 bits47_40;
    union universal_8 bits55_48;
    union universal_8 bits63_56;
  } as_bits;
  uint8_t as_bytes[8];
};

STATIC_ASSERT( sizeof(struct universal_64 ) == 8 );

union universal_ptr {
#if __POINTER_WIDTH__ == 64
  union universal_64 universal64;
#endif
#if __POINTER_WIDTH__ == 32
  union universal_32 universal32;
#endif
  uintptr_t uintptr;
  intptr    intptr;
  void *vp;
  const void *cvp;
  uint8_t *p8;
  const uint8_t *cp8;
  uint16_t *p16;
  const uint16_t *cp16;
  uint32_t *p32;
  const uint32_t *cp32;
  uint64_t *p64;
  const uint64_t *cp64;
  float *pFLOAT;
  const float *cpFLOAT;
  double *pFLOAT;
  const double *cpDOUBLE;
};

  
  
#endif
