from setuptools import setup, find_packages

VERSION = '00.00.10'
DESCRIPTION = 'hanfu is a Data Analysis package'
LONG_DESCRIPTION = 'This Python package will help you to analyse data'


setup(
        name="hanfu", 
        version=VERSION,
        author="Dr Anna Sung and Prof Kelvin Leong",
        author_email="<k.leong@chester.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas','transformers','tabulate'], # add any additional packages that 
               
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Education",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
