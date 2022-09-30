import time
from datetime import datetime, timedelta

def funA(f):
    def funB(*args):
        time.sleep(5)
        print(f"{f.__name__} is called at time {datetime.utcnow()}")
        return f(*args)
    return funB


@funA
def add2(a,b):
    z=a+b
    #print("returning sume of 2 numbers")
    return z

@funA
def add3(a,b,c):
    z=a+b+c
    #print("returning sume of 3 numbers")
    return z




print (add2(10,20))
print (add3(10,20,30))