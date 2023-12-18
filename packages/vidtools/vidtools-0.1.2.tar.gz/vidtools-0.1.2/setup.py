from setuptools import setup, find_packages

VERSION = '0.1.2' 
DESCRIPTION = 'video editor scripts'
LONG_DESCRIPTION = 'minimum package for automating common video and content editing tasks'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="vidtools", 
        version=VERSION,
        author="tijgersoftware",
        author_email="tijgersoftware@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)