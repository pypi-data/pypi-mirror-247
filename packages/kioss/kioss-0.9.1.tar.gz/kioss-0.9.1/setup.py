from setuptools import find_packages, setup # type: ignore

setup(
    name='kioss',
    version='0.9.1',
    packages=find_packages(),
    package_data={"kioss": ["py.typed"]},
    url='http://github.com/bonnal-enzo/kioss',
    license='Apache 2.',
    author='bonnal-enzo',
    author_email='bonnal.enzo.dev@gmail.com',
    description='Keep I/O Simple and Stupid: Ease the development of ETL/EL/ReverseETL scripts.'
)
