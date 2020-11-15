import math
import copy

class DisjointSet:
    def __init__(self, n):
        self.data = list(range(n))
        self.size = n

    def find(self, index):
        return self.data[index]
        
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        for i in range(self.size):
            if x <= y and self.find(i) == y:
                self.data[i] = x
            elif x > y and self.find(i) == x:
                self.data[i] = y

    def length(self):
        return len(set(self.data))

def get_data(f_name):
    file = open(f_name, "r")
    f_name = f_name[:-4]
	#print(f_name)
    info = list(map(int, file.readline().split()))
    data = [[0 for x in range(2)] for y in range(info[1])]
    index = 0

    while True:
        line = file.readline().strip('\n')
        if not line:
            break

        data[index] = list(map(int, line.split(',')))
        index += 1
    
    file.close()
    return data, f_name

def write_data(name, ans, span, option):
    f = open(name+"_output.txt", "a")
    f.write("---\n")
    f.write(option+"\n")
    f.write("clusters: ")
    for i in range(len(ans)):
        f.write("["+",".join(map(str, ans[i])) + "] ")
    
    f.write("\n")
    f.write("span: {}, {}\n".format(span[0], span[1]))
	
    f.close()

def cosine_similarity(v1, v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x, y = v1[i], v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    
    return  sumxy/math.sqrt(sumxx*sumyy)

def single_cluster(data):
    table = copy.deepcopy(data)
    tot = len(data)
    span = [1, 1]
    ans = DisjointSet(tot)

    while ans.length() >= 3:
        max_val, item1, item2 = 0, 0, 0
        for diagonal in range(len(table)):
            for i in range(diagonal+1, len(table)):
                if max_val < table[diagonal][i]:
                    max_val = table[diagonal][i]
                    item1, item2 = diagonal, i
        span[0] = span[1]
        span[1] = max_val
        if ans.length() == 3:
            break
        
        ans.union(item1, item2)
    
        for i in range(len(table)):
            if item1 != i:
                table[item1][i] = max(table[item1][i], table[item2][i])
                table[i][item1] = table[item1][i]
            table[item2][i] = -10
            table[i][item2] = -10

    return ans, span

def complete_cluster(data):
    table = copy.deepcopy(data)
    tot = len(data)
    span = [1, 1]
    ans = DisjointSet(tot)

    while ans.length() >= 3:
        max_val, item1, item2 = -10, 0, 0
        for diagonal in range(len(table)):
            for i in range(diagonal+1, len(table)):
                if max_val < table[diagonal][i]:
                    max_val = table[diagonal][i]
                    item1, item2 = diagonal, i
        span[0] = span[1]
        span[1] = max_val
        if ans.length() == 3:
            break
    
        ans.union(item1, item2)
        
        table[item2][item1] = -10
        table[item1][item2] = -10
        for i in range(len(table)):
            if item1 != i:
                table[item1][i] = min(table[item1][i], table[item2][i])
                table[i][item1] = table[item1][i]
            table[item2][i] = -10
            table[i][item2] = -10

    return ans, span

def average_cluster(data):
    table = copy.deepcopy(data)
    tot = len(data)
    span = [1, 1]
    ans = DisjointSet(tot)

    while ans.length() >= 3:
        max_val, item1, item2 = -10, 0, 0
        for diagonal in range(len(table)):
            for i in range(diagonal+1, len(table)):
                if max_val < table[diagonal][i]:
                    max_val = table[diagonal][i]
                    item1, item2 = diagonal, i
        span[0] = span[1]
        span[1] = max_val
        if ans.length() == 3:
            break
    
        ans.union(item1, item2)
        
        table[item2][item1] = -10
        table[item1][item2] = -10
        for i in range(len(table)):
            if item1 != i:
                table[item1][i] = min(table[item1][i], table[item2][i])
                table[i][item1] = table[item1][i]
            table[item2][i] = -10
            table[i][item2] = -10

    return ans, span

def indexToVertex(ans, data):
    cl1, cl2, cl3, cnt = -1, -1, -1, 0
    for i in set(ans.data):
        if cnt == 0:
            cl1 = i
        elif cnt == 1:
            cl2 = i
        elif cnt == 2:
            cl3 = i
        cnt += 1

    nans = [[], [], []]
    for i in range(len(ans.data)):
        idx = 0
        if ans.data[i] == cl1:
            idx = 0
        elif ans.data[i] == cl2:
            idx = 1
        elif ans.data[i] == cl3:
            idx = 2       
        nans[idx].append((data[i][0], data[i][1]))

    return nans

def clustered(data, name):
    f = open(name+"_output.txt", "a")
    num = name[name.find('_')+1:]
    f.write(num+"\n")
    f.close()

    table = [[-10 for x in range(len(data))] for y in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                continue
            table[i][j] = cosine_similarity(data[i], data[j])

    ans, span = single_cluster(table)
    info = indexToVertex(ans, data)
    write_data(name, info, span, "single")

    ans, span = complete_cluster(table)
    info = indexToVertex(ans, data)
    write_data(name, info, span, "complete")
    '''
    ans, span = average_cluster(table)
    info = indexToVertex(ans, data)    
    write_data(name, info, span, "average")
    '''
if __name__ == "__main__":
    print("Coordinate_Practice... ", end="")
    data, name = get_data("CoordinatePlane_practice.txt")
    clustered(data, name)
    print("Done")

    print("Coordinate_1... ", end="")
    data, name = get_data("CoordinatePlane_1.txt")
    clustered(data, name)
    print("Done")

    print("Coordinate_2... ", end="")
    data, name = get_data("CoordinatePlane_2.txt")
    clustered(data, name)
    print("Done")

    print("Coordinate_3... ", end="")
    data, name = get_data("CoordinatePlane_3.txt")
    clustered(data, name)
    print("Done")

    # data, name = get_data( input_here )
    # clustered(data, name)