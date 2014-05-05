from distutils.core import setup, Extension

# todo: put in the correct directories for flycap
module1 = Extension('pygray',
	                include_dirs = ['/usr/local/include'],
                    libraries = ['tcl83'],
                    library_dirs = ['/usr/local/lib'],
                    sources = ['pygray.cpp'])

setup (name = 'PyGray',
       version = '0.1',
       description = 'Point gray camera capture extension',
       ext_modules = [module1])