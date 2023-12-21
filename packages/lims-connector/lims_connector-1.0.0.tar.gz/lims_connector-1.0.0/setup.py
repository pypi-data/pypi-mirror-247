from setuptools import setup, find_packages

setup(
    name='lims_connector',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    author='Manish Kumar',
    author_email='mkumar1@cmh.edu',
    description='Python module for basic querying of LIMS samples, analyses, and analysis files',
    url='https://dev.azure.com/CMHResearchIS/GMC/_git/cmhlims_orm',
    install_requires=[
        'pyyaml',
        'sqlalchemy',
        'pymysql',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
