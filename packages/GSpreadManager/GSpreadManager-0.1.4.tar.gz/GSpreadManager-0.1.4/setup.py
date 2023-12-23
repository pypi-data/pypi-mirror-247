from setuptools import setup, find_packages

setup(
    name='GSpreadManager',
    version='0.1.4',
    author='PabloAlaniz',
    author_email='pablo@culturainteractiva.com',
    description='Un módulo de Python para gestionar y automatizar tareas en Google Sheets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PabloAlaniz/GSpreadManager',
    packages=find_packages(),
    install_requires=[
        'gspread>=3.0',
        'oauth2client>=4.0',
        'pandas>=1.2.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
