import setuptools
import gonhang.api as api

setuptools.setup(
    name='gonhang',
    version='0.0.1',
    author="Fred Cox",
    author_email="fredcox@gmail.com",
    description='gonhang - The Next Generation Light-Weight System Monitor for Linux',
    long_description=api.FileUtil.getContents('README.md'),
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
        'humanfriendly'
    ],
    include_package_data=True,
    zip_safe=False,
)



