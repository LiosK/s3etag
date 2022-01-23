import setuptools

with open("README.md", mode="r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3etag",
    version="0.1.0",
    author="Koichi Kawamura",
    author_email="koichikwmr@icloud.com",
    description="calculate AWS S3 etag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koichikawamura/s3etag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['s3etag = s3etag:main']
    },
    python_requires='>=3.7',
)
