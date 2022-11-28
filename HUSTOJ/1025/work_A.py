class Stack:
    len = 0
    array = []
    array_pop = []

    def __init__(self) -> None:
        pass

    def init(self):
        self.array = list(map(int,input().split()))

    def read(self):
        opt = input().split()
        if opt[0] == 'pop':
            try:
                for i in range(0,int(opt[1])):
                    temp = self.array.pop()
                    self.array_pop.append(temp)
            except Exception as e:
                pass
        elif opt[0] == 'push':
            for i in range(1,len(opt)):
                self.array.append(int(opt[i]))
    
    def _printArray(self,data):
        print('len = {}'.format(len(data)),end='')
        print(', data = {}'.format(' '.join(str(x) for x in data)) if len(data) > 0 else '')
        
    
    def print(self):
        self._printArray(self.array)

    def print_pop(self):
        self._printArray(self.array_pop)


n = input()
s = Stack()
s.init()
s.read()
s.read()

s.print()
s.print_pop()

