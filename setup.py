from setuptools import setup, find_packages

setup(
    name='iFASTATHANU',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Source': 'https://github.com/hungvutuan/iFASTATHANU-Flask-Python'
    },
    install_requires=[
        'Flask>=0.2',
        'mysql-connector-python>=8.0',
        'pydantic>=1.6'
    ]
)
