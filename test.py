# Python program to illustrate
# *args with first extra argument
def myFun(arg1, *argv):
    print ("First argument :", arg1)
    print(type(argv[0]))


myFun('Hello', 'Welcome', 'to', 'GeeksforGeeks')
