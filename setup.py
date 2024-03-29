import os
from distutils.core import Extension, setup
from Cython.Build import cythonize

extension = Extension(
    'maptools.toksim.toksim',
    sources=[
        "maptools/toksim/toksim.pyx", 
        "maptools/toksim/srcs/c_toksim.cpp",
        "maptools/toksim/srcs/c_windowbuf.cpp",
        "maptools/toksim/srcs/c_token.cpp",
        "maptools/toksim/srcs/c_tile.cpp",
        "maptools/toksim/srcs/c_comm.cpp"
    ],
    language='c++'
)

if os.name == 'posix':
    ext_modules = cythonize(extension)
else: 
    ext_modules = None

setup(
    name='maptools',
    version='1.0',
    packages=[
        'maptools',
        'maptools.calcusim',
        'maptools.calcusim.host',
        'maptools.calcusim.device',
        'maptools.core',
        'maptools.drawing',
        'maptools.hardware',
        'maptools.mapper',
        'maptools.quantization',
        'maptools.quantization.ppq_lowbit',
        'maptools.toksim',
        'maptools.utils',
        'maptools.nlrt',
        'maptools.research'
    ],
    ext_modules=ext_modules
)
