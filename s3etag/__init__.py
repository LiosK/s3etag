# vim: set fileencoding=utf-8 :

from __future__ import annotations

import argparse
import hashlib
import re
import sys


def main() -> int:
    # parse arguments
    parser = argparse.ArgumentParser(description="s3etag - compute AWS S3 Etags")
    parser.add_argument("files", nargs="+", help="filenames")
    parser.add_argument(
        "--chunksize",
        metavar="size",
        default="8MB",
        type=parse_chunksize,
        help="multipart_chunksize used for upload in bytes or with a size suffix KB, MB, GB, or TB (default: 8MB)",
    )
    args = parser.parse_args()

    # loop given files
    n_errors = 0
    for filename in args.files:
        try:
            etag = compute_etag(filename, args.chunksize)
            print("{: <39s} {}".format(etag, filename), flush=True)
        except OSError as err:
            print("ERROR: {}".format(err), file=sys.stderr, flush=True)
            n_errors += 1

    return int(n_errors > 0)


def parse_chunksize(size: str) -> int:
    """Parse chunksize argument"""
    match = re.fullmatch(r"(\d+)([KMGT]B)?", size)
    if match is None:
        raise argparse.ArgumentTypeError("invalid size value: '{}'".format(size))
    num, suffix = match.groups("")
    return int(num) * (
        {
            "": 1,
            "KB": 1024**1,
            "MB": 1024**2,
            "GB": 1024**3,
            "TB": 1024**4,
        }[suffix]
    )


def compute_etag(filename: str, chunksize: int) -> str:
    """Compute Etag for a file"""
    with open(filename, "rb") as fh:
        buf = fh.read(chunksize)
        dgst_part = hashlib.md5(buf)
        buf = fh.read(chunksize)
        if len(buf) < 1:
            return dgst_part.hexdigest()

        count = 1
        dgst_whole = hashlib.md5(dgst_part.digest())
        while len(buf) > 0:
            count += 1
            dgst_part = hashlib.md5(buf)
            dgst_whole.update(dgst_part.digest())
            buf = fh.read(chunksize)
        return "{}-{}".format(dgst_whole.hexdigest(), count)
