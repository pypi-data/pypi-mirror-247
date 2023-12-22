"""Methods used for calculating Word Error Rate (WER)"""
import os

from loguru import logger

from .audio import AudioWaveform
from .score import ScoreCalculator

import whisper
from jiwer import wer


class WerCalculationException(Exception):
    pass


class WerCalculator(ScoreCalculator):
    """ Word Error Rate (WER) calculator class"""

    def __init__(self, model='medium.en'):
        """
        Initialize WER calculator

        Args:
            model (str): name of the whisper AI model to use for speech to text transcription. See
                https://github.com/openai/whisper for details
        """

        logger.info(f"Loading WhisperAI's {model} model...")
        self.model = whisper.load_model(model)
        logger.info(f"...done")

    @staticmethod
    def format_transcription(transcription_str: str) -> str:
        """
        Formats transcriptions to remove line endings, capitalization, periods and commas

        Args:
            transcription_str (str): the text to format
        Returns:
            Formatted text string
        """
        transcript = transcription_str
        transcript = transcript.replace('\n', '')  # Remove all new lines
        transcript = transcript.lower()  # Convert everything to lowercase
        transcript = transcript.replace('.', ' ')
        transcript = transcript.replace(',', ' ')

        return transcript

    def audio_file_to_text(self, filename: str, extra_formatting: bool = True) -> str:
        """
        Transcribe an audio file to text using Whisper AI

        Args:
            filename (str): the location of the file to transcribe
            extra_formatting (bool): whether to format the transcription to remove punctuation, line endings, etc.
        Returns:
            The transcribed text
        """

        results = self.model.transcribe(filename)

        if extra_formatting:
            return self.format_transcription(results['text'])
        else:
            return results['text']

    def audio_waveform_to_text(self, waveform: AudioWaveform, extra_formatting: bool = True) -> str:
        """
        Transcribe an audio waveform to text by first writing it to file and then using Whisper AI to transcribe it

        Args:
            waveform (AudioWaveform): AudioWaveform to transcribe
            extra_formatting (bool): whether to format the transcription to remove punctuation, line endings, etc.
        Returns:
            The transcribed text
        """

        # Whisper AI assumes 16 kHz sampling rate for numpy arrays. Resample if required
        if waveform.sample_rate != 16000:
            logger.info(f"Waveform {waveform.name} being resampled to 16kHz from {waveform.sample_rate/1000:.0f} kHz")
            waveform_to_transcribe = waveform.resample(new_sample_rate=16000)
        else:
            waveform_to_transcribe = waveform

        results = self.model.transcribe(waveform_to_transcribe.timeseries)

        if extra_formatting:
            return self.format_transcription(results['text'])
        else:
            return results['text']

    def calculate_score_from_single_waveform(self,
                                             input_waveform: AudioWaveform,
                                             reference_text: str,
                                             extra_formatting: bool = True,
                                             log_details: bool = False) -> float:
        """
        Calculate Word Error Rate for a single waveform by comparing to reference text. If data are in the form of
        two AudioWaveforms, WerCalculator.calculate_score_from_waveforms should be used

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_text (str): reference text against which to compare the transcribed input_waveform text
            extra_formatting (bool): whether to format the transcription to remove punctuation, line endings, etc.
            log_details (bool): logs transcripts of waveform that went into calculation

        Returns:
            A single calculated WER
        """

        transcription_test = self.audio_waveform_to_text(waveform=input_waveform,
                                                         extra_formatting=extra_formatting)

        if reference_text == "":
            logger.warning(f"Reference text is empty")
        if transcription_test == "":
            logger.warning(f"Test text is empty")

        score = wer(reference_text, transcription_test)

        if log_details:
            logger.info(f"Reference text: {reference_text}")
            logger.info(f"Test text:      {transcription_test}")
            logger.info(f"WER:            {score}")

        return score

    def calculate_score_from_waveforms(self,
                                       input_waveform: AudioWaveform,
                                       reference_waveform: AudioWaveform,
                                       extra_formatting: bool = True,
                                       log_details: bool = False,
                                       **kwargs) -> float:
        """
        Calculate Word Error Rate by comparing data in the form of two AudioWaveforms

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_waveform (AudioWaveform): reference waveform against which to compare the transcribed
                input_waveform text
            extra_formatting (bool): whether to format the transcription to remove punctuation, line endings, etc.
            log_details (bool): logs transcripts of waveform that went into calculation

        Returns:
            A single calculated WER
        """

        if len(kwargs) > 0:
            logger.info(f"Ignoring extra kwargs passed in: {kwargs}")

        transcription_reference = self.audio_waveform_to_text(waveform=reference_waveform,
                                                              extra_formatting=extra_formatting)

        return self.calculate_score_from_single_waveform(input_waveform=input_waveform,
                                                         reference_text=transcription_reference,
                                                         extra_formatting=extra_formatting,
                                                         log_details=log_details)
