import pandas as pd
import numpy as np


class Df:

    def __init__(self):
        self.dataframes = {}

    def create_dataframes(self, mode, columns_p: list, columns_c: list):
        self.dataframes['people'] = pd.DataFrame(columns=columns_p)
        self.dataframes['communities'] = pd.DataFrame(columns=columns_c)
        if mode == 'people':
            self.dataframes.pop('communities')
        elif mode == 'communities':
            self.dataframes.pop('people')

    def insert_dataframe(self, response: list, name: str, j: int):
        for i in self.dataframes:
            try:
                data = response[j:j+len(self.dataframes[i].columns.to_list())-1]
                tmp = pd.DataFrame(np.column_stack(data), columns=self.dataframes[i].columns.to_list()[1:], dtype=str)
                tmp['q'] = name
                self.dataframes[i] = pd.concat([self.dataframes[i], tmp], ignore_index=True)
                j += len(self.dataframes[i].columns.to_list()) - 1
            except:
                print(1)
        return j

    def drop_none(self, subset_p: list, subset_c: list):
        for i in self.dataframes:
            if i == 'people':
                self.dataframes[i] = self.dataframes[i].dropna(subset=subset_p)
            else:
                self.dataframes[i] = self.dataframes[i].dropna(subset=subset_c)

    def edit_dataframes(self):
        for i in self.dataframes:
            if i == 'people':
                self.dataframes[i]['name'] = (self.dataframes[i].pop('first_name') + ' ' +
                                             self.dataframes[i].pop('last_name'))
                self.dataframes[i]['id'] = 'https://vk.com/id' + self.dataframes[i]['id']
            else:
                self.dataframes[i]['screen_name'] = 'https://vk.com/' + self.dataframes[i]['screen_name']
