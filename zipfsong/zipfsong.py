import sys
import heapq


def best_m_songs(m, songs):
    return heapq.nlargest(m, songs, lambda song: int(song['plays']) * song['index'])


if __name__ == '__main__':
    header = sys.stdin.readline()
    n, m = [int(val) for val in header.split(' ')]
    songs = []
    for i in range(1, n + 1):
        line = sys.stdin.readline()
        plays, title = [val.strip() for val in line.split(' ')]
        songs.append({'plays': plays, 'title': title, 'index': i})
    for song in best_m_songs(m, songs):
        print song['title']
