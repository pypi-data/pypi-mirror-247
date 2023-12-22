class MinMax:
    def __init__(self):
        # self.lower_limit = min_value
        # self.upper_limit = max_value
        self.min_value = None
        self.max_value = None
    
    def fit(self, data):
        self.min_value = min(data)
        self.max_value = max(data)
    
    def transform(self, data):
        new_list = []
        for value in data:
            normalized_value = (value - self.min_value) / (self.max_value - self.min_value)
            new_list.append(normalized_value)
        return new_list
    
    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)
# class ZScore:
#     def __init__(self):
#         pass

# class Sygmoid:
#     def __init__(self, min_value:float, max_value:float):
#         self.min_value = min_value
#         self.max_value = max_value