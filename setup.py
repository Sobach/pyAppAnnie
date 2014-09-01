from distutils.core import setup

setup(
    name='pyAppAnnie',
    version='0.0.1',
    author='Alexander Tolmach',
    author_email='tolmach@me.com',
    packages=['pyappannie', 'pyappannie.test'],
    #scripts=[],
    url='https://github.com/Sobach/pyAppAnnie/',
    license='LICENSE.txt',
    description='Wrapper for mobile applications stats service App Annie.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.3.0",
    ],
)