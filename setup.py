from distutils.core import setup

setup(
    name='maptools',
    version='1.0',
    packages = [
        'maptools',
        'maptools.calcusim',
        'maptools.calcusim.host',
        'maptools.calcusim.device',
        'maptools.core',
        'maptools.drawing',
        'maptools.hardware',
        'maptools.mapper',
        'maptools.quantization',
        'maptools.toksim',
        'maptools.utils'
    ]
)