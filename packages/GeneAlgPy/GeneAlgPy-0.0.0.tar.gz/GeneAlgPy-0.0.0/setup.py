from setuptools import setup, find_packages

VERSION = '0.0.0' 
DESCRIPTION = 'Genetic algorithm tools'
LONG_DESCRIPTION = 'Python genetic algorithm tools with fortran backend'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="GeneAlgPy", 
        version=VERSION,
        author="Adam Shannon",
        author_email="adam.shannon02@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Genetic Algorithms'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)