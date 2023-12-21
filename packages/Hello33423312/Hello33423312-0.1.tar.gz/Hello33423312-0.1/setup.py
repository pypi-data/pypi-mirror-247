from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.1'
DESCRIPTION = 'Clear untuk Kode Kelompok'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="Hello33423312",
    version=VERSION,
    author="scaem007",
    author_email="<syahrulromadhonmuhamamd@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/syahrulcaem/Informasi_negara',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['Hello'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)