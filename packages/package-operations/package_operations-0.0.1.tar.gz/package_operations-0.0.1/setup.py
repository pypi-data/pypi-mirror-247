from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='package_operations',
    version='0.0.1',
    url='https://github.com/edithcarollaine/package_operations',
    license='MIT License',
    author='Edith Carollaine',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='edith.carollaine12@gmail.com',
    keywords='Package',
    description=u'Faz somas e subtrações',
    packages=['package_operations'],)