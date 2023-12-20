from setuptools import setup, find_packages

setup(
    name="rm_common_python_utils",
    version="0.2",
    author="RM",
    author_email="afrasiyab.manzoor@razormetrics.com",
    description="A project to provide common functionality across our python projects",
    url="https://git-codecommit.us-east-1.amazonaws.com/v1/repos/python_utils_development",
    packages=find_packages(),
    install_requires=[
        'rollbar==0.16.3',
        'psycopg_pool==3.1.7',
        'psycopg[binary]==3.1.9',
        'SQLAlchemy==1.4.48',
        'psycopg2-binary==2.9.5',
        'tqdm==4.65.0',
        'python-snappy==0.6.1',
        'protobuf==4.24.3',
        'boto3~=1.19.9',
        'pytest==7.4.0',
        'pytest-mock==3.11.1',
        'pydantic==2.5.1'
    ],
)
