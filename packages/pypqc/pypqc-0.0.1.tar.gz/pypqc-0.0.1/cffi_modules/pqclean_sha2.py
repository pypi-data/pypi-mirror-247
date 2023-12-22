from cffi import FFI

from pqc._util import fix_compile_args, map_immed

from pathlib import Path
import re

ffibuilder = FFI()
extra_compile_args = []
fix_compile_args(extra_compile_args)

ffibuilder.cdef("""\
#define PQC_SHA256CTX_BYTES ...
#define PQC_SHA512CTX_BYTES ...

typedef struct {uint8_t *ctx;} sha224ctx;
typedef struct {uint8_t *ctx;} sha256ctx;
typedef struct {uint8_t *ctx;} sha384ctx;
typedef struct {uint8_t *ctx;} sha512ctx;
""")

ffibuilder.cdef("""\
void sha224_inc_init(sha224ctx *state);
void sha224_inc_ctx_clone(sha224ctx *stateout, const sha224ctx *statein);
void sha224_inc_blocks(sha224ctx *state, const uint8_t *in, size_t inblocks);
void sha224_inc_finalize(uint8_t *out, sha224ctx *state, const uint8_t *in, size_t inlen);
void sha224_inc_ctx_release(sha224ctx *state);
void sha224(uint8_t *out, const uint8_t *in, size_t inlen);
""")

ffibuilder.cdef("""\
void sha256_inc_init(sha256ctx *state);
void sha256_inc_ctx_clone(sha256ctx *stateout, const sha256ctx *statein);
void sha256_inc_blocks(sha256ctx *state, const uint8_t *in, size_t inblocks);
void sha256_inc_finalize(uint8_t *out, sha256ctx *state, const uint8_t *in, size_t inlen);
void sha256_inc_ctx_release(sha256ctx *state);
void sha256(uint8_t *out, const uint8_t *in, size_t inlen);
""")

ffibuilder.cdef("""\
void sha384_inc_init(sha384ctx *state);
void sha384_inc_ctx_clone(sha384ctx *stateout, const sha384ctx *statein);
void sha384_inc_blocks(sha384ctx *state, const uint8_t *in, size_t inblocks);
void sha384_inc_finalize(uint8_t *out, sha384ctx *state, const uint8_t *in, size_t inlen);
void sha384_inc_ctx_release(sha384ctx *state);
void sha384(uint8_t *out, const uint8_t *in, size_t inlen);
""")

ffibuilder.cdef("""\
void sha512_inc_init(sha512ctx *state);
void sha512_inc_ctx_clone(sha512ctx *stateout, const sha512ctx *statein);
void sha512_inc_blocks(sha512ctx *state, const uint8_t *in, size_t inblocks);
void sha512_inc_finalize(uint8_t *out, sha512ctx *state, const uint8_t *in, size_t inlen);
void sha512_inc_ctx_release(sha512ctx *state);
void sha512(uint8_t *out, const uint8_t *in, size_t inlen);
""")

ffibuilder.set_source('pqc._lib.pqclean_sha2',
	'#include "sha2.h"',
#	None,
	include_dirs=['Lib/PQClean/common'],
	sources=['Lib/PQClean/common/sha2.c'],
	extra_compile_args=extra_compile_args,
)
ffi = ffibuilder
