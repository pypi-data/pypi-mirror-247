class _DataConverter:
    def __init__(self, data):
        self.original_ = data
        self.type_ = str(type(data))
        self.index_ = None
        self.converted_ = None
    
    def _convert_to_list(self):
        try:
            if self.type_ == "<class 'pandas.core.frame.DataFrame'>":
                self.converted_ = self.original_.values.tolist()
            elif(self.type_ == "<class 'pandas.core.series.Series'>" or 
               self.type_ == "<class 'numpy.matrix'>" or 
               self.type_ == "<class 'numpy.ndarray'>"):
                self.converted_ = self.original_.tolist()
            else:
                self.converted_ = self.original_
            return self.converted_
        except  Exception as e:
            print(f'An unexcepted error has occured: {e}')
    
    def _unconvert(self, data=None):
        try:
            new_data = None
            if data is None:
                data == self.converted_
            if self.type_ == "<class 'pandas.core.frame.DataFrame'>":
                from pandas import DataFrame
                new_data = DataFrame(data=data, columns=self.original_.columns, index=self.index_)
            elif self.type_ == "<class 'pandas.core.series.Series'>":
                from pandas import Series
                new_data = Series(data)
            elif self.type_ == "<class 'numpy.matrix'>":
                from numpy import matrix
                new_data = matrix(data)
            elif self.type_ == "<class 'numpy.ndarray'>":
                from numpy import array
                new_data = array(data)
            else:
                new_data = data
            return new_data
        except Exception as e:
            print(f'An unexcepted error has occured: {e}')


def _cor(x, y):
    try:
        if _is_matrix(x) and _is_matrix(y):
            if len(x) == len(y):
                if not all(len(row) == 1 for row in x):
                    raise ValueError('The x and y matrix should be in the shape (n, 1), but the shape of x is ​​not compatible.')
                    return None
                if not all(len(row) == 1 for row in y):
                    raise ValueError('The x and y matrix should be in the shape (n, 1), but the shape of y is ​​not compatible.')
                    return None
                length = len(x)
                if length > 0:
                    r = 0.0
                    sumx = 0.0
                    sumy = 0.0
                    sumxy = 0.0
                    sumx2 = 0.0
                    sumy2 = 0.0
                    from gendbox.preprocessing.normalization import MinMax as __minmax
                    normalizer = __minmax()
                    x = normalizer.fit_transform(x)
                    y = normalizer.transform(y)
                    for i in range(0,len(x)):
                        sumx += x[i][0]
                        sumy += y[i][0]
                        sumxy += x[i][0] * y[i][0]
                        sumx2 += x[i][0] ** 2
                        sumy2 += y[i][0] ** 2
                    try:
                        r = (length*sumxy-sumx*sumy)/((length*sumx2-sumx**2)*(length*sumy2-sumy**2))**0.5
                    except ZeroDivisionError:
                        r = 0
                        pass
                    return r
                else:
                    raise ValueError('x and y are empty.')
            else:
                raise ValueError('x and y are not equal in length.')
        elif not _is_matrix(x) and not _is_matrix(y):
            if isinstance(x, list) and isinstance(y, list):
                if len(x) == len(y):
                    length = len(x)
                    if length > 0:
                        r = 0.0
                        sumx = 0.0
                        sumy = 0.0
                        sumxy = 0.0
                        sumx2 = 0.0
                        sumy2 = 0.0
                        for i in range(0,len(x)):
                            sumx += x[i]
                            sumy += y[i]
                            sumxy += x[i] * y[i]
                            sumx2 += x[i] ** 2
                            sumy2 += y[i] ** 2
                        try:
                            r = (length*sumxy-sumx*sumy)/((length*sumx2-sumx**2)*(length*sumy2-sumy**2))**0.5
                        except ZeroDivisionError:
                            r = 0
                            pass
                        return r
                    else:
                        raise ValueError('x and y are empty.')
                else:
                    raise TypeError('x and y are not equal in length.')
            else:
                raise TypeError('The format of x and y is not compatible.')
        else:
            raise TypeError('x and y have different shapes.')
    except ValueError or TypeError as e:
        print(e)
    except Exception as e:
        print(f'An unexcepted error has occured: {e}')
    
    
def _is_matrix(obj):
    try:
        if not isinstance(obj, list):
            return False
        elif not obj:
            return False
        elif not all(isinstance(row, list) and len(row) == len(obj[0]) for row in obj):
            return False
        else:
            return True
    except Exception as e:
        print(f'An unexcepted error has occured: {e}')
