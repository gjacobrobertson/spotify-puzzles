import sys

def reverse_num(num):
  rnum = num & 1
  while num >> 1:
    rnum <<= 1
    num >>= 1
    rnum |= (num & 1)
  return rnum

if __name__ == '__main__':
  line =  sys.stdin.readline()
  num = int(line)
  print reverse_num(num)
