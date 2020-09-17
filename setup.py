import setuptools

# ---------------------------------------------------
# system dependencies
# curl
# wmctrl
# hddtemp

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='gonhang',
    version='0.2.7',
    author="Fred Cox",
    author_email="fredcox@gmail.com",
    description='gonhang - The Next Generation Light-Weight System Monitor for Linux',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fredcox/gonhang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
    scripts=['bin/gonhang'],

    install_requires=[
        'PyQt5',
        'psutil',
        'humanfriendly',
        'requests'
    ],
    include_package_data=True,
    zip_safe=False,
)



