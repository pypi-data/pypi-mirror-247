from gendbox.utils import _DataConverter, _cor
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()
my_list = [1, 2, 3, 4, 5]
my_matrix = iris.data.tolist()
my_ndarray = iris.data
my_npmatrix = np.matrix([my_list, my_list, my_list, my_list])
my_dataframe = pd.DataFrame(iris.data)
my_series = pd.Series(my_list)


def test_data_converter():
    dc_list = _DataConverter(my_list)
    dc_matrix = _DataConverter(my_matrix)
    dc_ndarray = _DataConverter(my_ndarray)
    dc_npmatrix = _DataConverter(my_npmatrix)
    dc_dataframe = _DataConverter(my_dataframe)
    dc_series = _DataConverter(my_series)

    new_list = dc_list._convert_to_list()
    new_matrix = dc_matrix._convert_to_list()
    new_ndarray = dc_ndarray._convert_to_list()
    new_npmatrix = dc_npmatrix._convert_to_list()
    new_dataframe = dc_dataframe._convert_to_list()
    new_series = dc_series._convert_to_list()
    original_list = dc_list._unconvert(my_list)
    original_matrix = dc_matrix._unconvert(my_matrix)
    original_ndarray = dc_ndarray._unconvert(my_ndarray)
    original_npmatrix = dc_npmatrix._unconvert(my_ndarray)
    original_dataframe = dc_dataframe._unconvert(my_dataframe)
    original_series = dc_series._unconvert(my_series)

    result = (
        (str(type(new_list))=="<class 'list'>", str(type(original_list))=="<class 'list'>"),
        (str(type(new_matrix))=="<class 'list'>", str(type(original_matrix))=="<class 'list'>"),
        (str(type(new_ndarray))=="<class 'list'>", str(type(original_ndarray))=="<class 'numpy.ndarray'>"),
        (str(type(new_npmatrix))=="<class 'list'>", str(type(original_npmatrix))=="<class 'numpy.matrix'>"),
        (str(type(new_dataframe))=="<class 'list'>", str(type(original_dataframe))=="<class 'pandas.core.frame.DataFrame'>"),
        (str(type(new_series))=="<class 'list'>", str(type(original_series))=="<class 'pandas.core.series.Series'>"),
        )
    print(result)
    assert result == (
        (True, True),
        (True, True),
        (True, True),
        (True, True),
        (True, True),
        (True, True),
        )

def test_cor():
    col1 = [[i[0]] for i in my_matrix]
    col2 = [[i[1]] for i in my_matrix]
    result = round(_cor(col1, col2), 5)
    target = round(my_dataframe.corr().iloc[0, 1], 5)
    assert result == target