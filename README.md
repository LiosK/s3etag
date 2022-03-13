# s3etag
This repository was created by forking [LosK/s3etag](https://github.com/LiosK/s3etag)
## How to Install
```
$ pip install git+https://github.com/koichikawamura/s3etag
```

## Usage
### Command Line
See help:
```
$ s3etag --help
```
#### example
```
$ s3etag example.file
```
### in Your Code
```python
import pathlib
from s3etag import calc_s3_etag

filename = pathlib.Path('example.file')
# filename can be either pathlib.PosixPath or str
etag = calc_s3_etag(filename)
```
```
Help on function calc_s3_etag in module s3etag:

calc_s3_etag(filename, threshhold=8388608, chunksize=8388608)
    Compute Etag for a file

    Args:
        filename (pathlib.PosixPath or str):
            Path to the file on which the function computes etag
        threshhold (int):
            file-size (in bytes) threshhold above which the function computes
            etag chunk-wise / optional, defaults to 8388608 = 8M bytes
        chunksize (int):
            chunksize in bytes / optional, defaults to 8388608 = 8M bytes

    Returns:
        str: etag (aws s3-style md5)
```
