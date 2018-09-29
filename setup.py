from setuptools import setup, find_packages
setup(
    name='doufo',
    version='0.0.3',
    description='Data Processing Library in functional style.',
    url='https://github.com/tech-pi/doufo',
    author='Hong Xiang',
    author_email='hx.hongxiang@gmail.com',
    license='Apache',
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    install_requires=['attrs>=18.1', 'numpy', 'multipledispatch'],
    scripts=[],
    zip_safe=False)

