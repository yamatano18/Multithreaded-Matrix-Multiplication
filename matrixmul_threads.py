#!/usr/bin/python

import threading
import time
import math
import sys


class myThread(threading.Thread):
    def __init__(self, threadID, name, indexI, indexJ, info):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.indexI = indexI
        self.indexJ = indexJ
        self.sum = 0
        self.sumSq = 0
        self.info = info

    def run(self):
        self.sum = mult(self.name, self.info.A, self.info.B, self.info.ac, self.info.bc, self.indexI, self.indexJ, self.info)
        self.info.updateMatrix(self.sum)
        self.sumSquare = 0
        for i in range(len(self.sum)):
            self.sumSquare += self.sum[i] * self.sum[i]
        self.info.updateFrobemius(self.sumSquare)

        print "Thread-"+str(self.threadID)+" Vektor sum: "+str(self.sum)
        print "Thread-"+str(self.threadID)+" sumSquare:  "+str(self.sumSquare)

class MatrixInfo:
    def __init__(self, infoID, A, B, ac, bc, counter):
        self.infoID = infoID
        self.A = A
        self.B = B
        self.ac = ac
        self.bc = bc
        self.C = []
        self.frob = []
        self.counter = counter

    def updateMatrix(self, C):
        self.C.append(C)

    def updateFrobemius(self, value):
        self.frob.append(value)

    def reorder(self,bc):
        X = []
        vect1 = []
        vect2 = []
        for i in range(len(self.C)):
            vect1.extend(self.C[i])

        for i,x in enumerate(vect1):
            if i%bc == 0 and i>0:
                X.append(vect2)
                vect2 = []
            vect2.append(x)

        X.append(vect2)
        self.C = X
        #print "sumSq: ", self.frob

        # X = [[0]*bc]*ar
        #
        # k = 0
        # m = 0
        #
        # for i in range(ar):
        #     for j in range(bc):
        #         print "k=" + `k` + ", m=" + `m`
        #         print "i=" + `i` + ", j=" + `j`
        #
        #         if (i*bc+j)%3 == 0 and i+j != 0:
        #
        #             k += 1
        #             m = 0
        #         X[i][j] = self.C[k][m]
        #         m += 1
        # self.C = X

    def showMatrix(self):
        print "Macierz wynikowa:"
        for r in self.C:
            print(r)

    def incrementCounter(self):
        self.counter += 1

    def getCounter(self):
        return self.counter

    def countFrobemious(self):
        frobenious = 0
        for i in range(n_child):
            frobenious += self.frob[i]
        print "Norma Frobeniusa = ", math.sqrt(frobenious)

def mult(threadName, A, B, ac, bc, i1, i2, info):
    x = []
    for i in range(i1, i2):
        s = 0
        for k in range(ac):
            s += A[i / bc][k] * B[k][i % bc]
        #print threadName+": A["+`i/bc`+"]["+`k`+"]="+str(A[i/bc][k])+", B["+`k`+"]["+`i%bc`+"]="+str(B[k][i%bc])
        x.append(s)
        # Get lock to synchronize threads
        threadLock.acquire()
        info.incrementCounter()
        # Free lock to release next thread
        threadLock.release()
    return x

try:
    n_child = int(sys.argv[1])
except IndexError:
    n_child = 4

    print "Nie wlasciwy argument, wprowadzam ",n_child, " wantki!"
A = []
B = []
ar = 0
ac = 0
br = 0
bc = 0
counter = 0
maxCount = 0
frobenius = 0

matrix_file1 = open("A.txt")
for i, line in enumerate(matrix_file1):
    if i == 0:
        ar = int(line)
    elif i == 1:
        ac = int(line)
    elif i > 1:
        tmp = line.split(" ")
        tmp.remove("\n")
        A += [map(float, tmp)]

matrix_file2 = open("B.txt")
for i, line in enumerate(matrix_file2):
    if i == 0:
        br = int(line)
    elif i == 1:
        bc = int(line)
    elif i > 1:
        tmp = line.split(" ")
        tmp.remove("\n")
        B += [map(float, tmp)]

info = MatrixInfo(0, A, B, ac, br, counter)
n = ar * bc / 3
threadLock = threading.Lock()
threads = []
maxCount = ar * bc

# Create new threads
for i in range(n_child):
    if i < (n_child - 1):
        threads.append(myThread(i, "Thread-" + str(i), i * n, (i + 1) * n, info))
    else:
        threads.append(myThread(i, "Thread-" + str(i), i * n, n * 3+1, info))

# Start new Threads
for i in range(n_child):
    threads[i].start()


#while (info.getCounter() != maxCount):
#    time.sleep(0.2)
#
#    if float(info.getCounter())/float(maxCount) != 1:
#        print str(float(info.getCounter())/float(maxCount)*100)+"%"
#    print str(float(info.getCounter())/float(maxCount)*100)+"%"

# Wait for all threads to complete
for t in threads:
    t.join()

print "################################################"

info.reorder(bc)
info.showMatrix()
info.countFrobemious()