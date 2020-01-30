import fileinput
#sum all numbers given
#print as int if it is an integer never, which means without leading
# .[NUMBER] or decimal part,
# if it as a float number print it with decimal part

lines = []

for line in fileinput.input():
    lines.append(line)

sum = 0
for number in lines:
    sum = sum + float(number)

isInt = (abs(sum) - abs((int(sum))) == 0)
if isInt:
    print(int(sum))
else:
    print(sum)
