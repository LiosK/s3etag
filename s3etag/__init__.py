# vim: set fileencoding=utf-8 :

import argparse
import hashlib
import re
import sys
import os
import pathlib


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description="s3etag - compute AWS S3 Etags"
    )
    parser.add_argument("files", nargs="+", help="filenames")
    parser.add_argument(
        "-t", "--threshhold",
        metavar="size",
        default="8MB",
        type=parse_chunksize,
        help="threshhold to apply multipart md5 calculation in bytes "
             "or with a size suffix KB, MB, GB, or TB (default: 8MB)"
    )
    parser.add_argument(
        "-c", "--chunksize",
        metavar="size",
        default="8MB",
        type=parse_chunksize,
        help="multipart_chunksize used for upload in bytes "
             "or with a size suffix KB, MB, GB, or TB (default: 8MB)"
    )
    args = parser.parse_args()

    # loop given files
    for f in args.files:
        etag = calc_s3_etag(f, args.threshhold, args.chunksize)
        print("{: <39s} {}".format(etag, f), flush=True)


def parse_chunksize(size):
    """Parse chunksize argument"""
    match = re.fullmatch(r"(\d+)([KMGT]B)?", size)
    if match is None:
        raise argparse.ArgumentTypeError(
            "invalid size value: '{}'".format(size)
        )
    num, suffix = match.groups("")
    return int(num) * (
        {
            "": 1,
            "KB": 1024 ** 1,
            "MB": 1024 ** 2,
            "GB": 1024 ** 3,
            "TB": 1024 ** 4,
        }[suffix]
    )


def calc_s3_etag(filename, threshhold, chunksize):
    """Compute and print Etag for a file"""
    if isinstance(filename, pathlib.PosixPath):
        filesize = filename.stat().st_size
    elif isinstance(filename, str):
        filesize = os.path.getsize(filename)
    else:
        print("invalid filename", sys.stderr)

    if filesize <= threshhold:
        try:
            with open(filename, "rb") as fh:
                buf = fh.read()
                etag = hashlib.md5(buf).hexdigest()
        except OSError as err:
            print("ERROR: {}".format(err), file=sys.stderr, flush=True)
            return err.errno

    else:
        count = 0
        dgst_part = hashlib.md5()
        dgst_whole = hashlib.md5()
        try:
            with open(filename, "rb") as fh:
                while True:
                    buf = fh.read(chunksize)
                    if len(buf) < 1:
                        break
                    count = count + 1
                    dgst_part = hashlib.md5(buf)
                    dgst_whole.update(dgst_part.digest())
        except OSError as err:
            print("ERROR: {}".format(err), file=sys.stderr, flush=True)
            return err.errno

        etag = (
            "{}-{}".format(dgst_whole.hexdigest(), count)
            if count > 1
            else dgst_part.hexdigest()
        )

    return etag
