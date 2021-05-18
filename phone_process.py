from phonemizer import phonemize
import json

langs = ['es', 'it', 'fr', 'ky', 'nl', 'ru', 'sv', 'tr', 'tt', 'zh']
phone_lang = ['es', 'it', 'fr-fr', 'ky', 'nl', 'ru', 'sv', 'tr', 'tt', 'cmn']
# text = '就差當天沒直接訂'
# phone_seq = phonemize(text, language = 'cmn', backend = 'espeak')
# print(phone_seq)
# phone_seq = phone_seq.split()
# print(phone_seq)
# for lang in langs:
    
    # print(lang)
    # print(phonemize(text, language = lang, backend = 'espeak'))

# dict_path = '../common_voices_splits/zh/phonesMatches_reduced.json'

# with open(dict_path) as f:
#    IPA_dict = json.load(f)
# print(IPA_dict)

# label = []
# for phone in phone_seq: 
#     label.append(IPA_dict[phone])

# print(label)

IPA_dict = {}
start_idx = 0

for lang in langs:
    dict_path = '../common_voices_splits/'+lang+'/phonesMatches_reduced.json'

    with open(dict_path) as f:
        IPA_dict_new = json.load(f)

    for key in IPA_dict_new.keys():
        try: 
            x = IPA_dict[key]
        except KeyError : 
            IPA_dict[key] = start_idx
            start_idx += 1

print(IPA_dict)
print(len(IPA_dict))

reversed_IPA = {value : key for (key, value) in IPA_dict.items()}

print(reversed_IPA)



