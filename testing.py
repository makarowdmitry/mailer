from multiprocessing import Process, Manager, Lock

def f(d, l,ll):
    ll.acquire()
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()
    ll.release()

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    l = manager.list(range(10))
    ll = Lock()

    for m in range(10):
        p = Process(target=f, args=(d, l,ll))
        p.start()
        print m

    print d
    print l