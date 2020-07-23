from setuptools import setup, find_packages

# Reduce maintenance by using both of dependencies' management files
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='iFASTATHANU',
    version='0.1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Source': 'https://github.com/hungvutuan/iFASTATHANU-Flask-Python'
    },
    install_requires=requirements
)
