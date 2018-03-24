import sys
import twitter
import multiprocessing as multiproc


if len(sys.argv) == 2:
    twitter.download(sys.argv[1])
elif len(sys.argv) > 2:
    for link in sys.argv[1::]:
        p = multiproc.Process(target=twitter.download, args=(link,))
        p.start()
else:
    print('Usage: python3 main.py "https://twitter.com/username/status/8942397439823"')
