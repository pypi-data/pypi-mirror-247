from struct import pack
from setuptools import setup , find_packages

setup(
    name= 'Mensajes-Panchob28',
    version='5.0',
    descripcion='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    autor='Francisco Burchardt',
    email='saiman_4@hotmail.com',
    url='https://www.linkedin.com/in/francisco-burchardt/',
    license_files=['LICENSE'],
    packages= find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip()
                                     for paquete in open('requirements.txt').readlines()],

    classifires=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',        
        'Topic :: Utilities'
    ]                                 
)