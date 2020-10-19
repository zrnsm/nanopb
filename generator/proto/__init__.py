'''This file dynamically builds the proto definitions for Python.'''
from __future__ import absolute_import

import os.path
import sys
import tempfile
import shutil

import pkg_resources

from ._utils import has_grpcio_protoc, invoke_protoc

dirname = os.path.dirname(__file__)
protosrc = os.path.join(dirname, "nanopb.proto")
protodst = os.path.join(dirname, "nanopb_pb2.py")

# First, try to dynamically build and load the .proto file
error_build = None
proto_ok = False
if os.path.isfile(protosrc):
    tmpdir = tempfile.mkdtemp(prefix="nanopb-")

    try:
        cmd = [
            "protoc",
            "--python_out={}".format(tmpdir),
            protosrc,
            "-I={}".format(dirname),
        ]

        invoke_protoc(argv=cmd)

        sys.path.insert(0, tmpdir)
        import nanopb_pb2

        proto_ok = True
    except e:
        error_build = e
    finally:
        shutil.rmtree(tmpdir)

# As a fallback, see if we have a prebuilt file available
error_import = None
if not proto_ok:
    try:
        import nanopb_pb2
        proto_ok = True
    except:
        error_import = e

if not proto_ok:
    sys.stderr.write("Failed to build/import nanopb_pb2.py.\n")
    sys.stderr.write("\n\nBuild error: %s\n" % error_build)
    sys.stderr.write("\n\nDirect import error: %s\n" % error_import)
    raise Exception("Failed to build/import nanopb_pb2.py.\n")
