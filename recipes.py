import numpy as np
import pandas as pd
from joblib import load
import warnings

warnings.filterwarnings("ignore")


class Forecast:

    def __init__(self, list_of_ingredients):
        all_ingredients = pd.read_csv('nutrients.csv').drop(columns=['nutrient', 'value', 'nutrient_api']).columns
        self.list_of_ingredients = [ingredient.lower().strip() for ingredient in list_of_ingredients.split(',')]
        self.known_ingredients = []
        self.unknown_ingredients = []
        for ingredient in self.list_of_ingredients:
            if ingredient in all_ingredients:
                self.known_ingredients.append(ingredient)
            elif ingredient != '':
                self.unknown_ingredients.append(ingredient)

    def preprocess(self):
        all_ingredients = pd.read_csv('nutrients.csv').drop(columns=['nutrient', 'value', 'nutrient_api']).columns
        vector = pd.DataFrame(data=[np.zeros(len(all_ingredients))], columns=all_ingredients)
        for ingredient in self.known_ingredients:
            vector.loc[0, [ingredient]] = 1.0
        return vector

    def predict_rating_category(self):
        model = load('best_model.joblib')
        rating_cat = model.predict(self.preprocess())[0]
        if rating_cat == 'bad':
            text = 'Плохое сочетание ингредиентов'
        elif rating_cat == 'so-so':
            text = 'Среднее сочетание ингредиентов'
        else:
            text = 'Отличное сочетание ингредиентов'
        return rating_cat, text


class NutritionFacts:

    def __init__(self, list_of_ingredients):
        all_ingredients = pd.read_csv('nutrients.csv').drop(columns=['nutrient', 'value', 'nutrient_api']).columns
        self.list_of_ingredients = [ingredient.lower().strip() for ingredient in list_of_ingredients.split(',')]
        self.known_ingredients = []
        self.unknown_ingredients = []
        for ingredient in self.list_of_ingredients:
            if ingredient in all_ingredients:
                self.known_ingredients.append(ingredient)
            elif ingredient != '':
                self.unknown_ingredients.append(ingredient)

    def retrieve(self):
        facts = pd.read_csv('nutrients.csv')[['nutrient'] + self.known_ingredients]
        return facts

    def filter(self, n):
        text_with_facts = ''
        for ingredient in self.known_ingredients:
            text_with_facts += f'{ingredient.title()}\n'
            top_n_nutrients = self.retrieve()[['nutrient', ingredient]].sort_values(ingredient, ascending=False).head(n)
            for index, row in top_n_nutrients.iterrows():
                text_with_facts += f'{row["nutrient"]} - {round(row[ingredient])}% of Daily Value\n'
            text_with_facts += '\n'
        return text_with_facts


class SimilarRecipes:

    def __init__(self, list_of_ingredients):
        all_ingredients = pd.read_csv('nutrients.csv').drop(columns=['nutrient', 'value', 'nutrient_api']).columns
        self.list_of_ingredients = [ingredient.lower().strip() for ingredient in list_of_ingredients.split(',')]
        self.known_ingredients = []
        self.unknown_ingredients = []
        for ingredient in self.list_of_ingredients:
            if ingredient in all_ingredients:
                self.known_ingredients.append(ingredient)
            elif ingredient != '':
                self.unknown_ingredients.append(ingredient)

    def find_all(self):
        indexes = None
        recipes = pd.read_csv('recipes.csv')
        for ingredient in self.known_ingredients:
            recipes = recipes[recipes[ingredient] == 1.0]
            if len(recipes) == 0:
                return indexes
        indexes = recipes.index
        return indexes

    def top_similar(self, n):
        text_with_recipes = None
        try:
            similar_recipes = pd.read_csv('recipes.csv').iloc[self.find_all()]
        except:
            return text_with_recipes
        if n <= 0:
            return text_with_recipes
        similar_recipes['count_ingredients'] = similar_recipes[similar_recipes.columns[9:-1]].apply(sum, axis=1)
        similar_recipes = similar_recipes[similar_recipes['count_ingredients'] < (5 + len(self.known_ingredients))]
        top_n_recipes = similar_recipes.sort_values('count_ingredients').head(n)
        text_with_recipes = ''
        for index, row in top_n_recipes.iterrows():
            text_with_recipes += f"- {row['title']}, рейтинг: {str(row['rating'])}, URL: {row['link']}\n"
        return text_with_recipes


def print_daily_menu():
    breakfasts = pd.read_csv('breakfasts.csv')
    lunches = pd.read_csv('lunches.csv')
    dinners = pd.read_csv('dinners.csv')
    breakfast = breakfasts.sample(1)
    print("ЗАВТРАК\n---------------------")
    print(f"{breakfast['title'].values[0]} (рейтинг: {breakfast['rating'].values[0]})")
    print('\nИнгредиенты:')
    for ingredient in breakfast.columns[9:-2]:
        if breakfast[ingredient].values[0] == 1.0:
            print(f'\t- {ingredient}')
    print('\nКБЖУ:')
    print(f'\t- calories: {int(breakfast["calories"].values[0])}%')
    print(f'\t- protein: {int(breakfast["protein"].values[0])}%')
    print(f'\t- fat: {int(breakfast["fat"].values[0])}%')
    print(f'\t- carbohydrates: {int(breakfast["carbohydrates"].values[0])}%')
    print(f'\t- sodium: {int(breakfast["sodium"].values[0])}%')
    print(f'\nURL: {breakfast["link"].values[0]}')

    lunch = lunches.sample(1)
    print("\nОБЕД\n---------------------")
    print(f"{lunch['title'].values[0]} (рейтинг: {lunch['rating'].values[0]})")
    print('\nИнгредиенты:')
    for ingredient in lunch.columns[9:-2]:
        if lunch[ingredient].values[0] == 1.0:
            print(f'\t- {ingredient}')
    print('\nКБЖУ:')
    print(f'\t- calories: {int(lunch["calories"].values[0])}%')
    print(f'\t- protein: {int(lunch["protein"].values[0])}%')
    print(f'\t- fat: {int(lunch["fat"].values[0])}%')
    print(f'\t- carbohydrates: {int(lunch["carbohydrates"].values[0])}%')
    print(f'\t- sodium: {int(lunch["sodium"].values[0])}%')
    print(f'\nURL: {lunch["link"].values[0]}')

    dinner = dinners.sample(1)
    print("\nУЖИН\n---------------------")
    print(f"{dinner['title'].values[0]} (рейтинг: {dinner['rating'].values[0]})")
    print('\nИнгредиенты:')
    for ingredient in dinner.columns[9:-2]:
        if dinner[ingredient].values[0] == 1.0:
            print(f'\t- {ingredient}')
    print('\nКБЖУ:')
    print(f'\t- calories: {int(dinner["calories"].values[0])}%')
    print(f'\t- protein: {int(dinner["protein"].values[0])}%')
    print(f'\t- fat: {int(dinner["fat"].values[0])}%')
    print(f'\t- carbohydrates: {int(dinner["carbohydrates"].values[0])}%')
    print(f'\t- sodium: {int(dinner["sodium"].values[0])}%')
    print(f'\nURL: {dinner["link"].values[0]}')
