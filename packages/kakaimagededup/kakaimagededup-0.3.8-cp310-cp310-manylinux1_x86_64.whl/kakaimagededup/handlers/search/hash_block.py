from typing import Callable, Dict
from collections import defaultdict

def split(key, split_count):
  pre_length = int(16 / split_count)
  return [key[i * pre_length: (i + 1) * pre_length] for i in range(split_count)]

class HashBlock:
  def __init__(self, hash_dict: Dict, distance_function: Callable, n_split=4):
    print('end')
    self.distance_function = distance_function
    self.hash_dict = hash_dict  # database
    self.n_split = n_split
    self.phash_cache = [defaultdict(list) for i in range(n_split)]
    self.init_phash_map()
    
  def init_phash_map(self):
    for key, value in self.hash_dict.items():
      self.split_and_gen_hash_index(key, value)
    
  def split_and_gen_hash_index(self, filename, hash_value):
    key_split = split(hash_value, self.n_split)
    print(key_split)
    for index, k in enumerate(key_split):
      self.phash_cache[index][k].append(filename)
    
  def search(self, query: str, tol: int = 10) -> Dict[str, int]:
    hash_value = self.hash_dict[query]
    key_split = split(hash_value, self.n_split)
    print(key_split)
    result = set()
    for index, k in enumerate(key_split):
      if k in self.phash_cache[index]:
        for filename in self.phash_cache[index][k]:
          hamming_distance = self.distance_function(hash_value, self.hash_dict[filename])
          if hamming_distance <= tol:
            result.add((filename, hamming_distance))
    return list(result)
