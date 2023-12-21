from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Kuantsol Transformation Package'
LONG_DESCRIPTION = 'Kuantsol Transformation Package'

# Setting up
setup(
    name="kuantsol_transformation",
    version=VERSION,
    author="Barış Coşkun",
    author_email="<baris.coskun@kuantsol.ai>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that

    keywords=['python', 'kuantsol_transformation'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)