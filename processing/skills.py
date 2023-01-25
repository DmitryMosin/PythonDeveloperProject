import numpy as np
from utils import create_graph_image
import pandas as pd

VACANCIES_FILE = './data/vacancies_with_skills.csv'


class Skills:

    need_cols = ['name', 'key_skills', 'published_at']
    my_prof = ['Python-программист', 'python', 'питон', 'пайтон']
    need_years = ('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022')

    def __init__(self):
        self.data_file = pd.read_csv(VACANCIES_FILE, usecols=self.need_cols)
        self.data_file = self.data_file[self.data_file['name'].str.contains('|'.join(self.my_prof), case=False)]
        self.data_file['key_skills'].replace('', np.nan, inplace=True)
        self.data_file.dropna(subset=['key_skills'], inplace=True)
        self.data_file['year'] = self.data_file['published_at'].apply(lambda p: p[:4])

    def get_skills_data_frame(self):
        dct_dct_skills = {}
        for year, group in self.data_file.groupby(['year']):
            dct_dct_skills[year] = {}
            for _, row in group.iterrows():
                for skill in row['key_skills'].split('\n'):
                    if skill in dct_dct_skills[year]:
                        dct_dct_skills[year][skill] += 1
                    else:
                        dct_dct_skills[year][skill] = 1
        return pd.DataFrame(dct_dct_skills)

    def create_image_skills(self):
        df_skills = self.get_skills_data_frame()
        for year in self.need_years:
            dfy = df_skills.sort_values(by=[year], ascending=False).head(10)
            dct_dct_skills = dfy[year].to_dict()
            print(list(dct_dct_skills.keys()))
            print(list(dct_dct_skills.values()))

            create_graph_image(
                f'Топ 10 навыков для указанной профессии в {year} году:',
                'Навык',
                'Количество упоминаний',
                list(dct_dct_skills.keys()),
                list(dct_dct_skills.values()),
                f'images/image_skills_count_{year}.png'
            )


if __name__ == '__main__':
    skills = Skills()
    skills.create_image_skills()
