import numpy as np
from utils import create_array 

def test_equal_arrays():
  arr1 = create_array()
  arr2 = create_array()
  assert (np.array_equal(arr1, arr2), "Arrays are not equal"
