from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "My first package"
LONG_DESCRIPTION = 'My Python first package with a slightly longer description'

setup(

        name="verysimplemodule_andreia",
        version=VERSION,
        author="andreia",

        author_email="andreia.st.1010@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['scikit-image', 'numpy'],

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)
