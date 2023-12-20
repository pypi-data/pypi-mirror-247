from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='helptool',
    version='1.0.1',    
    description='Help tool for linux',
    url='https://github.com/Lessyzz',
    author='Lessy',
    author_email='onurtazefidan12345@gmail.com',
    packages=['helptool'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    long_description=long_description,
    long_description_content_type="text/markdown",
)