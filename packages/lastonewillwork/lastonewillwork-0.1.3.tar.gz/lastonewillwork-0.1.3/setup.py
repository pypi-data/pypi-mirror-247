from setuptools import setup, find_packages

setup(
    name='lastonewillwork',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'my_script = main:main',
        ],
    },
    author='Guy',
    author_email='guykishon1@gmail.com',
    description='Test CICD',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/hachshara/CICD',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        # Add more classifiers as needed
    ],
)
