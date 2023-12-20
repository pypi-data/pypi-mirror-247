from setuptools import setup, find_packages 
  
setup( 
    name='sbomgentwo', 
    version='1.0.0', 
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
            'sbomgentwo = sbomgen.main:main',
        ],
    },
) 