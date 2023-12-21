# -*- coding: utf-8 -*-
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle

from fastgplearn.skflow import SymbolicRegressor, SymbolicClassifier
from sklearn.datasets import fetch_california_housing, load_iris
from fastgplearn.skflow import SymbolicRegressor

x, y = load_iris(return_X_y=True)
x = x[y < 2]
x[(46, 47, 48, 49, 50,), :] = 4
y = y[y < 2]

x, y = shuffle(x, y)

# @Time  : 2023/7/7 17:47
# @Author : boliqq07
# @Software: PyCharm
# @License: MIT License

sr = SymbolicClassifier(population_size=1000, generations=10, stopping_criteria=1.0,
                        store=True, p_mutate=0.2, p_crossover=0.5, select_method="tournament",
                        tournament_size=5, hall_of_fame=3, store_of_fame=50,
                        constant_range=(0, 1.0), constants=None, depth=(1, 5),
                        function_set=('add', 'sub', 'mul', 'div', "pow2", "pow3", "exp"),
                        n_jobs=1, verbose=True, random_state=0, method_backend='p_numpy', func_p=None,
                        sci_template="default")

parameters = {'generations': range(20, 60, 5), 'tournament_size': range(5, 20, 5), 'p_mutate': [0.005, 0.05, 0.1, 0.5]}

gs = GridSearchCV(estimator=sr, param_grid=parameters, cv=10, scoring='r2', n_jobs=-1, verbose=2)

sr.fit(x, y)
res = sr.top_n(0)