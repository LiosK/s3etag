```text
usage: s3etag [-h] [--chunksize size] files [files ...]

s3etag - compute AWS S3 Etags

positional arguments:
  files             filenames

optional arguments:
  -h, --help        show this help message and exit
  --chunksize size  multipart_chunksize used for upload in bytes or with a
                    size suffix KB, MB, GB, or TB (default: 8MB)
```
