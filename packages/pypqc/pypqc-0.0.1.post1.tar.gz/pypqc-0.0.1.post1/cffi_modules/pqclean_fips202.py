from cffi import FFI

from pqc._util import fix_compile_args, map_immed

from pathlib import Path
import re

ffibuilder = FFI()
extra_compile_args = []
fix_compile_args(extra_compile_args)

ffibuilder.cdef("""\
#define SHAKE128_RATE ...
#define SHAKE256_RATE ...
#define SHA3_256_RATE ...
#define SHA3_384_RATE ...
#define SHA3_512_RATE ...
#define PQC_SHAKEINCCTX_BYTES ...
#define PQC_SHAKECTX_BYTES ...

typedef struct {uint64_t *ctx;} shake128incctx;
typedef struct {uint64_t *ctx;} shake128ctx;
typedef struct {uint64_t *ctx;} shake256incctx;
typedef struct {uint64_t *ctx;} shake256ctx;
typedef struct {uint64_t *ctx;} sha3_256incctx;
typedef struct {uint64_t *ctx;} sha3_384incctx;
typedef struct {uint64_t *ctx;} sha3_512incctx;
""")

ffibuilder.cdef("""
void shake128_absorb(shake128ctx *state, const uint8_t *input, size_t inlen);
void shake128_squeezeblocks(uint8_t *output, size_t nblocks, shake128ctx *state);
void shake128_ctx_release(shake128ctx *state);
void shake128_ctx_clone(shake128ctx *dest, const shake128ctx *src);
void shake128_inc_init(shake128incctx *state);
void shake128_inc_absorb(shake128incctx *state, const uint8_t *input, size_t inlen);
void shake128_inc_finalize(shake128incctx *state);
void shake128_inc_squeeze(uint8_t *output, size_t outlen, shake128incctx *state);
void shake128_inc_ctx_clone(shake128incctx *dest, const shake128incctx *src);
void shake128_inc_ctx_release(shake128incctx *state);
""")

ffibuilder.cdef("""\
void shake256_absorb(shake256ctx *state, const uint8_t *input, size_t inlen);
void shake256_squeezeblocks(uint8_t *output, size_t nblocks, shake256ctx *state);
void shake256_ctx_release(shake256ctx *state);
void shake256_ctx_clone(shake256ctx *dest, const shake256ctx *src);
void shake256_inc_init(shake256incctx *state);
void shake256_inc_absorb(shake256incctx *state, const uint8_t *input, size_t inlen);
void shake256_inc_finalize(shake256incctx *state);
void shake256_inc_squeeze(uint8_t *output, size_t outlen, shake256incctx *state);
void shake256_inc_ctx_clone(shake256incctx *dest, const shake256incctx *src);
void shake256_inc_ctx_release(shake256incctx *state);
void shake128(uint8_t *output, size_t outlen, const uint8_t *input, size_t inlen);
void shake256(uint8_t *output, size_t outlen, const uint8_t *input, size_t inlen);
void sha3_256_inc_init(sha3_256incctx *state);
void sha3_256_inc_absorb(sha3_256incctx *state, const uint8_t *input, size_t inlen);
void sha3_256_inc_finalize(uint8_t *output, sha3_256incctx *state);
void sha3_256_inc_ctx_clone(sha3_256incctx *dest, const sha3_256incctx *src);
void sha3_256_inc_ctx_release(sha3_256incctx *state);
void sha3_256(uint8_t *output, const uint8_t *input, size_t inlen);
""")

ffibuilder.cdef("""\
void sha3_384_inc_init(sha3_384incctx *state);
void sha3_384_inc_absorb(sha3_384incctx *state, const uint8_t *input, size_t inlen);
void sha3_384_inc_finalize(uint8_t *output, sha3_384incctx *state);
void sha3_384_inc_ctx_clone(sha3_384incctx *dest, const sha3_384incctx *src);
void sha3_384_inc_ctx_release(sha3_384incctx *state);
void sha3_384(uint8_t *output, const uint8_t *input, size_t inlen);
void sha3_512_inc_init(sha3_512incctx *state);
void sha3_512_inc_absorb(sha3_512incctx *state, const uint8_t *input, size_t inlen);
void sha3_512_inc_finalize(uint8_t *output, sha3_512incctx *state);
void sha3_512_inc_ctx_clone(sha3_512incctx *dest, const sha3_512incctx *src);
void sha3_512_inc_ctx_release(sha3_512incctx *state);
void sha3_512(uint8_t *output, const uint8_t *input, size_t inlen);
""")

ffibuilder.set_source('pqc._lib.pqclean_fips202',
	'#include "fips202.h"',
#	None,
	include_dirs=['Lib/PQClean/common'],
	sources=['Lib/PQClean/common/fips202.c'],
	extra_compile_args=extra_compile_args,
)
ffi = ffibuilder
