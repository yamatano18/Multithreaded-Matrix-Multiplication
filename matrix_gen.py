import sys
import random

def gen_matrix():
  file = open(sys.argv[1], 'w')
  i = int(sys.argv[2])
  j = int(sys.argv[3])
  file.write(str(i) + '\n')
  file.write(str(j) + '\n')

  for x in range(0, i):
    for z in range(0, j):
      file.write(str(random.uniform(0.0,1.0)) + ' ')
    file.write('\n')

  file.close()

gen_matrix()                  
