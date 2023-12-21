from setuptools import setup, find_packages

setup(
    name='holonetra',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'geopandas',
    ],
    author='Akhil Chhibber',
    author_email='akhil.chibber@gmail.com',
    description='A Python library for spatial operations',
    keywords='GIS geopandas buffer shapefile',
    url='https://github.com/akhilchibber',
)
