import pandas as pd
from phonemizer import phonemize

df = pd.read_csv('/home/daniel094144/Daniel/data/CommonVoice/zh-TW/validated.tsv', sep='\t')
df['phoneme'] = df['sentence']


numfail = 0
for i in range(1, 1000):
    # print(df['phoneme'][i])
    
    try:
        df['phoneme'][i] = phonemize(df['sentence'][i], language = 'cmn', backend = 'espeak')
    except RuntimeError: 
        df['phoneme'][i] = None
        numfail += 1

print(numfail)
