from calculator_fchapuis.calculator_pckg.calculator import Calculator


def test_add():
    calc = Calculator()
    calc.add(5)
    assert calc.memory == 5


def test_subtract():
    calc = Calculator()
    calc.subtract(2)
    assert calc.memory == -2


def test_multiply():
    calc = Calculator()
    calc.multiply(3)
    assert calc.memory == 0


def test_divide():
    calc = Calculator()
    calc.divide(3)
    assert calc.memory == 0.0  # Note: Check the expected result based on your use case


def test_floor_divide():
    calc = Calculator()
    calc.floor_divide(5)
    assert calc.memory == 0


def test_root():
    calc = Calculator()
    calc.root(2)
    assert calc.memory == 0.0  # Note: Check the expected result based on your use case


def test_memory_retention():
    calc = Calculator()
    calc.add(10)
    assert calc.memory == 10
    # Testing memory retention: adding a value to the current memory value
    calc.add(5)
    assert calc.memory == 15


def test_reset_memory():
    calc = Calculator()
    calc.reset_memory()
    assert calc.memory == 0
