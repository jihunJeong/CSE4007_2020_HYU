import math

def get_data(f_name):
    file = open(f_name, "r")
    f_name = f_name[:-4]
	print(f_name)

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

def write_data(ans, name):
    f = open(name+"_output.txt", "a")
    f.write("---\n")
	for i in range(h):
		f.write("".join(map(str, ans[i]))+"\n")
	
    f.close()

def cosine_similarity(v1, v2):
    return simil

def single_cluster(data):

    
    return ans

def complete_cluster(data):
    
    return ans

def average_cluster(data):
    
    return ans

def clustered(data, name):
    f = open(name+"_output.txt", "a")
    num = name[name.find('_')+1:]
    f.write(num+"\n")
    f.close()
    
    ans = single_cluster(data)
    write_data(ans, name)
    ans = complete_cluster(data)
    write_data(ans, name)
    ans = average_cluster(data)
    write_data(ans, name)
    
if __name__ == "__main__":
    data, name = get_data("CoordinatePlane_1.txt")
    clustered(data, name)

    data, name = get_data("CoordinatePlane_2.txt")
    clustered(data, name)

    data, name = get_data("CoordinatePlane_3.txt")
    clustered(data, name)

    # data, name = get_data( input_here )
    # clustered(data, name)