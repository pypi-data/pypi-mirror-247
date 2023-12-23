from setuptools import setup, find_packages

setup(
    name='directory-splitter',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your script may have
    ],
    entry_points={
        'console_scripts': [
            'directory-splitter = your_module_name:print_url',
        ],
    },
    author='Your Name',
    author_email='your@email.com',
    description='A script to split and extract unique endpoints from a list of URLs.',
    license='MIT',
    keywords='directory-splitter url-parser',
    url='https://github.com/yourusername/directory-splitter',
)
