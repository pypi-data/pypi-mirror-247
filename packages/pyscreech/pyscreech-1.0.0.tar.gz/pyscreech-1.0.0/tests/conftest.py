"""
Collection of pytest fixtures that are accessible to all the pytests in this directory
"""
import os
import pathlib

import pytest

from pyscreech.audio import AudioWaveform
from pyscreech.stipa import StipaCalculator
from pyscreech.stoi import StoiCalculator
from loguru import logger
from _pytest.logging import LogCaptureFixture

from pyscreech.wer import WerCalculator


def recording_filename(filename):
    resource_filename = os.path.join(pathlib.Path(__file__).parents[1], 'tests', 'resources', filename)
    return resource_filename


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


@pytest.fixture(scope="session")
def wer_calculator():
    return WerCalculator()


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)
