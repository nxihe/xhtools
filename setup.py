import setuptools 

with open ('README.md' , 'r') as fh:
    long_description = fh.read()
    setuptools.setup(
        name='xhtools', version='0.1',author='yunze', author_email='kenbliky@gmail.com',
        description='各种数据分析小工具及一些好玩的脚本', long_description=long_description,
        long_description_content_type='text/markdown', url='https://github.com/nxihe/xhtools',
        packages=setuptools.find_packages (),
        classifiers=['Programming Language :: Python :: 3','License : : OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
        python_requires='>= 3.5')