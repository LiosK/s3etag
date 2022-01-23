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
etag = calc_s3_etag(filename, 8388608, 8388608)
```
