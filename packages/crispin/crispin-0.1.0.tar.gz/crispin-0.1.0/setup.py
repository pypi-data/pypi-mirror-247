from setuptools import setup, find_packages

setup(
    name='crispin',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'crispin = crispin.__main__:main',
        ],
    },
    author='Your Name',
    author_email='dominique.c.a.paul@gmail.com',
    description='A Python package named Crispin with custom functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dominiquepaul/crispin',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)