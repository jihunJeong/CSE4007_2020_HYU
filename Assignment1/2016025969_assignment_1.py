from collections import deque
import heapq
import sys
import copy
import math

sys.setrecursionlimit(10**6)

def backtracking(visited, ans, start, end, length):
	avl_x = [0, -1, 0, 1]
	avl_y = [1, 0, -1, 0]
	w, h = len(ans[0]), len(ans)

	ans[end[0]][end[1]] = 5
	y, x = end[0], end[1]

	while x != start[1] or y != start[0]:
		for i in range(4):
			ny = y + avl_y[i]
			nx = x + avl_x[i]
			if 0 <= nx and 0 <= ny and w > nx and h > ny:
				if visited[ny][nx] == visited[y][x] - 1:
					ans[ny][nx] = 5
					length += 1
					y, x  = ny, nx
					break
	return ans, length

def bfs(arr, start, end, k_pos, f_name):
	maze = copy.deepcopy(arr)
	ans = copy.deepcopy(maze)
	length, s = 0, copy.deepcopy(start)				
	dq = deque([[start[0],start[1], 0]])
	avl_x = [0, -1, 0, 1]
	avl_y = [1, 0, -1, 0]

	w, h, time = len(maze[0]), len(maze), 0
	visited = [[0 for x in range(w)] for y in range(h)]
	visited[start[0]][start[1]] = 3

	while dq:
		idx = dq.popleft()

		for i in range(4):
			nx = idx[1] + avl_x[i]
			ny = idx[0] + avl_y[i]
			nkey = idx[2]
			if 0 <= nx and 0 <= ny and w > nx and h > ny:
				if maze[ny][nx] == 4 and nkey == len(k_pos):
					visited[ny][nx] = visited[idx[0]][idx[1]] + 1
					e = [ny, nx]
					ans, length = backtracking(visited, ans, s, e, length)
					ans[start[0]][start[1]], ans[end[0]][end[1]] = 3, 4
					
					f = open(f_name+"_BFS_output.txt", "w")
					print('')
					for i in range(h):
						f.write("".join(map(str, ans[i]))+"\n")
					f.write("---\n")
					f.write("length={}\n".format(length))
					f.write("time={}".format(time))
					f.close()
					return True

				if maze[ny][nx] != 1 and visited[ny][nx] == 0:
					visited[ny][nx] = visited[idx[0]][idx[1]] + 1
					time += 1
					
					if maze[ny][nx] == 6:
						e = [ny, nx]
						ans, length = backtracking(visited, ans, s, e, length)
						nkey += 1
						
						dq = deque()
						visited = [[0 for x in range(w)] for y in range(h)]
						visited[ny][nx] = 3
						s = [ny, nx]
						maze[ny][nx] = 2
						dq.append([ny, nx, nkey])
						break
									
					dq.append([ny, nx, nkey])

ids_time = 0

def dls(arr, start, end, depth, k_pos, f_name):
	global ids_time
	maze = copy.deepcopy(arr)
	ans = copy.deepcopy(maze)
	k_list = copy.deepcopy(k_pos)
	stack = [[start[0], start[1], 0]]
	length, s = 0, copy.deepcopy(start)

	avl_x = [0, -1, 0, 1]
	avl_y = [1, 0, -1, 0]

	w, h, time, chk_depth = len(maze[0]), len(maze), 0, 0

	visited = [[0 for x in range(w)] for y in range(h)]
	visited[start[0]][start[1]] = 3

	while stack and chk_depth < depth:
		idx = stack.pop()

		for i in range(4):
			nx = idx[1] + avl_x[i]
			ny = idx[0] + avl_y[i]
			nkey = idx[2]
			chk = False
			if 0 <= nx and 0 <= ny and w > nx and h > ny:	
				if maze[ny][nx] == 4 and nkey == len(k_pos):
					visited[ny][nx] = visited[idx[0]][idx[1]] + 1
					e = [ny, nx]
					ans, length = backtracking(visited, ans, s, e, length)
					ans[start[0]][start[1]], ans[end[0]][end[1]] = 3, 4
					
					f = open(f_name+"_IDS_output.txt", "w")
					for i in range(h):
						f.write("".join(map(str, ans[i]))+"\n")
					f.write("---\n")
					f.write("length={}\n".format(length))
					f.write("time={}".format(ids_time))
					f.close()
					return True

				if maze[ny][nx] != 1 and visited[ny][nx] == 0:
					visited[ny][nx] = visited[idx[0]][idx[1]] + 1
					chk_depth += 1
					ids_time += 1
					chk = True
					
					if maze[ny][nx] == 6:
						e = [ny, nx]
						ans, length = backtracking(visited, ans, s, e, length)
						nkey += 1
						stack = []
						visited = [[0 for x in range(w)] for y in range(h)]
						visited[ny][nx], maze[ny][nx] = 3, 2
						s = [ny, nx]
						chk_depth += 1
						stack.append([ny, nx, nkey])
						break
					
					stack.append([idx[0], idx[1], nkey])
					stack.append([ny, nx, nkey])
					break

		if chk == False:
			chk_depth -= 1
	return False

