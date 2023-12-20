from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Barcelona Vocabulary Questonnaire'
LONG_DESCRIPTION = 'Development package for the Barcelona Vocabulary Questonnaire (BVQ)'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="bvqpy", 
        version=VERSION,
        author="Gonzalo Garcia-Castro",
        author_email="gongarciacastro@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'requests'
        ], 
        
        keywords=['python', 'vocabulary'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)