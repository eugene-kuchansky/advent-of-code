"""
9 10
9 9

9*10-9*9

9 10 10
9 9 9

100 999



9 10 10 10 10 10
9 8 7 6 5 4


9 10 10
9 9 10
9 9 9
"""
from time import time
start = 240920
stop = 789857

class Num(object):
    def __init__(self, int_num):
        self.num_list = []
        self.num_list.append(int_num // 100000)
        self.num_list.append(int_num // 10000 % 10)
        self.num_list.append(int_num // 1000 % 10)
        self.num_list.append(int_num // 100 % 10)
        self.num_list.append(int_num // 10 % 10)
        self.num_list.append(int_num % 10)

    def to_int(self):
        n = 0
        for i in range(6):
            n += self.num_list[i] * 10**(5 - i)
        return n
    
    def inc(self):
        for i in range(5, -1, -1):
            self.num_list[i] += 1
            if self.num_list[i] == 10:
                self.num_list[i] = self.num_list[i - 1]
            else:
                break
    
    def is_incr(self):
        for i in range(1, 6, 1):
            if self.num_list[i] < self.num_list[i - 1]:
                return False
        return True
    
    def is_2_same(self):
        for i in range(5):
            if self.num_list[i] == self.num_list[i + 1]:
                return True
        return False

    def is_2_only_same(self):
        for i in range(5):
            if i == 0:
                if self.num_list[i] == self.num_list[i + 1] and self.num_list[i + 1] != self.num_list[i + 2]:
                    return True
            elif i == 4:
                if self.num_list[i] == self.num_list[i + 1] and self.num_list[i] != self.num_list[i - 1]:
                    return True
            else:
                if self.num_list[i] == self.num_list[i + 1] and self.num_list[i + 1] != self.num_list[i + 2] and self.num_list[i] != self.num_list[i - 1]:
                    return True
        return False

t = time()
res1 = 0
res2 = 0
#n = Num(777999)
#print(n.is_2_only_same())
#exit()
num = Num(start)
while num.to_int() <= stop:
    if num.is_incr():
        if num.is_2_same():
            res1 += 1
        if num.is_2_only_same():
            res2 += 1
    num.inc()
print(res1)
print(res2)
print(time() - t)

t = time()
res1 = 0
res2 = 0
for i6 in range(1, 10):
    for i5 in range(i6, 10):
        for i4 in range(i5, 10):
            for i3 in range(i4, 10):
                for i2 in range(i3, 10):
                    for i1 in range(i2, 10):
                        num = i6 * 100000 + i5 * 10000 + i4 * 1000 + i3 * 100 + i2 * 10 + i1  
                        if 789857 >= num >= 240920:
                            if i6 <= i5 <= i4 <= i3 <= i2 <=i1:
                                if i6 == i5 or i5 == i4 or i4 == i3 or i3 == i2 or i2 == i1:
                                    res1 +=1
                                if (i6 == i5 and i5 != i4) or \
                                        (i5 == i4 and i4 != i3  and i5 != i6) or \
                                        (i4 == i3 and i3 != i2 and i4 != i5) or \
                                        (i3 == i2 and i2 != i1 and i3 != i4) or \
                                        (i2 == i1 and i3 != i2):
                                    res2 +=1
                            
#print(total)
print(res1)
print(res2)
print(time() - t)
            
#print(9*10*10 - 9 * 8 * 9 - 9 * 8 - 9)

            
