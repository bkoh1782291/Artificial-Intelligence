txt = "oxxxo-ox-"

a = []

for x in txt:
	a.append(x)

print(a)

b = [[],[],[]]

list_count = 0

for y in a:
    if list_count <= 5 and list_count >= 3:
    	b[1].append(y)
    elif list_count <= 8 and list_count >= 6:
    	b[2].append(y)
    elif list_count <= 2 and list_count >= 0:
    	b[0].append(y)
    list_count += 1

print(b)
    	