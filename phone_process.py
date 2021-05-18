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


dict_path = '../common_voices_splits/'+'zh'+'/phonesMatches_reduced.json'

with open(dict_path) as f:
    IPA_dict_new = json.load(f)

reversed_IPA = {value : key for (key, value) in IPA_dict_new.items()}
print(reversed_IPA)

phone_label_ori = '13 16 6 31 2 0 16 2 13 26 37 25 6 7 22 32 3 33 35 3 28 23 12 20 21 28 23 6 7 20 21 '
phone_label_ori = phone_label_ori.split()
phone_label_ori = list(map(int, phone_label_ori))
print(phone_label_ori)
global_IPA = []
for ori_label in phone_label_ori:
    global_IPA.append(IPA_dict[reversed_IPA[ori_label]])
print(global_IPA)



# with open('./global_IPA.json', 'w') as outfile:
#     json.dump(IPA_dict, outfile)

NumPhone = len(IPA_dict)
for lang in langs:
    i = 0
    dict_path = '../common_voices_splits/'+lang+'/phonesMatches_reduced.json'
    with open(dict_path) as f:
        IPA_dict_new = json.load(f)
    for key in IPA_dict_new.keys():
        if IPA_dict[key]:
            i += 1
    print(lang + ': contains '+ str(i))

well = 0
visited = {}
for key in IPA_dict.keys():
    visited[key] = 0

for lang in ['es', 'fr', 'it', 'zh']:
    dict_path = '../common_voices_splits/'+lang+'/phonesMatches_reduced.json'
    with open(dict_path) as f:
        IPA_dict_new = json.load(f)
    for key in IPA_dict_new.keys():
        if IPA_dict[key] and visited[key] == 0:
            i += 1
            visited[key] = 1

print('es, it, fr contain '+ str(i) + ' IPAs')

for lang in ['ky', 'nl', 'ru', 'sv', 'tr', 'tt']:
    unseen = 0
    dict_path = '../common_voices_splits/'+lang+'/phonesMatches_reduced.json'
    with open(dict_path) as f:
        IPA_dict_new = json.load(f)
    for key in IPA_dict_new.keys():
        if visited[key] == 0:
            unseen += 1
    print(lang + ' contains ', str(unseen), ' unseen IPA on for well resource')

