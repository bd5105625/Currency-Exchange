a = {"ab":1, "cd":2}
# b = [1,2,3]
di = {"1":a}
print(di["1"])
a["ab"] = 100
print(a)
print(di["1"])