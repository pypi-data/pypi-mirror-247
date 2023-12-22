"""
Collection of pytest fixtures that are accessible to all the pytests in this directory
"""

import pathlib

import pytest

from pyscreech.audio import AudioWaveform
from pyscreech.stipa import StipaCalculator
from pyscreech.stoi import StoiCalculator
from pyscreech.wer import WerCalculator


def recording_filename(filename):
    resources_dir = pathlib.Path(__file__).parent.parent / 'resources'
    return f'{resources_dir}/{filename}'


@pytest.fixture(scope="session")
def reference_stipa_waveform():
    reference_filename = recording_filename("StipaV5_CEA.wav")
    return AudioWaveform.load_audio(reference_filename)

@pytest.fixture(scope="session")
def stipa_calculator():
    return StipaCalculator()

@pytest.fixture(scope="session")
def stoi_calculator():
    return StoiCalculator()


