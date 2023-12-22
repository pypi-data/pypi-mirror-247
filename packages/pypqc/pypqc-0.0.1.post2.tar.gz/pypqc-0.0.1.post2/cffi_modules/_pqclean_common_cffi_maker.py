from cffi import FFI

from distutils.sysconfig import parse_makefile
from pathlib import Path
import platform
import re
from textwrap import dedent

from pqc._util import partition_list, map_immed

def make_ffi(build_root, lib_name):
	build_root = Path(build_root)
	module_name = f'pqc._lib.pqclean_{lib_name}'

	ffibuilder = FFI()
	extra_compile_args = []
	csources = []
	cdefs = []

	# Public Interface

	sources = [(build_root / lib_name).with_suffix('.c')]

	include = [(build_root), *(p.with_suffix('.h') for p in sources)]
	include_h = [p for p in include if not p.is_dir()]
	include_dirs = list({(p.parent if not p.is_dir() else p) for p in include})

	for p in include_h:
		csources.append(f'#include "{p.name}"')
		cdefs.append(re.sub(r'(?m)^(#\w.*)', '', p.read_text()))

	# Platform-specific

	if platform.system() == 'Windows':
		# https://foss.heptapod.net/pypy/cffi/-/issues/516
		# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
		# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
		extra_compile_args.append('/TC')

	from pprint import pprint; pprint(locals())
	ffibuilder.set_source(
		module_name,
		'\n'.join(csources),
		sources=[p.as_posix() for p in sources],
		include_dirs=[p.as_posix() for p in include_dirs],
		extra_compile_args=extra_compile_args,
	)
	map_immed(ffibuilder.cdef, cdefs)
	return ffibuilder
