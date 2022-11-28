class Vec:
    x = 0
    y = 0
    z = 0

    def __init__(self) -> None:
        pass

    def read(self):
        num = list(map(int,input().split()))
        self.x = num[0]
        self.y = num[1]
        self.z = num[2]

    def add(self,t,mode = 1):
        self.x = self.x + mode * t.x
        self.y = self.y + mode * t.y
        self.z = self.z + mode * t.z

    def sub(self,t):
        self.add(t,-1)
    
    def mul(self,t):
        self.x = self.x * t
        self.y = self.y * t
        self.z = self.z * t
    
    def div(self,t):
        self.x = self.x / t
        self.y = self.y / t
        self.z = self.z / t
    
    def x_out(self,x,e=' '):
        if x - int(x) == 0:
            print(x,end=e)
        else:
            print('%.2f' % x,end=e)

    def output(self):
        print('%.2f %.2f %.2f' % (self.x,self.y,self.z))
    
    def output_int(self):
        print('{} {} {}'.format(self.x,self.y,self.z))

    def length(self):
        print('%.2f' % (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5)

vec_1 = Vec()
vec_2 = Vec()
vec_1.read()
vec_2.read()

opt = input()
if opt == 'add':
    vec_1.add(vec_2)
elif opt == 'sub':
    vec_1.sub(vec_2)
elif opt == 'mul':
    vec_1.mul(int(input()))
elif opt == 'div':
    vec_1.div(int(input()))
elif opt == 'get_length':
    vec_1.length()

if(opt != 'get_length'):
    if opt == 'div':
        vec_1.output()
    else:
        vec_1.output_int()
