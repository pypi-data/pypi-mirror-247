def mean(data):
    try:
        from gendbox.utils import _DataConverter, _is_matrix
        conv = _DataConverter(data)
        data = conv._convert_to_list()
        mean_ = None
        if _is_matrix(data):
            length = len(data) * len(data[0])
            total = sum([sum(row) for row in data])
            mean_ = total/length
        else:
            mean_ = sum(data)/len(data)
        return mean_
    except ValueError:
        print("A list consisting of only numbers must be entered as a parameter.")
    except Exception as e:
        print(f'An unexcepted error has occured: {e}')

def med(data:list):
    try:
        sorted_data = sorted(data)
        median = 0.0
        if len(sorted_data) % 2 == 0:
            median = (sorted_data[len(sorted_data)//2-1] + sorted_data[len(sorted_data)//2]) / 2
        else:
            median = sorted_data[(len(sorted_data)-1)//2]
        return median
    except ValueError:
        print("A list consisting of only numbers must be entered as a parameter.")
    except Exception as e:
        print(f'An unexpected error has occured: {e}')

def lowerq(data:list):
    if len(data) < 4:
        raise ValueError('The length of the list must be at least 4 to lower quartile calculation.')
        return None
    try:
        sorted_data = sorted(data)
        lowerset = None
        lowerset = sorted_data[:len(data)//2]
        q1 = None
        if len(lowerset) % 2 == 0:
            q1 = mean([lowerset[len(lowerset)//2-1], lowerset[len(lowerset)//2]])
        else:
            q1 = lowerset[len(lowerset)//2]
        return q1
    except ValueError:
        print("A list consisting of only numbers must be entered as a parameter.")
    except Exception as e:
        print(f'An unexpected error has occured: {e}')

def upperq(data:list):
    if len(data) < 4:
        raise ValueError('The length of the list must be at least 4 to upper quartile calculation.')
        return None
    try:
        sorted_data = sorted(data)
        upperset = None
        if len(data) % 2 == 0:
            upperset = sorted_data[len(data)//2:]
        else:
            upperset = sorted_data[len(data)//2+1:]
        q3 = None
        if len(upperset) % 2 == 0:
            q3 = mean([upperset[len(upperset)//2-1], upperset[len(upperset)//2]])
        else:
            q3 = upperset[len(upperset)//2]
        return q3
    except ValueError:
        print("A list consisting of only numbers must be entered as a parameter.")
    except Exception as e:
        print(f'An unexpected error has occured: {e}')
            
def iqr(data:list):
    if len(data) < 4:
        raise ValueError('The length of the list must be at least 4 to Interquartile Range calculation.')
        return None
    try:
        q1 = lowerq(data)
        q3 = upperq(data)
        return q3 - q1
    except ValueError:
        print("A list consisting of only numbers must be entered as a parameter.")
    except Exception as e:
        print(f'An unexpected error has occured: {e}')

def std(data:list, sample:bool=True):
    try:
        std = 0.0
        mean_ = mean(data)
        total = 0.0
        for value in data:
            total = total + (value-mean_)**2
        if sample == True:
            if len(data) == 1:
                return 0.0
            std = (total/(len(data)-1))**0.5
        else:
            if len(data) == 0:
                raise ValueError('The list cannot be empty.')
                return None
            std = (total/len(data))**0.5
        return std
    except ValueError:
        print("A list consisting of only numbers must be entered as a parameter.")
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")

def cor(data):
    try:
        from gendbox.utils import _DataConverter, _is_matrix, _cor
        conv = _DataConverter(data)
        if str(type(data)) == "<class 'pandas.core.frame.DataFrame'>":
            conv.index_ = data.columns
        data = conv._convert_to_list()
        if _is_matrix(data):
            cor_data = []
            for i in range(0, len(data[0])):
                cor_row = []
                for j in range(0, len(data[0])):
                    corr = _cor([row[i] for row in data], [row[j] for row in data])
                    cor_row.append(corr)
                cor_data.append(cor_row)
            cor_data = conv._unconvert(cor_data)
            return cor_data
        else:
            raise TypeError('A matrix must be entered as a parameter.')
    except TypeError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error has occurred: {e}")

