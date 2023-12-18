#include "common.h"

#if defined(__AVX512VL__) && defined(__AVX512VBMI2__) && defined(__AVX512BW__)
# include "decoder_common.h"
# ifndef YENC_DISABLE_AVX256
#  include "decoder_avx2_base.h"
void decoder_set_vbmi2_funcs() {
    ALIGN_ALLOC(lookups, sizeof(*lookups), 16);
    // TODO: consider removing compact LUT
    decoder_init_lut(lookups->eqFix, lookups->compact);
    _do_decode = &do_decode_simd<false, false, sizeof(__m256i)*2, do_decode_avx2<false, false, ISA_LEVEL_VBMI2> >;
    _do_decode_raw = &do_decode_simd<true, false, sizeof(__m256i)*2, do_decode_avx2<true, false, ISA_LEVEL_VBMI2> >;
    _do_decode_end_raw = &do_decode_simd<true, true, sizeof(__m256i)*2, do_decode_avx2<true, true, ISA_LEVEL_VBMI2> >;
    _decode_simd_level = ISA_LEVEL_VBMI2;
}
# else
#  include "decoder_sse_base.h"
void decoder_set_vbmi2_funcs() {
    decoder_sse_init();
    decoder_init_lut(lookups->eqFix, lookups->compact);
    _do_decode = &do_decode_simd<false, false, sizeof(__m128i)*2, do_decode_sse<false, false, ISA_LEVEL_VBMI2> >;
    _do_decode_raw = &do_decode_simd<true, false, sizeof(__m128i)*2, do_decode_sse<true, false, ISA_LEVEL_VBMI2> >;
    _do_decode_end_raw = &do_decode_simd<true, true, sizeof(__m128i)*2, do_decode_sse<true, true, ISA_LEVEL_VBMI2> >;
    _decode_simd_level = ISA_LEVEL_VBMI2;
}
# endif
#else

void decoder_set_avx2_funcs();

void decoder_set_vbmi2_funcs() {
    decoder_set_avx2_funcs();
}
#endif
