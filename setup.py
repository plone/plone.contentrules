from setuptools import setup, find_packages

version = '2.0.7'

setup(
    name='plone.contentrules',
    version=version,
    description="Plone ContentRules Engine",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Plone content rules events',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/plone.contentrules',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      'setuptools',
      'six',
      'ZODB3',
      'zope.annotation',
      'zope.component',
      'zope.componentvocabulary',
      'zope.configuration',
      'zope.container',
      'zope.i18nmessageid',
      'zope.interface',
      'zope.lifecycleevent',
      'zope.schema',
      'zope.testing',
    ],
    )
