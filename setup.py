import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pdf_wrangler',
    version='0.0.1',
    author='happilyeverafter95',
    author_email='author@example.com',
    description='PDFMiner Wrapper & Other PDF utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/happilyeverafter95/pdf-wrangler',
    install_requires=['pdfminer.six==20181108'],
    project_urls={
        'Bug Tracker': 'https://github.com/happilyeverafter95/pdf-wrangler/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
)