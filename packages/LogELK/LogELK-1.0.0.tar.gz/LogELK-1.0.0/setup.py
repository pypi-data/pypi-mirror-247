from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Envia os logs para o ELK'
LONG_DESCRIPTION = 'Envia os logs para o ELK através de requisições HTTP'

setup(
        name="LogELK",
        version=VERSION,
        author="Jones Vieira",
        author_email="<jones.vieira@tivit.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'requests==2.22.0',
            'urllib3==1.25.8'
        ]
)