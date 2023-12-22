from setuptools import setup, find_packages

setup(
    name='dataset_private',
    version='1.0.1',
    author='tmptmp',
    author_email='tmptmp@tmptmp.com',
    description='A package for getting datasets from package',
    include_package_data=True,
    packages=find_packages(),
)
