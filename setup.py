from setuptools import setup, find_packages
setup(
    name='doufo',
    version='0.0.1',
    description='Data Processing Library in functional style.',
    url='https://github.com/Hong-Xiang/doufo',
    author='Hong Xiang',
    author_email='hx.hongxiang@gmail.com',
    license='Apache',
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    install_requires=[],
    scripts=[],
    zip_safe=False)

