from setuptools import setup, find_packages

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
    install_requires=[
        'Flask>=1.0',
        'mysql-connector-python',
        'pydantic==1.6'
    ]
)
