import numpy as np

def test_equal_arrays():
  assert (np.array_equal([1, 2], [1, 2])), "Arrays are not equal"
