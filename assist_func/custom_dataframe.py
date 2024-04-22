import pandas as pd
import numpy as np


class SingletonDf:
    __instance = None
    dataframes = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def create_dataframes(cls, mode, columns_p: list, columns_c: list):
        cls.dataframes['people'] = pd.DataFrame(columns=columns_p)
        cls.dataframes['communities'] = pd.DataFrame(columns=columns_c)
        if mode == 'people':
            cls.dataframes.pop('communities')
        elif mode == 'communities':
            cls.dataframes.pop('people')

    @classmethod
    def insert_dataframe(cls, response: list, name: str, j: int):
        for i in cls.dataframes:
            data = response[j:j+len(cls.dataframes[i].columns.to_list())-1]
            tmp = pd.DataFrame(np.column_stack(data), columns=cls.dataframes[i].columns.to_list()[1:], dtype=str)
            tmp['q'] = name
            cls.dataframes[i] = pd.concat([cls.dataframes[i], tmp], ignore_index=True)
            j += len(cls.dataframes[i].columns.to_list()) - 1
        return j

    @classmethod
    def drop_none(cls, subset_p: list, subset_c: list):
        for i in cls.dataframes:
            if i == 'people':
                cls.dataframes[i].dropna(subset=subset_p)
            else:
                cls.dataframes[i].dropna(subset=subset_c)

    @classmethod
    def edit_dataframes(cls):
        for i in cls.dataframes:
            if i == 'people':
                cls.dataframes[i]['name'] = (cls.dataframes[i].pop('first_name') + ' ' +
                                             cls.dataframes[i].pop('last_name'))
                cls.dataframes[i]['id'] = 'https://vk.com/id' + cls.dataframes[i]['id']
            else:
                cls.dataframes[i]['screen_name'] = 'https://vk.com/' + cls.dataframes[i]['screen_name']
