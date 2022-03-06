class testtile:
    def __init__(self, val) ->None:
        self.val = val
    
    def getEntropy(self):
        return self.val

class NodeMinHeap:
    def __init__(self) -> None:
        self.theHeap = []
    
    def push(self, pushThis):
        self.theHeap.append(pushThis) 
        n = int((len(self.theHeap)//2)-1)
        for k in range(n, -1, -1):
            self.minHeapify(k)

    def remove(self, removeThis):
        self.theHeap.remove(removeThis)
        self.minHeapify(len(self.theHeap) - 1)
        pass

    def poproot(self):
        p = int((len(self.theHeap)-1)/2)
        min = self.theHeap.pop(p)
        self.minHeapify(p)
        return min

    def minHeapify(self,k):
        l = 2 * k + 1
        r = 2 * k + 2
        if l < len(self.theHeap) and self.theHeap[l].getEntropy() < self.theHeap[k].getEntropy():
            smallest = l
        else:
            smallest = k
        if r < len(self.theHeap) and self.theHeap[r].getEntropy() < self.theHeap[smallest].getEntropy():
            smallest = r
        if smallest != k:
            self.theHeap[k], self.theHeap[smallest] = self.theHeap[smallest], self.theHeap[k]
            self.minHeapify(smallest)


    def theHeappp(self):
        return [x.val for x in self.theHeap]

class NodeMinHeap2:
    def __init__(self) -> None:
        self.theHeap = []
        self.size = 0

    def swap(self, a, b):
        self.theHeap[a], self.theHeap[b] = self.theHeap[b], self.theHeap[a]
    
    def push(self, pushThis):
        self.size+= 1
        self.theHeap.append(pushThis)
        current = self.size-1
        while self.theHeap[current].getEntropy() < self.theHeap[current//2].getEntropy():
            self.swap(current, current//2)
            current = current//2

    def poproot(self):
        root = int((self.size-1)/2)
        min = self.theHeap[root]
        self.theHeap[root] = self.theHeap[self.size]
        self.size -= 1
        self.min_heapify(root)
        return min

    def min_heapify(self, i):
        if not (i >= (self.size//2) and i <= self.size):
            if (self.theHeap[i].getEntropy() > self.theHeap[2 * i].getEntropy()  or  self.theHeap[i].getEntropy() > self.theHeap[(2 * i) + 1].getEntropy()): 
                if self.theHeap[2 * i] < self.theHeap[(2 * i) + 1]:
                    self.swap(i, 2 * i)
                    self.min_heapify(2 * i)
                else:
                    self.swap(i, (2 * i) + 1)
                    self.min_heapify((2 * i) + 1)
        pass

    def theHeappp(self):
        return [x.val for x in self.theHeap]



class NodeMinHeap3:
    def __init__(self, maxsize) -> None:
        self.maxsize = maxsize
        self.theHeap = [0] * (maxsize - 1)
        self.theHeap[0] = -1
        self.size = 0
        self.root = 1

    def swap(self, a, b):
        self.theHeap[a], self.theHeap[b] = self.theHeap[b], self.theHeap[a]
    
    def push(self, pushThis):
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.theHeap[self.size] = pushThis 
        current = self.size
        while self.theHeap[current].getEntropy() < self.theHeap[current//2].getEntropy():
            self.swap(current, current//2)
            current = current//2

    def poproot(self):
        min = self.theHeap[self.root]
        self.theHeap[self.root] = self.theHeap[self.size]
        self.size -= 1
        self.min_heapify(self.root)
        return min

    def min_heapify(self, i):
        if not (i >= (self.size//2) and i <= self.size):
            if (self.theHeap[i].getEntropy() > self.theHeap[2 * i].getEntropy()  or  self.theHeap[i].getEntropy() > self.theHeap[(2 * i) + 1].getEntropy()): 
                if self.theHeap[2 * i] < self.theHeap[(2 * i) + 1]:
                    self.swap(i, 2 * i)
                    self.min_heapify(2 * i)
                else:
                    self.swap(i, (2 * i) + 1)
                    self.min_heapify((2 * i) + 1)
        pass

    def theHeappp(self):
        return [x.val for x in self.theHeap]

heep = NodeMinHeap2()
print(heep.theHeappp())
heep.push(testtile(6))
print("push 6:", heep.theHeappp())
heep.push(testtile(1))
print("push 1:", heep.theHeappp())
heep.push(testtile(3))
print("push 3:", heep.theHeappp())
heep.push(testtile(2))
print("push 2:", heep.theHeappp())
heep.push(testtile(4))
print("push 4:", heep.theHeappp())


print("popped", heep.poproot().val)
print(heep.theHeappp())
print("popped", heep.poproot().val)
print(heep.theHeappp())
print("popped", heep.poproot().val)
print(heep.theHeappp())

