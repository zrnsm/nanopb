'''This file dynamically builds the proto definitions for Python.'''
from __future__ import absolute_import

import os.path
import sys
import tempfile
import shutil

import pkg_resources

# Compatibility layer to make TemporaryDirectory() available on Python 2.

try:
    from tempfile import TemporaryDirectory
except ImportError:
    class TemporaryDirectory:
        '''TemporaryDirectory fallback for Python 2'''
        def __enter__(self, prefix = 'tmp'):
            self.dir = tempfile.mkdtemp(prefix = prefix)
            return self.dir

        def __exit__(self, *args):
            shutil.rmtree(self.dir)

# The code below tries two methods for importing the definitions from nanopb.proto:
# 1) If nanopb.proto source file is available, build it using protoc to a temporary directory.
# 2) Otherwise, try importing a precompiled file.

from ._utils import has_grpcio_protoc, invoke_protoc

# First, try to dynamically build and load the .proto file
build_error = None
proto_ok = False
dirname = os.path.dirname(__file__)
protosrc = os.path.join(dirname, "nanopb.proto")
if os.path.isfile(protosrc):
    tmpdir = tempfile.mkdtemp(prefix="nanopb-")

    try:
        with TemporaryDirectory(prefix = 'nanopb-') as tmpdir:
            cmd = ["protoc",
                   "--python_out={}".format(tmpdir),
                   protosrc,
                   "-I={}".format(dirname),
                  ]

            invoke_protoc(argv=cmd)
            sys.path.insert(0, tmpdir)
            import nanopb_pb2
            proto_ok = True
    except e:
        build_error = e

# As a fallback, see if we have a prebuilt file available
import_error = None
if not proto_ok:
    try:
        from . import nanopb_pb2
        proto_ok = True
    except ImportError:
        pass # To be expected
    except:
        import_error = e

if not proto_ok:
    sys.stderr.write("Failed to build/import nanopb_pb2.py.\n")
    raise build_error or import_error or Exception("Failed to build/import nanopb_pb2.py.\n")
