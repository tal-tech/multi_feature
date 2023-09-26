from basic_module import *


def get_jsonStr_duration(jsonStr):
    text_list = jsonStr
    if len(text_list) == 0:
        return 0
    else:
        duration = int(text_list[-1]['end_time'])
        return duration


def change_input_2_godeye(student_json, teacher_json, student_start_at=0, teacher_start_at=0, subject=12, task_id=''):
    jsonStr = {
        "class": {
            "first_start_at": min(student_start_at, teacher_start_at),
            "last_end_at": 0,
            "subject": subject,
            "id": task_id
        },
        "student": {
            "duration": get_jsonStr_duration(student_json),
            "start_time_ms": student_start_at,
            "text": student_json
        },
        "teacher": {
            "duration": 0,
            "start_time_ms": teacher_start_at,
            "text": []
        }
    }

    if teacher_json is None:
        jsonStr['teacher'] = {}
        jsonStr['class']['last_end_at'] = jsonStr['class']['first_start_at'] + jsonStr['student']['duration']

    else:
        jsonStr['teacher']['duration'] = get_jsonStr_duration(teacher_json)
        jsonStr['class']['last_end_at'] = jsonStr['class']['first_start_at'] + min(jsonStr['student']['duration'],
                                                                                   jsonStr['teacher']['duration'])
        jsonStr['teacher']['text'] = teacher_json
    return jsonStr


def parse_list_2_df(text, task_id=''):
    error_code = default_error_code
    error_message = default_error_message
    df = None
    if len(text) == 0:
        error_code = text_empty
        logger.info('task_id:{},input text len is 0'.format(task_id))
        return error_code, error_message, df
    else:
        try:
            df = pd.DataFrame(text)
            df['begin_time'] = df['begin_time'].astype(np.int32)
            df['end_time'] = df['end_time'].astype(np.int32)
            df['sentence_id'] = range(1, df.shape[0] + 1)
            df['timeLength'] = df.end_time - df.begin_time
            df['textLength'] = df.text.apply(lambda x: get_text_len(x))
        except:
            logger.error('task_id:{},input format error,detail is{}'.format(task_id, traceback.format_exc()))
            error_code = input_error
        return error_code, error_message, df


def get_word_list(s1):  
    # 把句子按字分开，中文按字分，英文按单词，数字按空格  
    regEx = re.compile('[\\W]{1,}')    # 我们可以使用正则表达式来切分句子，切分的规则是除单词，数字外的任意字符串  
    res = re.compile(r"([\u4e00-\u9fa5])")    #  [\u4e00-\u9fa5]中文范围  
    p1 = regEx.split(s1.lower())  
    str1_list = []  
    for str in p1:  
        if res.split(str) == None:  
            str1_list.append(str)  
        else:  
            ret = res.split(str)  
            for ch in ret:  
                str1_list.append(ch)  
    list_word1 = [w for w in str1_list if len(w.strip()) > 0]  # 去掉为空的字符  
    return  list_word1  

def get_text_len(text):
    text = re_no_char.sub('', str(text))
    return len(get_word_list(text))