# DIR_CC=$PATH_COMMON_VOICES
DIR_CC='/home/daniel094144/Daniel/data/CommonVoice'
# for x in fr zh it ru nl sv es tr tt ky; do python adjust_sample_rate.py ${DIR_CC}/${x}/clips ${DIR_CC}/${x}/validated_phones_reduced.txt ${DIR_CC}/${x}/clips_16k; done
for x in zh-TW; do python3 adjust_sample_rate.py ${DIR_CC}/${x}/clips ${DIR_CC}/${x}/validated_phones_reduced.txt ${DIR_CC}/${x}/clips_16k; done