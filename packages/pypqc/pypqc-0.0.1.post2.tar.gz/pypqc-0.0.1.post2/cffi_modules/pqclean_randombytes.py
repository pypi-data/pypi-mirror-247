from cffi import FFI

from pqc._util import fix_compile_args

ffibuilder = FFI()
extra_compile_args = []
fix_compile_args(extra_compile_args)

ffibuilder.cdef("""\
int PQCLEAN_randombytes(uint8_t *output, size_t n);
""")

ffibuilder.set_source('pqc._lib.pqclean_randombytes',
	'#include "randombytes.h"',
#	None,
	include_dirs=['Lib/PQClean/common'],
	sources=['Lib/PQClean/common/randombytes.c'],
	extra_compile_args=extra_compile_args,
)
ffi = ffibuilder
