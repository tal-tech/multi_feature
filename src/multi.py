import sys
import os

basePath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(basePath, 'tools'))
from basic_module import *
import core_funs
import util_tools




def multi(text, muti, task_id=''):
    logger.info('task_id:{}'.format(task_id))
    error_code, error_message, df = util_tools.parse_list_2_df(text, task_id)
    result = {}
    if error_code == success:
        for item in muti:
            result[item] = eval('core_funs.{}(df,task_id)'.format(multi_item_2_fun[item]))
    return {'error_code': error_code, 'error_message': error_message, 'result': result}


if __name__=="__main__":
    text=[{
            "text": "这句话呢，其实都是告诉你游戏规则，他就看你能不能看到他这个给你的规定了。",
            "begin_time": 1326750,
            "end_time": 1332165
        },
        {
            "text": "或者说你骂人一个游戏，它上面会有一个游戏的一个，这个攻略对不对？",
            "begin_time": 1334200,
            "end_time": 1339555
        },
        {
            "text": "那你是不是要看到的这个游戏规则？女足知道了你这游戏谈话。",
            "begin_time": 1339540,
            "end_time": 1344105
        },
        {
            "text": "我什么时候该拐弯了或者什么？这种游戏是不是？",
            "begin_time": 1353120,
            "end_time": 1355985
        },
        {
            "text": "规则是不是那就是你看这句话呢76三呢，是游戏给你的一个攻略，告诉你这个游戏怎么玩",
            "begin_time": 1359510,
            "end_time": 1366485
        },
        {
            "text": "cc相同，是吧，那你看啊，这我就开始玩游戏的事嘛，对不对，那就按照他的这个说法来吧。",
            "begin_time": 1534130,
            "end_time": 1541365
        }
    ]
    muti = [
        "speed",
        "sent_num",
        "sent_av_len",
        "punch_num",
        "question_num"
    ]
    result = multi(text,muti)
    print(result)
    


