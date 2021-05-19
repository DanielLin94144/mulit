import json
from tqdm import tqdm

# well_lang = ['es', 'it', 'fr', 'ru']
# low_lang = ['ky', 'nl', 'sv', 'tr', 'tt', 'zh']

langs = ['es', 'it', 'fr', 'ru', 'ky', 'nl', 'sv', 'tr', 'tt', 'zh']

global_dict_path = './global_IPA.json'
phone_label_filename = 'validated_phones_reduced.txt'

# import global IPA dictionary
with open(global_dict_path) as f:
    global_IPA_dict = json.load(f)

# read the phone label from 'validated_phones_reduced.txt'
def parseSeqLabels(pathLabels):
    with open(pathLabels, 'r') as f:
        lines = f.readlines()
    output = {} 
    maxPhone = 0
    for line in lines:
        data = line.split()
        output[data[0]] = [int(x) for x in data[1:]]
        maxPhone = max(maxPhone, max(output[data[0]]))
    return output, maxPhone

# transform to global IPA label for each languages
for lang in langs:
    dict_path = '../common_voices_splits/'+lang+'/phonesMatches_reduced.json'
    with open(dict_path) as f:
        IPA_dict_new = json.load(f)
    reversed_IPA = {value : key for (key, value) in IPA_dict_new.items()}
    pathLabels = '../common_voices_splits/'+lang+'/'+phone_label_filename
    seq_label_dict, numPhone = parseSeqLabels(pathLabels)
    global_seq_label_dict = {}

    save_label_filename = '../common_voices_splits/'+lang+'/reduced_global_IPA.txt'
    with open(save_label_filename, 'w') as f:
        print('[INFO]   start writing global IPA label for '+ lang)
        for filename, seq_label in tqdm(seq_label_dict.items()):
            global_IPA = [global_IPA_dict[reversed_IPA[x]] for x in seq_label]
            # global_seq_label_dict[filename] = global_IPA
            # writing txt file 
            f.write(filename)
            for label in global_IPA: 
                f.write(' '+str(label))
            f.write('\n')
    
        
    


