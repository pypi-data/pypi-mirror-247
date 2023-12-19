from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education'
]

setup(
    name='akash_calculator',
    version='0.0.2',
    description='A very basic calculator',
    long_description='A very basic calculator package.',
    url='',
    author='Akash Singh',
    author_email='akash.singh@proteustech.in',
    license='MIT',
    classifiers=classifiers,
    keywords="calculator",
    packages=find_packages(),
    install_requires=[],
    setup_requires=['wheel']  
)
