from setuptools import find_packages
from setuptools import setup


version = "2.1.4.dev0"

setup(
    name="plone.contentrules",
    version=version,
    description="Plone ContentRules Engine",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="Plone content rules events",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/plone.contentrules",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "ZODB",
        "zope.annotation",
        "zope.component",
        "zope.componentvocabulary",
        "zope.configuration",
        "zope.container",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.lifecycleevent",
        "zope.schema",
        "zope.testing",
    ],
)
