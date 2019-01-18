#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import os.path as op
from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol
from pyannote.parser import MDTMParser

# this protocol defines a speaker diarization protocol: as such, a few methods
# needs to be defined: trn_iter, dev_iter, and tst_iter.

class SpeakerDiarization(SpeakerDiarizationProtocol):
    """My first speaker diarization protocol """

    def trn_iter(self):
        for _ in []:
            yield


    


    def dev_iter(self):
        # here, you should do the same as above, but for the development set
        for _ in []:
            yield

    def tst_iter(self):
        # absolute path to 'data' directory where annotations are stored
        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')

        annotations = MDTMParser().read(
            op.join(data_dir, 'fullref.mdtm'))

        # iterate over each file in training set
        for uri in sorted(annotations.uris):

            # get annotations as pyannote.core.Annotation instance
            annotation = annotations(uri)

            # `trn_iter` (as well as `dev_iter` and `tst_iter`) are expected
            # to yield dictionary with the following fields:
            yield {
                # name of the database class
                'database': 'CallHome',
                # unique file identifier
                'uri': uri,
                # reference as pyannote.core.Annotation instance
                'annotation': annotation,
                # annotated part as pyannote.core.Timeline instance
                'annotated': annotation.get_timeline().extent()
            }

# this is where we define each protocol for this database.
# without this, `pyannote.database.get_protocol` won't be able to find them...

class CallHome(Database):
    """MyDatabase database"""

    def __init__(self, preprocessors={}, **kwargs):
        super(CallHome, self).__init__(preprocessors=preprocessors, **kwargs)

        # register the first protocol: it will be known as
        # MyDatabase.SpeakerDiarization.MyFirstProtocol
        self.register_protocol(
            'SpeakerDiarization', 'All', SpeakerDiarization)
