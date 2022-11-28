class Matrix:
    nums = []
    def read(self):
        self.nums = []
        [self.nums.append(list(map(int,x.split(',')))) for x in input()[2:-2].split('],[')]

    def add(self,B):
        for i in range(0,len(self.nums)):
            for j in range(0,len(self.nums[0])):
                self.nums[i][j] += B.nums[i][j]
    
    def print(self):
        out = []
        [out.append('[' + ','.join(str(x) for x in i) + ']') for i in self.nums]
        print('[{}]'.format(','.join(str(x) for x in out)),end='')


nm = list(map(int,input().split()))
A = Matrix()
B = Matrix()
A.read()
B.read()
A.add(B)
A.print()


