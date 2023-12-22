'''
Tiny Audio Dataset, by our lab
'''

'''
The GTZAN dataset class, which extends the AudioDataset class
'''

from .dataset import Dataset
import json
import os
from typing import Callable, Optional
from .utils import download_file
import zipfile

class TAD(Dataset):
    subsets = ['all', 'train', 'valid', 'test']
    n_outputs = 24

    '''
    Annotations have them in 'sharp' while 'y' in dataset has them in 'flat' measure
    # means sharp
    C# = Db, D# = Eb, F# = Gb, G# = Ab, A# = Bb
    C sharp = D flat, D sharp = E flat
    '''
    classes = [c.lower() for c in [
        'C Major','C Minor','Db Major','Db Minor','D Major',
        'D Minor','Eb Major','Eb Minor','E Major','E Minor',
        'F Major','F Minor','Gb Major','Gb Minor','G Major',
        'G Minor','Ab Major','Ab Minor','A Major','A Minor',
        'Bb Major','Bb Minor','B Major','B Minor'
    ]]

    url = 'https://github.com/oriyonay/RandomPublicThings/raw/master/TAD.zip'
    
    def __init__(
        self, 
        dataroot: str, 
        n_samples: Optional[int] = 160000, 
        sr: Optional[int] = 16000, 
        transform: Optional[Callable] = None, 
        subset: str = 'all',
        return_labels: Optional[bool] = False,
        download: bool = True,
        **kwargs
    ):
        '''
        dataroot: where the data exists; will recursively traverse
        subset: the subset to load
        return_labels: should labels be returned?
        labels: (filename : label) pairs or None if unlabeled
        n_samples: number of samples to return
        sr: which sample rate to use? will resample if necessary
        transform: optional transform to signal
        '''
        super().__init__()

        assert subset in self.subsets

        self.dataroot = dataroot 
        self.subset = subset
        self.return_labels = return_labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        
        # download the data from self.url into dataroot
        if download:
            filename = download_file(self.url, os.path.join(self.dataroot, 'tad.zip'))

            zip_file = os.path.join(self.dataroot, filename)
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.dataroot)

            os.remove(zip_file)

        if not os.path.exists(os.path.join(self.dataroot, 'TAD')):
            print('Error: file does not exist. Use download=True to download dataset.')
            assert False

        # load filenames
        self.filenames = [
            os.path.join(self.dataroot, 'TAD', f'{i:03}.mp3') 
            for i in range(125)
        ]

        labels_json = os.path.join(self.dataroot, 'TAD', 'labels.json')
        with open(labels_json, 'r') as f:
            self.labels = json.load(f)

        # get split
        if self.subset.lower() == 'train':
            pass

    def get_signal(self, i):
        filename = self.filenames[i]
        return self.load_signal(filename)
        
    def get_label(self, i):
        return self.labels[i]
        
    def __len__(self):
        return len(self.filenames)