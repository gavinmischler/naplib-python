import pytest
import numpy as np
import os

from naplib.io import read_cnd
import naplib as nl

def test_read_cnd_file():

    curr_dir = os.path.dirname(__file__)
    file = os.path.join(curr_dir, 'dataSub1.mat')
    data = read_cnd(file)

    assert isinstance(data, nl.Data)

    assert len(data) == 20

    assert data.fields == ['dataType', 'deviceName', 'origTrialPosition', 'fs', 'extChan', 'eeg', 'stimIdxs', 'Speech Envelope Vectors', 'Word Onset Vectors', 'Spectrogram', 'Phonetic Features', 'condIdxs', 'fs_stim']

    test_entered_loop = False
    for t, trial in enumerate(data):
        test_entered_loop = True
        assert trial['condIdxs'] == 1
        assert trial['origTrialPosition'] == t
        assert trial['stimIdxs'] == t
        assert trial['eeg'].shape == (11,4)
        assert trial['fs'] == 128
        assert trial['Speech Envelope Vectors'].shape == (11,)
        assert trial['Word Onset Vectors'].shape == (11,)
        assert trial['Spectrogram'].shape == (11,16)
        assert trial['Phonetic Features'].shape == (11,19)
        assert trial['fs_stim'] == 128
        assert trial['dataType'] == 'EEG'
        assert trial['deviceName'] == 'BioSemi'
        assert trial['extChan'].shape == (11,2)

    assert test_entered_loop


def test_read_cnd_file_nostim():

    curr_dir = os.path.dirname(__file__)
    file = os.path.join(curr_dir, 'dataSub1.mat')
    data = read_cnd(file, load_stims=False)

    assert isinstance(data, nl.Data)

    assert len(data) == 20

    assert data.fields == ['dataType', 'deviceName', 'origTrialPosition', 'fs', 'extChan', 'eeg']

    test_entered_loop = False
    for t, trial in enumerate(data):
        test_entered_loop = True
        assert trial['origTrialPosition'] == t
        assert trial['eeg'].shape == (11,4)
        assert trial['fs'] == 128
        assert trial['dataType'] == 'EEG'
        assert trial['deviceName'] == 'BioSemi'
        assert trial['extChan'].shape == (11,2)

    assert test_entered_loop

def test_read_cnd_file_onlystim():

    curr_dir = os.path.dirname(__file__)
    file = os.path.join(curr_dir, 'dataStim.mat')
    data = read_cnd(file, load_stims=False)

    assert isinstance(data, nl.Data)

    assert len(data) == 20

    assert data.fields == ['stimIdxs', 'Speech Envelope Vectors', 'Word Onset Vectors', 'Spectrogram', 'Phonetic Features', 'condIdxs', 'fs_stim']

    test_entered_loop = False
    for t, trial in enumerate(data):
        test_entered_loop = True
        assert trial['Speech Envelope Vectors'].shape == (11,)
        assert trial['Word Onset Vectors'].shape == (11,)
        assert trial['Spectrogram'].shape == (11,16)
        assert trial['Phonetic Features'].shape == (11,19)
        assert trial['fs_stim'] == 128

    assert test_entered_loop