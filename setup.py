from setuptools import setup, find_packages

setup(
    name='TransEdit',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'transedit = transedit.transedit:main'  
        ],
    },
    install_requires=[
        'beautifulsoup4', 
    ],
    python_requires='>=3.6',
    description='A simple text editor which edits the text with a pipeline of transformations, written as a Python function.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Phil Jones (Future Office Labs)',
    author_email='interstar@gmail.com',
    url='https://github.com/interstar/transedit', 
)

