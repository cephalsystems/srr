from distutils.core import setup, Extension

# todo: put in the correct directories for flycap
module1 = Extension('pygray',
	                include_dirs = ['/usr/local/include', '/usr/include/flycapture'],
                    libraries = ['lflycapture'],
                    library_dirs = ['/usr/local/lib', '/usr/lib'],
                    sources = ['pygray.cpp'])

setup (name = 'PyGray',
       version = '0.1',
       description = 'Point gray camera capture extension',
       ext_modules = [module1])