x = -1230

y = str(x)
l = []
s = ""
for i in range(len(y)):
    l.append(y[-i - 1])
o = s.join(l)
if o[-1] == '-':
    o = int(o[:-1])
    output = -o
else:
    output = int(o)
print(output)
