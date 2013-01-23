import zipfsong
import unittest
import random


class TestZipfSong(unittest.TestCase):
    def random_album(self, n, m):
        #pick m songs to be the best
        best_indices = random.sample(range(1, n + 1), m)
        factors = {}
        for idx, val in enumerate(best_indices):
            factors[val] = m - idx + 1

        songs = []
        for j in range(1, n + 1):
            title = "Song %d" % j
            factor = 100
            if j in factors:
                factor *= factors[j]
            plays = str(factor * n / j)
            songs.append({'title': title, 'plays': plays, 'index': j})

        return (songs, best_indices)

    def random_tests(self):
        for i in range(100):
            #Pick random values for n and m
            n = random.randint(1, 50000)
            m = random.randint(1, n)

            (songs, best_indices) = self.random_album(n, m)

            best_m_songs = zipfsong.best_m_songs(m, songs)
            self.assertEqual([song['index'] for song in best_m_songs], best_indices)

    def test_best_m_songs(self):
        #Test m = 1 and m = n
        songs = [
            {'title': 'one', 'plays': '3', 'index': 1},
            {'title': 'two', 'plays': '1', 'index': 2}, ]
        self.assertEqual(zipfsong.best_m_songs(2, songs), songs)
        self.assertEqual(zipfsong.best_m_songs(1, songs), songs[:1])

        self.random_tests()


if __name__ == '__main__':
    unittest.main()
