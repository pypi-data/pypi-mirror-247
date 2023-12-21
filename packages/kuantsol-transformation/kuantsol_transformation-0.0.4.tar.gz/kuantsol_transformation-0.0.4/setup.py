from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Kuantsol Transformation Package'
LONG_DESCRIPTION = 'Kuantsol Transformation Package'

with open('requirements.txt') as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="kuantsol_transformation",
    version=VERSION,
    author="Barış Coşkun",
    author_email="<baris.coskun@kuantsol.ai>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['kuantsol_transformation', 'kuantsol_transformation.*']),
    install_requires=required,  # add any additional packages that

    keywords=['python', 'kuantsol_transformation'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)