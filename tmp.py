import os, glob, sys

def quiet(*args):
    pass

trace = quiet

testfiles = glob.glob("*.py")
testfiles.sort()
trace(os.getcwd(), *testfiles)
print(*testfiles)
print(sys.executable)