import sys
import heapq

def key(song):
  return song['quality']

def best_m_songs(m, songs):
  return heapq.nlargest(m, songs, key)

if __name__ == '__main__':
  header = sys.stdin.readline()
  n, m = [int(val) for val in header.split(' ')]
  songs = []
  for i in range(n):
    line = sys.stdin.readline()
    vals = line.split(' ')
    plays = int(vals[0])
    title = vals[1].rstrip()
    songs.append({'quality': plays * (i+1), 'title': title})
  for song in best_m_songs(m, songs):
    print song['title']
