# CallHome database plugin for pyannote.database

# Discription
NIST SRE 2000 CallHome subset (the R65_8_1 folder).

This is *not* the whole CallHome corpora which were released by LDC under other references (among others https://catalog.ldc.upenn.edu/LDC2001S97), But this NIST SRE subset seems to be now widely refered as simply "CallHome" in the litterature, probably because it is referenced as such in the Kaldi recipes.

There are some specificities in this corpus: due to the fact that it is a recorded phone call, there are always 2 dominant speakers in each conversation (average is 2.57 speaker per file), and other speakers are coming from the same channel as either of the 2 main speakers. Also I didn't find the gender information in NIST SRE 2000 references and it would be interesting to know if this is same-gender or opposite-gender. We may have such information in the original CallHome references but the mapping is unknown.


## Installation

```bash
$ git clone https://github.com/yinruiqing/pyannote-db-callhome.git
$ pip install -e .
```

Tell `pyannote` where to look for CallHome audio files.

```bash
$ cat ~/.pyannote/db.yml
CallHome: /path/to/callhome/audio/original/{uri}.wav
```

CallHome database has only Test set for diarization protocol.

## Speaker diarization protocol


Protocol is initialized as follows:

```python
>>> from pyannote.database import get_protocol, FileFinder
>>> preprocessors = {'audio': FileFinder()}
>>> protocol = get_protocol('CallHome.SpeakerDiarization.All',
...                         preprocessors=preprocessors)
```

### Test / Evaluation

```python
>>> # initialize evaluation metric
>>> from pyannote.metrics.diarization import DiarizationErrorRate
>>> metric = DiarizationErrorRate()
>>>
>>> # iterate over each file of the test set
>>> for test_file in protocol.test():
...
...     # process test file
...     audio = test_file['audio']
...     hypothesis = process_file(audio)
...
...     # evaluate hypothesis
...     reference = test_file['annotation']
...     uem = test_file['annotated']
...     metric(reference, hypothesis, uem=uem)
>>>
>>> # report results
>>> metric.report(display=True)