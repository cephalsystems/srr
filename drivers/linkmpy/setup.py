from distutils.core import setup, Extension

module1 = Extension('linkmpy',
                    include_dirs=['/usr/local/include',
                                  '/usr/include/INCLUDEDIR'],
                    libraries=['LIBRARY'],
                    library_dirs=['/usr/local/lib', '/usr/lib'],
                    sources=['linkmpy.cpp'])

setup(name='LinkMPy',
      version='0.1',
      description='linkm-lib python bindings',
      ext_modules=[module1])
