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

def load(path_item):
    seq_name = path_item.stem
    data = torchaudio.load(str(path_item))[0].view(1, -1)
    return seq_name, data


class SingleSequenceDataset(Dataset):

    def __init__(self,
                 pathDB,
                 seqNames,
                 phoneLabelsDict,
                 inDim=1,
                 transpose=True):
        """
        Args:
            - path (string): path to the training dataset
            - sizeWindow (int): size of the sliding window
            - seqNames (list): sequences to load
            - phoneLabels (dictionnary): if not None, a dictionnary with the
                                         following entries
                                         "step": size of a labelled window
                                         "$SEQ_NAME": list of phonem labels for
                                         the sequence $SEQ_NAME
        """
        self.seqNames = deepcopy(seqNames)
        self.pathDB = pathDB
        self.phoneLabelsDict = deepcopy(phoneLabelsDict)
        self.inDim = inDim
        self.transpose = transpose
        self.loadSeqs()

    def loadSeqs(self):

        # Labels
        self.seqOffset = [0]
        self.phoneLabels = []
        self.phoneOffsets = [0]
        self.data = []
        self.maxSize = 0
        self.maxSizePhone = 0

        # Data

        nprocess = min(30, len(self.seqNames))

        start_time = time.time()
        to_load = [Path(self.pathDB) / x for _, x in self.seqNames]

        with Pool(nprocess) as p:
            poolData = p.map(load, to_load)

        tmpData = []
        poolData.sort()

        totSize = 0
        minSizePhone = float('inf')
        for seqName, seq in poolData:
            self.phoneLabels += self.phoneLabelsDict[seqName]
            self.phoneOffsets.append(len(self.phoneLabels))
            self.maxSizePhone = max(self.maxSizePhone, len(
                self.phoneLabelsDict[seqName]))
            minSizePhone = min(minSizePhone, len(
                self.phoneLabelsDict[seqName]))
            sizeSeq = seq.size(1)
            self.maxSize = max(self.maxSize, sizeSeq)
            totSize += sizeSeq
            tmpData.append(seq)
            self.seqOffset.append(self.seqOffset[-1] + sizeSeq)
            del seq
        self.data = torch.cat(tmpData, dim=1)
        self.phoneLabels = torch.tensor(self.phoneLabels, dtype=torch.long)
        print(f'Loaded {len(self.phoneOffsets)} sequences '
              f'in {time.time() - start_time:.2f} seconds')
        print(f'maxSizeSeq : {self.maxSize}')
        print(f'maxSizePhone : {self.maxSizePhone}')
        print(f"minSizePhone : {minSizePhone}")
        print(f'Total size dataset {totSize / (16000 * 3600)} hours')

    def __getitem__(self, idx):

        offsetStart = self.seqOffset[idx]
        offsetEnd = self.seqOffset[idx+1]
        offsetPhoneStart = self.phoneOffsets[idx]
        offsetPhoneEnd = self.phoneOffsets[idx + 1]

        sizeSeq = int(offsetEnd - offsetStart)
        sizePhone = int(offsetPhoneEnd - offsetPhoneStart)

        outSeq = torch.zeros((self.inDim, self.maxSize))
        outPhone = torch.zeros((self.maxSizePhone))

        outSeq[:, :sizeSeq] = self.data[:, offsetStart:offsetEnd]
        outPhone[:sizePhone] = self.phoneLabels[offsetPhoneStart:offsetPhoneEnd]

        return outSeq,  torch.tensor([sizeSeq], dtype=torch.long), outPhone.long(),  torch.tensor([sizePhone], dtype=torch.long)

    def __len__(self):
        return len(self.seqOffset) - 1