from setuptools import setup, find_packages 
  
setup( 
    name='sbomgen', 
    version='1.0.1', 
    description='SBOM Generator in cyclonedx format', 
    author='cd dev', 
    author_email='akashsah2003@gmail.com', 
    packages=['sbomgen', 
            'sbomgen.Parsers', 
            'sbomgen.Utility'
            ], 
    install_requires=[ 
        'datetime',
        'argparse',
        'toml',
        'pyyaml',
        'dicttoxml'
    ],
    entry_points= {
        'console_scripts': [
            'sbomgen = sbomgen.main:main',
        ],
    },
) 