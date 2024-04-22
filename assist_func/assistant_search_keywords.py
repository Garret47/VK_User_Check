import asyncio
import io
import re
import aiohttp
import time
import pandas as pd
import numpy as np
from assist_func import custom_dataframe
from data import (STANDARD_URL_VK, COUNT_TOKENS_IN_FILE, COUNT_REQUEST_VK_THE_SAME, STR_VK_CODE,
                  DEFAULT_VK_PEOPLE, DEFAULT_VK_COMMUNITIES, DEFAULT_VK_TIMEOUT)

FileNameToken = './data/vk_codes.txt'
df_custom = custom_dataframe.SingletonDf()


def gen_code(data: str, df: pd.DataFrame, i: int):
    code_vk = ''.join(df.iloc[i:i+COUNT_REQUEST_VK_THE_SAME]['code'])
    params = (df.iloc[i:i+COUNT_REQUEST_VK_THE_SAME]['param']).to_list()
    return code_vk + 'return [' + ', '.join(map(lambda elem: data.format(elem), params)) + '];'


def edit_response(task: asyncio.Task):
    if task.cancelled():
        return
    try:
        response, names = task.result()
    except TimeoutError:
        return
    read = 0
    for i in range(len(names)):
        read = df_custom.insert_dataframe(response, names[i], read)


async def task_get_resp(code, names, token):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                response = await session.get(url=STANDARD_URL_VK.format(code, token), timeout=DEFAULT_VK_TIMEOUT)
                text = await response.json()
            except TimeoutError:
                continue
            if text.get('error'):
                if text['error']['error_code'] == 12:
                    raise ValueError('Code_VK very bad')
                elif text['error']['error_code'] == 6:
                    await asyncio.sleep(1)
                    continue
                elif text['error']['error_code'] == 29:
                    raise OSError('vk rate limit rich')
                else:
                    print(text['error']['error_code'])
                    print(text['error'])
                    print(token)
                    return 'error'
            return text['response'], names


def read_token(file):
    return file.readline()[:-1]


def create_returned_data(prefix: str, data: list):
    return ', '.join(list(map(lambda x: '{0}.items@.{1}@.'.format('{0}', prefix) + x, data)))


def create_field(question: str):
    change_str = re.sub(r'@\.[a-z]*', '', question)
    if change_str == '':
        return []
    return change_str.split(', ')


def create_dataframe_and_dict_code(settings: dict):
    arr_people = settings['people'].split(', ') if settings['people'] else []
    arr_communities = settings['communities'].split(', ') if settings['communities'] else []
    if settings['mode'] == 'all':
        fields = create_field(settings['people']) + create_field(settings['communities'])
        fields = None if fields == [] else fields
        returned_data = create_returned_data('profile', DEFAULT_VK_PEOPLE + arr_people)
        returned_data += ', ' + create_returned_data('group', DEFAULT_VK_COMMUNITIES + arr_communities)
    elif settings['mode'] == 'people':
        fields = create_field(settings['people'])
        returned_data = create_returned_data('profile', DEFAULT_VK_PEOPLE + arr_people)
    else:
        fields = create_field(settings['communities'])
        returned_data = create_returned_data('group', DEFAULT_VK_COMMUNITIES + arr_communities)
    df_custom.create_dataframes(settings['mode'], ['q']+DEFAULT_VK_PEOPLE+arr_people,
                                ['q']+DEFAULT_VK_COMMUNITIES+arr_communities)
    return fields, returned_data


def change_code(row: pd.Series, fields: list):
    if fields:
        return f'var {row["param"]} = ' + STR_VK_CODE.format('search.getHints', f'"q":"{row["q"]}", '
                                                                                f'"limit": {row["count"]}, '
                                                                                f''f''f'"fields": {fields}') + ';'
    return f'var {row["param"]} = ' + STR_VK_CODE.format('search.getHints', f'"q":"{row["q"]}", '
                                                                            f'"limit": "{row["count"]}"') + ';'


def change_dataframe(df: pd.DataFrame, fields: list):
    df['param'] = df['q'].apply(lambda q: f'a{df.index[df["q"] == q].to_list()[0] % COUNT_REQUEST_VK_THE_SAME}')
    df['code'] = df[['q', 'count', 'param']].apply(lambda row: change_code(row, fields), axis=1)
    return df


def edit_answer():
    df_custom.drop_none(['id'], ['name'])
    df_custom.edit_dataframes()


async def run_vk_search(df: pd.DataFrame, settings: dict):
    fields, returned_data = create_dataframe_and_dict_code(settings)
    tasks = []
    file = open(FileNameToken, mode='r')
    count_requests = (df.shape[0] // COUNT_REQUEST_VK_THE_SAME + int((df.shape[0] % COUNT_REQUEST_VK_THE_SAME) != 0))
    if COUNT_TOKENS_IN_FILE >= count_requests:
        arr_tokens_requests = [1 for _ in range(count_requests)]
    else:
        arr_tokens_requests = [count_requests // COUNT_TOKENS_IN_FILE for _ in range(COUNT_TOKENS_IN_FILE)]
        if count_requests % COUNT_TOKENS_IN_FILE:
            arr_tokens_requests[:count_requests % COUNT_TOKENS_IN_FILE] = (
                list(map(lambda x: arr_tokens_requests[x]+1, range(count_requests % COUNT_TOKENS_IN_FILE))))
    df = change_dataframe(df, fields)
    for i in range(len(arr_tokens_requests)):
        token = read_token(file)
        for j in range(arr_tokens_requests[i]):
            number = (j + sum(arr_tokens_requests[:i])) * COUNT_REQUEST_VK_THE_SAME
            code_vk = gen_code(returned_data, df, number)
            names = df.iloc[number:number+COUNT_REQUEST_VK_THE_SAME]['q'].to_list()
            task = asyncio.create_task(task_get_resp(code_vk, names, token))
            task.add_done_callback(edit_response)
            tasks.append(task)
    await asyncio.gather(*tasks)
    file.close()
    edit_answer()
    return df_custom.dataframes

