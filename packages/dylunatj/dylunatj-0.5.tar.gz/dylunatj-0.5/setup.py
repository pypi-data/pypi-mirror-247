from setuptools import setup
import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(name='dylunatj',
      description='A simple wsgi web framework',
    #   long_description=long_description,
      version='0.5',
      url='https://github.com/gjergjk71/dylunatj',
      author='Gjergj Kadriu',
      author_email='tasoha1763@astegol.com',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      packages=['dylunatj'],
      install_requires=[
          setuptools.find_packages()
      ],
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
)