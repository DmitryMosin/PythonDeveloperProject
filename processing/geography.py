import numpy as np
import pandas as pd
from utils import create_graph_image


VACANCIES_FILE = './data/vacancies_with_skills.csv'

currency_to_rub = {
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "UZS": 0.0055,
    "UAH": 1.64,
    "BYR": 23.91,
    "RUR": 1,
    "AZN": 35.68,
    "USD": 60.66,
    "EUR": 59.90,
}


class Cities:

    need_cols = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name']
    need_show = 20

    def __init__(self):
        self.file_data = pd.read_csv(VACANCIES_FILE, usecols=self.need_cols)
        self.file_data['average'] = self.file_data[['salary_from', 'salary_to']].mean(axis=1)
        self.file_data['salary'] = self.file_data.apply(self.get_salary, axis=1)
        self.file_data.dropna(subset=['salary'], inplace=True)

    def get_salary_data_frame(self):
        return pd\
            .DataFrame({'salary': self.file_data.groupby(['area_name'])['salary'].mean()})\
            .reset_index()\
            .sort_values(by=['salary'], ascending=False)[1:self.need_show + 1]

    def get_count_data_frame(self):
        df_count = pd\
            .DataFrame({'count': self.file_data.groupby(['area_name']).size()})\
            .reset_index()\
            .sort_values(by=['count'], ascending=False)\
            .head(self.need_show)

        count = self.file_data.shape[0]
        df_count['part'] = df_count['count'].apply(lambda x: round(x / count, 4))
        return df_count

    def create_images(self):
        df_salary = self.get_salary_data_frame()
        df_count = self.get_count_data_frame()
        print(df_salary)
        print(df_count)

        create_graph_image(
            'Уровень зарплат по городам (в порядке убывания)',
            'Город',
            'Зарплата, руб.',
            df_salary['area_name'].to_list(),
            df_salary['salary'].to_list(),
            'images/image_geography_salary.png'
        )

        create_graph_image(
            'Доля вакансий по городам (в порядке убывания)',
            'Город',
            'Доля вакансий',
            df_count['area_name'].to_list(),
            df_count['part'].to_list(),
            'images/image_geography_parts.png'
        )

    @staticmethod
    def get_salary(row):
        try:
            return row['average'] * currency_to_rub[row['salary_currency']]
        except:
            return np.nan


if __name__ == '__main__':
    cities = Cities()
    cities.create_images()
