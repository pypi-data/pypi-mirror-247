"""Tests of wer.py"""

from tests.conftest import recording_filename
from pyscreech.audio import AudioWaveform


def test_calculate_wer_from_waveforms(wer_calculator):

    filename = recording_filename("harvard_set1_12sec.wav")
    ref_text = wer_calculator.audio_file_to_text(filename=filename)
    assert 'the birch canoe slid on the smoothie' in ref_text

    ref_wf = AudioWaveform.load_audio(filename)
    ref_text = wer_calculator.audio_waveform_to_text(waveform=ref_wf)
    assert 'the birch canoe slid on the smoothie' in ref_text

    test_wf = ref_wf.resample(new_sample_rate=4000)

    score_unmodified = wer_calculator.calculate_score_from_waveforms(input_waveform=ref_wf,
                                                                     reference_waveform=ref_wf)

    # no modification so error should be 0
    assert score_unmodified == 0.0

    score_resampled = wer_calculator.calculate_score_from_waveforms(input_waveform=test_wf,
                                                                    reference_waveform=ref_wf)

    # the resampled version has non-zero WER
    assert round(score_resampled, 3) == 0.091

    # pass in reference text instead of full waveform and nothing should change
    score_resampled_single_waveform = wer_calculator.calculate_score_from_single_waveform(input_waveform=test_wf,
                                                                                          reference_text=ref_text)
    assert round(score_resampled_single_waveform, 3) == 0.091

