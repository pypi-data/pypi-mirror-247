class MinMax:
    def __init__(self):
        self.min_value = None
        self.max_value = None
    
    def fit(self, data):
        try:
            if str(type(data)) == "<class 'pandas.core.frame.DataFrame'>":
                data = data.values.tolist()
            if(str(type(data)) == "<class 'pandas.core.series.Series'>" or 
               str(type(data)) == "<class 'numpy.matrix'>" or 
               str(type(data)) == "<class 'numpy.ndarray'>"):
                data = data.tolist()
            from gendbox.utils import _is_matrix
            if _is_matrix(data):
                min_values = []
                max_values = []
                for row in data:
                    if _is_matrix(row):
                        raise ValueError('The array must have 1 or 2 dimension.')
                    min_values.append(min(row))
                    max_values.append(max(row))
                self.min_value = min(min_values)
                self.max_value = max(max_values)
            else: 
                self.min_value = min(data)
                self.max_value = max(data)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f'An unexcepted error has occured: {e}')
    
    def transform(self, data):
        try:
            from gendbox.utils import _DataConverter, _is_matrix
            conv = _DataConverter(data)
            data = conv._convert_to_list()
            new_data = []
            
            if _is_matrix(data):
                for i in range(0, len(data)):
                    new_row = []
                    for j in range(0, len(data[i])):
                        value = data[i][j]
                        normalized_value = (value - self.min_value) / (self.max_value - self.min_value)
                        new_row.append(normalized_value)
                    new_data.append(new_row)
            else:
                for value in data:
                    normalized_value = (value - self.min_value) / (self.max_value - self.min_value)
                    new_data.append(normalized_value)
            print('DATA:', new_data)
            new_data = conv._unconvert(new_data)
            return new_data
        except Exception as e:
            print(f'An unexcepted error has occured: {e}')
    
    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)

# class ZScore:
#     def __init__(self):
#         self.mean = None
#         self.std = None
    
#     def fit(self, data):
#         try:
#             import gendbox.stats as __sts
#             self.mean = __sts.mean(data)
#             self.std = __sts.std(data)
#         except Exception as e:
#             print(f'An unexcepted error has occured: {e}')
    
#     def transform(self, data):
#         try:
#             new_list = []
#             for value in data:
#                 normalized_value = (value - self.mean) / self.std
#                 new_list.append(normalized_value)
#             return new_list
#         except Exception as e:
#             print(f'An unexcepted error has occured: {e}')
    
#     def fit_transform(self, data):
#         self.fit(data)
#         return self.transform(data)

# class Robust:
#     def __init__(self):
#         self.median = None
#         self.iqr = None
    
#     def fit(self, data):
#         try:
#             import gendbox.stats as __sts
#             self.median = __sts.median(data)
#             self.iqr = __sts.iqr(data)
#         except Exception as e:
#             print(f'An unexcepted error has occured: {e}')
    
#     def transform(self, data):
#         try:
#             new_list = []
#             for value in data:
#                 normalized_value = (value - self.median) / self.iqr
#                 new_list.append(normalized_value)
#             return new_list
#         except Exception as e:
#             print(f'An unexcepted error has occured: {e}')
    
#     def fit_transform(self, data):
#         self.fit(data)
#         return self.transform(data)