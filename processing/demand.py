import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


class Demand:

    need_cols = ['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at']
    my_prof = ['Python-программист', 'python', 'питон', 'пайтон']

    def __init__(self):
        self.file_data = pd.read_csv(VACANCIES_FILE, usecols=self.need_cols)
        self.file_data['average'] = self.file_data[['salary_from', 'salary_to']].mean(axis=1)
        self.file_data['salary'] = self.file_data.apply(self.get_salary, axis=1)
        self.file_data['date'] = self.file_data.apply(self.get_date, axis=1)
        self.file_data['year'] = self.file_data.apply(self.get_year, axis=1)
        self.file_data.dropna(subset=['salary'], inplace=True)

    def get_dict_data(self):
        temp_df = self.file_data[self.file_data['name'].str.contains('|'.join(self.my_prof), case=False)]
        # New data frame
        data_frame = pd.DataFrame()
        data_frame['salary'] = self.file_data.groupby(['year'])['salary'].mean()
        data_frame['count'] = self.file_data.groupby(['year']).size()
        data_frame['my_prof_salary'] = temp_df.groupby(['year'])['salary'].mean()
        data_frame['my_prof_count'] = temp_df.groupby(['year']).size()
        print(data_frame)
        return data_frame.to_dict()

    def create_images(self):
        stats = self.get_dict_data()

        create_graph_image(
            'Динамика уровня зарплат по годам',
            'Год',
            'Зарплата, руб.',
            list(stats['salary'].keys()),
            list(stats['salary'].values()),
            'images/image_demand_salary.png'
        )

        create_graph_image(
            'Динамика количества вакансий по годам',
            'Год',
            'Кол-во вакансий',
            list(stats['count'].keys()),
            list(stats['count'].values()),
            'images/image_demand_count.png'
        )

        create_graph_image(
            'Динамика уровня зарплат по годам для выбранной профессии',
            'Год',
            'Зарплата, руб.',
            list(stats['my_prof_salary'].keys()),
            list(stats['my_prof_salary'].values()),
            'images/image_demand_my_prof_salary.png'
        )

        create_graph_image(
            'Динамика количества вакансий по годам для выбранной профессии',
            'Год',
            'Кол-во вакансий',
            list(stats['my_prof_count'].keys()),
            list(stats['my_prof_count'].values()),
            'images/image_demand_my_prof_count.png'
        )

    @staticmethod
    def get_salary(row):
        try:
            return row['average'] * currency_to_rub[row['salary_currency']]
        except:
            return np.nan

    @staticmethod
    def get_date(row):
        return row['published_at'][:7]

    @staticmethod
    def get_year(row):
        return row['published_at'][:4]


if __name__ == '__main__':
    demand = Demand()
    demand.create_images()




