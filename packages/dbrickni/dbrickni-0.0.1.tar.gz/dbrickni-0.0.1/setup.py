from setuptools import setup, find_packages

setup(
    name='dbrickni',
    version='0.0.1',
    author='Simon De Smul',
    author_email='simon.desmul@alinso.group',
    description='Package for import of databricks notebooks',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)