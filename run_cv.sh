
PATH_COMMON_VOICES=''
CHECKPOINT_TO_TEST=''
OUTPUT_DIR=''

python3 cpc/eval/common_voices_eval.py train ${PATH_COMMON_VOICES}/es/clips_16k \
    ${PATH_COMMON_VOICES}/es/validated_phones_reduced.txt ${CHECKPOINT_TO_TEST} \
    --pathTrain ${PATH_COMMON_VOICES}/es/trainSeqs_5.0_uniform_new_version.txt \
    --pathVal ${PATH_COMMON_VOICES}/es/trainSeqs_5.0_uniform_new_version.txt \
    --freeze -o ${OUTPUT_DIR}
