from abc import abstractmethod
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd


class SpectralLibrary:
    """Main to initialze a SpectralLibrary obj."""

    def __init__(
        self,
        input_dataframe: pd.DataFrame,
        grpc_dict: dict,
        output_path: Union[str, Path],
        min_intensity_threshold: Optional[float] = 0.05,
        chunksize: Optional[int] = None,
    ):
        """
        Initialize a SpectralLibrary obj.

        :param input_dataframe: dataframe of sequences, charges, and masses of all library peptides
        :param grpc_dict: GRPC client output dictionary with spectrum, irt, and proteotypicity prediction
        :param output_path: path to output file including file name
        :param min_intensity_threshold: optional filter for low intensity peaks
        :param chunksize: optional chunksize for dlib
        """
        if isinstance(output_path, str):
            output_path = Path(output_path)
        self.spectra_input = input_dataframe
        self.grpc_output = grpc_dict
        self.out_path = output_path
        self.min_intensity_threshold = min_intensity_threshold
        self.chunksize = chunksize

    def load(self):
        """Load predictions from hdf5 file."""

    @abstractmethod
    def write(self):
        """Write predictions."""
        pass

    @abstractmethod
    def prepare_spectrum(self):
        """Prepare spectrum."""
        pass
