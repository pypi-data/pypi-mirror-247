from setuptools import setup, find_packages

setup(
    name='UltraLink',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author='Noah Wilhoite',
    author_email='notnoah349@gmail.com',
    description='A container for my python modules.',
    long_description="""
This is a container for my python modules.
It's whole purpose is to allow me to access my own modules from anywhere without having to make a whole now package on PyPi.
""",
    long_description_content_type='text/markdown',
)