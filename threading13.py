from multiprocessing import Process

def f(name):
    print 'hello', name

if __name__ == '__main__':

	# a = map(f, range(500000))
    p = Process(target=f, args=(range(500000),))
    p.start()
    p.join()
    # p2 = Process(target=f, args=(range(100000),))
    # p2.start()
    # p2.join()