def ids(maze, start, end, k_pos, f_name):
	global ids_time
	ids_time = 0
	for depth in range(0, 1000000000):
		if dls(maze, start, end, depth, k_pos, f_name):
			break

class Point:
	def __init__(self, y, x, nkey, heuristic, cost = 0):
		self.x = x
		self.y = y
		self.nkey = nkey
		self.cost = cost
		self.priority = heuristic + cost

	def __lt__(self, other):
		return self.priority < other.priority

def gbfs(arr, start, end, k_pos, f_name):
	heap, s = [], copy.deepcopy(start)
	maze, k_list = copy.deepcopy(arr), copy.deepcopy(k_pos)
	ans, length, heuristic = copy.deepcopy(maze), 0, 10000000
	for i in range(len(k_list)):
		heuristic = min(heuristic, abs(k_list[i][0]-start[0])+abs(k_list[i][1]-start[1]))					
	if not k_pos:
		heuristic = abs(end[0]-start[0])+abs(end[1]-start[1])

	sp = Point(start[0], start[1], 0, heuristic)
	heapq.heappush(heap, sp)
	
	avl_x = [0, -1, 0, 1]
	avl_y = [1, 0, -1, 0]

	w, h, time = len(maze[0]), len(maze), 0
	visited = [[0 for x in range(w)] for y in range(h)]
	visited[start[0]][start[1]] = 1

	while heap:
		cp = heapq.heappop(heap)
		for i in range(4):
			ny = cp.y + avl_y[i] 
			nx = cp.x + avl_x[i]
			nkey = cp.nkey

			if 0 <= nx and 0 <= ny and w > nx and h > ny:
				if maze[ny][nx] == 4 and nkey == len(k_pos):
					visited[ny][nx] = visited[cp.y][cp.x] + 1
					e = [ny, nx]
					ans, length = backtracking(visited, ans, s, e, length)
					ans[start[0]][start[1]], ans[end[0]][end[1]] = 3, 4
					
					f = open(f_name+"_GBFS_output.txt", "w")
					for i in range(h):
						f.write("".join(map(str, ans[i]))+"\n")
					f.write("---\n")
					f.write("length={}\n".format(length))
					f.write("time={}".format(time))
					f.close()
					return True

				if maze[ny][nx] != 1 and visited[ny][nx] == 0:
					visited[ny][nx] = visited[cp.y][cp.x] + 1
					time += 1
					if maze[ny][nx] == 6:
						e = [ny, nx]
						ans, length = backtracking(visited, ans, s, e, length)
						nkey += 1
						heap = []
						k_list.remove([ny, nx])
						visited = [[0 for x in range(w)] for y in range(h)]
						visited[ny][nx], maze[ny][nx] = 3, 2
						s = [ny, nx]

						if not k_pos:
							heuristic = abs(end[0]-ny)+abs(end[1]-nx)
						else :
							for i in range(len(k_list)):
								heuristic = min(heuristic, abs(k_list[i][0]-ny)+abs(k_list[i][1]-nx))
						
						np = Point(ny, nx, nkey, heuristic)
						heapq.heappush(heap, np)
						break

					if not k_pos:
							heuristic = abs(end[0]-ny)+abs(end[1]-nx)
					else :
						for i in range(len(k_list)):
							heuristic = min(heuristic, abs(k_list[i][0]-ny)+abs(k_list[i][1]-nx))

					np = Point(ny, nx, nkey, heuristic)
					heapq.heappush(heap, np)
					

