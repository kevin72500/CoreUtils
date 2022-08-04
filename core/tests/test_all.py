from core.utils import addException

@addException
def testFunc(a,b):
    return a/b


if __name__=='__main__':
    testFunc(1, 0)