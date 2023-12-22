import gendbox.stats as sts
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
my_list = [1, 2, 3, 4, 5]
my_matrix = iris.data.tolist()
my_ndarray = iris.data
my_dataframe = pd.DataFrame(iris.data)
my_series = pd.Series(my_list)

def test_mean():
    means = []
    means.append(sts.mean(my_list))
    means.append(sts.mean(my_matrix))
    means.append(sts.mean(my_ndarray))
    means.append(sts.mean(my_dataframe))
    means.append(sts.mean(my_series))
    print(means)
    result = tuple(mean is not None for mean in means)
    assert result == (True,) * len(means)

def test_med():
    result = sts.med(my_list)
    assert result == 3

def test_lowerq():
    result = sts.lowerq(my_list)
    assert result == 1.5

def test_upperq():
    result = sts.upperq(my_list)
    assert result == 4.5

def test_iqr():
    result = sts.iqr(my_list)
    assert result == 3

def test_std():
    result = sts.std(my_list)
    assert result == 2.5**0.5

def test_cor():
    result1 = sts.cor(my_matrix) is not None
    result2 = sts.cor(my_ndarray) is not None
    result3 = sts.cor(my_dataframe) is not None
    result = (result1, result2, result3)
    assert result == (True, True, True)
