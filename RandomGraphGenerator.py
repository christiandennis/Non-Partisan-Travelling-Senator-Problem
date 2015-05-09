import random

print('Size: ')
N = int(input())

print('Output file: ')
baji = str(input())

fout = open(str(baji) + '.in', 'w')
lst = [[0 for _ in range(N)] for _ in range(N)]
for i in range( N):
	for j in range(N):
		if j>i:
			lst[i][j] = random.randint(0, 100)
		elif i>j:
			lst[i][j] = lst[j][i]
			
fout.write(str(N)+'\n')
for i in range(N):
	for j in range(N):
		fout.write(str(lst[i][j])+" ")
	fout.write('\n')


