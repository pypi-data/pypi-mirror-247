from setuptools import setup, find_packages

setup(
    name='hw_2',
    version='0.1.0',
    author='Emir Vildanov',
    author_email='emirvildanow@gmail.com',
    description='Package to generate latex',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)