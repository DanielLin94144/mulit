import argparse
import os
import torchaudio
from copy import deepcopy
import torch
import time
import random
import math
import json
import subprocess
import sys
import progressbar
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from torch.multiprocessing import Pool
from cv_dataset import findAllSeqs, parseSeqLabels, filterSeqs
from Common_voice import SingleSequenceDataset 
from torch.utils.data import Dataset, DataLoader

if __name__ == '__main__':

    pathDB = '/home/daniel094144/Daniel/data/CommonVoice/es/clips_16k'    
    pathPhone = '/home/daniel094144/Daniel/data/CommonVoice/es/reduced_global_IPA.txt'
    file_extension = '.mp3'
    in_dim = 1
    pathTrain = '/home/daniel094144/Daniel/common_voices_splits/es/trainSeqs_5.0_uniform_new_version.txt'
    batchSize = 4
    '''
    variable setting

        - pathDB: Path to the directory containing the audio data / pre-computed features.
        - PathPhone: Path to the .txt file containing the phone transcription.
        - in_dim: Dimension of the input data, useful when working with 
                        pre-computed features or stereo audio.
        - pathTrain: Path to the .txt files containing the list of the training sequences.                       
    '''

    inSeqs, _ = findAllSeqs(pathDB,
                            extension=file_extension)
    
    phoneLabels, nPhones = parseSeqLabels(pathPhone)

    seqTrain = filterSeqs(pathTrain, inSeqs)
    print(seqTrain)
    print(f"Loading the training dataset at {pathDB}")

    datasetTrain = SingleSequenceDataset(pathDB, seqTrain,
                                            phoneLabels, inDim=in_dim)

    train_loader = DataLoader(datasetTrain, batch_size=batchSize,
                                shuffle=True)