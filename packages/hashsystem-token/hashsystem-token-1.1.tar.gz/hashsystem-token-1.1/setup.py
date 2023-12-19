from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "des.md").read_text()
setup(
    name='hashsystem-token',
    version='1.1',
    author='Rajat Mishra',
    author_email='rajatsmishra@aol.com',
    description='hashsystem helps developers generate hash passwords and generate token and decode token,that can be used in jwt ,apitokens,any kind of encription and decription process.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)