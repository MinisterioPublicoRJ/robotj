from setuptools import setup, find_packages


__version__ = '0.0.0dev0'


setup(
    name='robotj',
    descripition='Robo de raspagem de processos do TJRJ',
    url='https://github.com/MinisterioPublicoRJ/robotj',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    author='Felipe Ferreira & Rhenan Bartels',
    license='MIT',
    zip_safe=False
)