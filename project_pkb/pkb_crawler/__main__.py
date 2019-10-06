import argparse

from igcrawler.main import start

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, help='format untuk output tugas (level1), contoh : --mode 1', metavar='')
    parser.add_argument('-u', '--username', type=str, help='username untuk login instagram', metavar='')
    parser.add_argument('-p', '--password', type=str, help='password untuk login instagram', metavar='')
    parser.add_argument('--uid', type=str, help='instagram id user mula mula yang ingin di-crawl', metavar='')
    parser.add_argument('-n', '--limit', type=str, help='scrap n-posts dari setiap user', metavar='')
    parser.add_argument('-r', '--ring', type=str, help='mengambil follower sampai n-ring', metavar='')
    parser.add_argument('-c', help='melanjutkan dari scrapping sebelumnya (experimental)', action='store_true')
    start(parser.parse_args())
