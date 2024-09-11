import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pingshui_rhyme',
    version='0.2',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='A Python package for classifying Chinese characters phonologically based on the Middle Chinese Pingshui rhyme scheme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rbnyng',
    author_email='',
    url='https://github.com/rbnyng/pingshui_rhyme',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    package_data={
        'pingshui_rhyme': ['data/*.json'],
    },
)