def a_star(arr, start, end, k_pos, f_name):
	heap, s = [], copy.deepcopy(start)
	maze, k_list = copy.deepcopy(arr), copy.deepcopy(k_pos)
	ans, length, heuristic = copy.deepcopy(maze), 0, 10000000
	for i in range(len(k_list)):
		heuristic = min(heuristic, abs(k_list[i][0]-start[0])+abs(k_list[i][1]-start[1]))					
	if not k_pos:
		heuristic = abs(end[0]-start[0])+abs(end[1]-start[1])

	sp = Point(start[0], start[1], 0, heuristic)
	heapq.heappush(heap, sp)
	
	avl_x = [0, -1, 0, 1]
	avl_y = [1, 0, -1, 0]

	w, h, time = len(maze[0]), len(maze), 0
	visited = [[0 for x in range(w)] for y in range(h)]
	visited[start[0]][start[1]] = 1

	while heap:
		cp = heapq.heappop(heap)
		for i in range(4):
			ny = cp.y + avl_y[i] 
			nx = cp.x + avl_x[i]
			nkey = cp.nkey
			nc = cp.cost + 1

			if 0 <= nx and 0 <= ny and w > nx and h > ny:
				if maze[ny][nx] == 4 and nkey == len(k_pos):
					visited[ny][nx] = visited[cp.y][cp.x] + 1
					e = [ny, nx]
					ans, length = backtracking(visited, ans, s, e, length	)
					ans[start[0]][start[1]], ans[end[0]][end[1]] = 3, 4
					
					f = open(f_name+"_A_star_output.txt", "w")
					for i in range(h):
						f.write("".join(map(str, ans[i]))+"\n")
					f.write("---\n")
					f.write("length={}\n".format(length))
					f.write("time={}".format(time))
					f.close()
					return True

				if maze[ny][nx] != 1 and visited[ny][nx] == 0:
					visited[ny][nx] = visited[cp.y][cp.x] + 1
					time += 1
					if maze[ny][nx] == 6:
						e = [ny, nx]
						ans, length = backtracking(visited, ans, s, e, length)
						nkey += 1
						heap = []
						k_list.remove([ny, nx])
						visited = [[0 for x in range(w)] for y in range(h)]
						visited[ny][nx], maze[ny][nx] = 3, 2
						s = [ny, nx]

						if not k_pos:
							heuristic = abs(end[0]-ny)+abs(end[1]-nx)
						else :
							for i in range(len(k_list)):
								heuristic = min(heuristic, abs(k_list[i][0]-ny)+abs(k_list[i][1]-nx))
						
						np = Point(ny, nx, nkey, heuristic, nc)
						heapq.heappush(heap, np)
						break

					if not k_pos:
							heuristic = abs(end[0]-ny)+abs(end[1]-nx)
					else :
						for i in range(len(k_list)):
							heuristic = min(heuristic, abs(k_list[i][0]-ny)+abs(k_list[i][1]-nx))

					np = Point(ny, nx, nkey, heuristic, nc)
					heapq.heappush(heap, np)
def sol(f_name):
	file = open(f_name, "r")
	f_name = f_name[:-4]
	print(f_name)
	info = list(map(int, file.readline().split()))
	arr = [[0 for x in range(info[2])] for y in range(info[1])]
	index = 0
	
	while True:
		line = file.readline().strip('\n')
		if not line:
			break

		arr[index] = list(map(int, line))
		index += 1


	k_cnt = 0
	k_pos = []
	
	for i in range(info[1]):
		for j in range(info[2]):
			if arr[i][j] == 3:
				start = [i, j]	
			elif arr[i][j] == 6:
				k_pos.append([i,j])
			elif arr[i][j] == 4:
				end = [i, j]
	file.close()


	bfs(arr, start, end, k_pos, f_name)
	ids(arr, start, end, k_pos, f_name)
	gbfs(arr, start, end, k_pos, f_name)
	a_star(arr, start, end, k_pos, f_name)	

if __name__ == "__main__":
	sol("Maze_1.txt")
	sol("Maze_2.txt")
	sol("Maze_3.txt")
	sol("Maze_4.txt")
	#sol("Maze_practice.txt")
	'''
	input_file_name = input()
	sol(input_file_name)
	'''