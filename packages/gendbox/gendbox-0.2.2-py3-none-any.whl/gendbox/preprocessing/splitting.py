def train_test(x, y, test_size:float, random_state:int)->tuple:
    if test_size <= 0.0 and test_size >= 1.0:
        raise ValueError('test_size must be between 0-1.')
    import random
    random.seed(random_state)
    from gendbox.utils import _DataConverter, _is_matrix
    dcx = _DataConverter(x)
    dcy = _DataConverter(y)
    data_x = dcx._convert_to_list()
    data_y = dcy._convert_to_list()
    if len(data_x) != len(data_y):
        raise ValueError('length of x and length of y must be equal.')
    x_train = []
    x_test = []
    y_train = []
    y_test = []
    test_length = int(len(data_x) * test_size)
    counter = 0
    print ("_is_matrix(data_x)", _is_matrix(data_x))
    print ("_is_matrix(data_y)", _is_matrix(data_y))
    if _is_matrix(data_x) and _is_matrix(data_y):
        while len(data_x) > 0:
            # print("counter:", counter)
            # print("test_length:", test_length)
            index = random.randint(0, len(data_x)-1)
            print("len(data_x):", len(data_x))
            print("index:", index)
            if counter < test_length:
                x_test.append(data_x[index])
                y_test.append(data_y[index])
                counter = counter + 1
            else:
                x_train.append(data_x[index])
                y_train.append(data_y[index])
            del data_x[index]
            del data_y[index]
    return (x_train, x_test, y_train, y_test)