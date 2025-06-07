from setuptools import setup, find_packages

# Extract version without importing the package
version = {}
with open('docopt/_version.py') as f:
    exec(f.read(), version)

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='docopt-ng',
    version=version['__version__'],
    description='Jazzband-maintained fork of docopt, the humane command line arguments parser.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nick Crews',
    author_email='nicholas.b.crews@gmail.com',
    url='https://github.com/jazzband/docopt-ng',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
