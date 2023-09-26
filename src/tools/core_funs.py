from basic_module import *

def get_sentence_list_duration_ms(df, task_id=''):
    duration = (np.max(df['end_time']) - np.min(df['begin_time']))
    return int(duration)

def get_sentence_list_duration_s(df, task_id=''):
    duration = (np.max(df['end_time']) - np.min(df['begin_time'])) / 1000
    return float(duration)

def get_speak_duration_s(df,task_id=''):
    if df.shape[0]==0:
        return 0
    else:
        df = df[df['textLength']!=0].copy()
        duration = np.sum(df['end_time']-df['begin_time'])/1000
        return duration

def get_speak_speed_s(df, task_id=''):
    '''语速'''
    speak_duration = get_speak_duration_s(df)
    char_num = df.textLength.sum()
    speak_speed = char_num / speak_duration
    return float(speak_speed)


def get_sentence_num(df, task_id=''):
    '''句数'''
    return int(df.shape[0])


def get_sentence_average_length(df, task_id=''):
    '''平均句长'''
    return float(df.textLength.mean())


def get_pause_words_num(df, task_id=''):
    '''停顿词次数'''
    pause_words_num = df['text'].apply(lambda x: len(
        re_pauseword.findall(str(x))) > 0).sum()
    return int(pause_words_num)


def get_question_num(df, task_id=''):
    '''问句数量'''
    question_num = df['text'].apply(lambda x: True if len(
        re_question.findall(str(x))) > 0 else False).sum()
    return int(question_num)


def get_short_sentence_num(df, task_id=''):
    '''短句数量<3'''
    short_sentnce_num = df.textLength.apply(
        lambda x: True if x > 0 and x < 3 else False).sum()
    return int(short_sentnce_num)


def get_median_sentence_num(df, task_id=''):
    '''中句数量>=3 and <=10'''
    median_sentence_num = df.textLength.apply(
        lambda x: True if x >= 3 and x <= 10 else False).sum()
    return int(median_sentence_num)


def get_long_sentence_num(df, task_id=''):
    '''长句数量>10'''
    long_sentence_num = df.textLength.apply(
        lambda x: True if x > 10 else False).sum()
    return int(long_sentence_num)

def get_video_duration_ms(df,task_id=''):
    '''视频长度'''
    return get_sentence_list_duration_ms(df,task_id)

def get_voice_duration_ms(df,task_id=''):
    '''说话声音长度'''
    voice_duration_ms = df[df.textLength > 0].timeLength.sum()
    return int(voice_duration_ms)

def get_word_num(df,task_id=''):
    '''说话总字数'''
    word_num = df[df.textLength > 0].textLength.sum()
    return int(word_num)

def get_max_sent_word(df,task_id=''):
    '''单句最长字数'''
    max_sent_word = df[df.textLength > 0].textLength.max()
    return int(max_sent_word)

def get_interaction_score(df, task_id=''):
    t = get_sentence_list_duration_s(df)
    k = get_sentence_num(df)
    k1 = get_short_sentence_num(df)
    k2 = get_median_sentence_num(df)
    k3 = get_long_sentence_num(df)
    m = get_question_num(df)
    v_speak_num = 1 if k / t > 0.063 else 0
    v_duration = 1 if (k1 + k2 * 3 + k3 * 6) / t > 0.27 else 0
    v_question = 1 if m / t * 100 > 0.896 else 0
    if v_speak_num and v_duration and v_question:
        level = 0
    if v_speak_num and v_duration and not v_question:
        level = 1
    if v_speak_num and not v_duration:
        level = 2
    if not v_speak_num:
        level = 3
    return level

def get_umm_ahh_num(df, task_id=''):
    '''单句最长字数'''
    umm_ahh_count = df['text'].apply(
        lambda x: len(re.sub(r'[^\w]|_','',str(x))) == 1 and 
        re.sub(r'[^\w]|_','',str(x)) in ['嗯','恩','阿','啊']).sum()
    return int(umm_ahh_count)