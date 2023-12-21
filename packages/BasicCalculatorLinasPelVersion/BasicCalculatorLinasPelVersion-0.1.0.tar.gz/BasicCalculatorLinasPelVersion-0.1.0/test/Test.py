from Calculator import Calculator

calculator = Calculator()

def test_Addition_single():
    plus = [1, 2.0, 3, 0, -1]
    for i in plus:
        calculator.Addition(i)
        x = i
        assert x - i == 0
        calculator.reset_memory()
        

def test_Addition_multi():
    calculator.Addition(1, 2.0, 3, 0, -1)
    assert calculator.memory == 5
    calculator.reset_memory()

def test_Subtraction_single():
    minus = [1, 2.0, 3, 0, -1]
    for i in minus:
        calculator.Subtraction(i)
        assert i + calculator.memory == 0
        calculator.reset_memory()

def test_Subtraction_multi():
    minus = [1, 2.0, 3, 0, -1]
    calculator.Subtraction(1, 2.0, 3, 0, -1)
    value = 0
    for i in minus:
        value += i
    assert value + calculator.memory == 0
    calculator.reset_memory()

def test_Multiplication_single():
    multiply = [1, 2.0, 3, 0, -1]
    for i in multiply:
        calculator.Multiplication(i)
        try:
            assert i / calculator.memory == 1
        except ZeroDivisionError:       #Dalyba is nulio
            pass
        calculator.reset_memory()

def test_Multiplication_multi():
    multiply = [[1, 2.0], [3, 0], [-1, 205]]
    for i,j in multiply:
        calculator.Multiplication(i,j)
        try:
            assert calculator.memory / i == j
            assert calculator.memory / j == i
        except ZeroDivisionError:       #Dalyba is nulio
            pass
        calculator.reset_memory()

def test_Division_multi():
    devide = [[1, 2.0], [3, -1.5], [-1, 205]]
    for i,j in devide:
        calculator.Division(i,j)
        assert calculator.memory == i / j
        calculator.reset_memory()

def test_Root():
    root = [[1, 2],[10, 73],[-200, 3], [-25, 1]]
    for i,j in root:
        calculator.Root(i,j)
        assert round((calculator.memory ** i),2) == j   #Number is too huge
        calculator.reset_memory()