from setuptools import setup,find_packages
classifiers=[
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'

]
setup(
     name='RandomiGiorgiUertashvili',
     version='0.0.1',
     description='calculator',
long_description_content_type="text/markdown",

    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Giorgi Uertashvili',
    author_email='giouerta97@gmail.com',
    license='MIT',
    keywords='calculator',
    classifiers=classifiers,
    packages=find_packages(),
    install_requesres=['']




)