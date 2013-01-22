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
    for i in range(1, n + 1):
        line = sys.stdin.readline()
        plays, title = [val.rstrip() for val in line.split(' ')]
        songs.append({'quality': int(plays) * i, 'title': title})
    for song in best_m_songs(m, songs):
        print song['title']
