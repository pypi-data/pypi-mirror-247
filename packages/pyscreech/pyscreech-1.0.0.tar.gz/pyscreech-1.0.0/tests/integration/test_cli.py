import numpy as np
import pytest

from pyscreech.cli import main, scores
from tests.conftest import recording_filename

from loguru import logger


@pytest.mark.parametrize('score_type', scores)
@pytest.mark.parametrize('print_all_scores', [True, False])
@pytest.mark.parametrize('randomize', [True, False])
@pytest.mark.parametrize('sync_waveforms', [True, False])
def test_cli(score_type, print_all_scores, randomize, sync_waveforms):

    if score_type == "STIPA":
        recording = recording_filename("StipaV5_CEA.wav")
        num_segments = 3
        duration = 5
    else:
        recording = recording_filename("harvard_set1_12sec.wav")
        num_segments = 1
        duration = 0

    starting_offset = 0
    butter_order = 2
    corner_frequency = None
    hamming_time = None

    logger.info("\n")
    logger.info(f"score_type={score_type}, randomize={randomize}, sync_waveforms={sync_waveforms}")

    score_result = main(score_type=score_type,
                        recording=recording,
                        reference=recording,
                        starting_offset=starting_offset,
                        duration=duration,
                        num_segments=num_segments,
                        sync_waveforms=sync_waveforms,
                        sync_std=False,
                        randomize=randomize,
                        print_all_scores=print_all_scores,
                        butter_order=butter_order,
                        corner_frequency=corner_frequency,
                        hamming_time=hamming_time,
                        log_details=True)

    if score_type == 'STIPA' and randomize and not sync_waveforms:
        # 0.88 should be pretty safe here for a random 5-second segment
        assert np.all(score_result > 0.88)
    elif score_type == 'WER':
        assert np.allclose(score_result, 0.0)
    else:
        assert np.allclose(score_result, 1.0)
