from setuptools import find_packages, setup


__description__ = "作业帮教研图表处理接口"
__license__ = ""
__requires__ = ["pyecharts"]
__version__ = "0.12"
__keywords__ = ["zyb", "charts"]


setup(
    name="zyb_charts",
    version=__version__,
    description=__description__,
    author='作业帮',
    author_email='',
    license=__license__,
    packages=find_packages(),
    include_package_data=True,
    keywords=__keywords__,
    install_requires=__requires__,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.7'
)

