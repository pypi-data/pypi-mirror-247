from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ACSGUI',
    version='2.3.1',
    packages=find_packages(),
    include_package_data=True,
    description='A very basic advance calculator',
    long_description='This is a very advance calculator package.',
    url='',
    author='Tanishq JM',
    author_email='tanishqurmi@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Advance result analyzer',
    install_requires=['pandas','openpyxl','numpy','matplotlib',
                      'tabula','AH22CS174']
)
