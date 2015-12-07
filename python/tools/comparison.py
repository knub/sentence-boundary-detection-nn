import math

OUR = "/home/tanja/Desktop/output"
XIAOYIN_DATA = "/home/tanja/Desktop/xiayin_data"
XIAOYIN_LABEL = "/home/tanja/Desktop/xiayin_label"

WINDOW = 5

our_data = []
our_label = []
xiaoyin_data = []
xiaoyin_label = []

with open(OUR, "r") as file_:
    for line in file_:
        line = line.rstrip()
        label = line[-1]
        our_label.append(float(label))

        line = line[1:-4]
        parts = line.split(", ")
        for p in parts:
            p = float(p)
            p = math.ceil(p * 1000)/1000
            our_data.append(float(p))

i = 0
with open(XIAOYIN_LABEL, "r") as file_:
    for line in file_:
        i += 1
        if i < 3:
            continue
        line = line.rstrip()
        xiaoyin_label.append(float(line))

i = 0
with open(XIAOYIN_DATA, "r") as file_:
    for line in file_:
        i += 1
        if i < 3:
            continue
        parts = line.split("\t")
        for p in parts:
            p = float(p)
            p = math.ceil(p * 1000)/1000
            xiaoyin_data.append(p)

assert(len(our_data) - 500 == len(xiaoyin_data))
assert(len(our_label) - 2 == len(xiaoyin_label))


count_label = 0
count_data = 0

for i in range(len(xiaoyin_data)):
    if our_data[i] != xiaoyin_data[i]:
        for j in range(max(0, i-WINDOW), min(len(xiaoyin_data), i + WINDOW)):
            if our_data[j] == xiaoyin_data[i] or our_data[i] == xiaoyin_data[j]:
                continue
        count_data += 1
        # print("ASSERTION FAILED!")
        # print("OUR", our_data[i], "XIAOYIN", xiaoyin_data[i])

for i in range(len(xiaoyin_label)):
    if our_label[i] != xiaoyin_label[i]:
        for j in range(max(0, i-WINDOW), min(len(xiaoyin_label), i + WINDOW)):
            if our_label[j] == xiaoyin_label[i] or our_label[i] == xiaoyin_label[j]:
                continue
        count_label += 1
        # print("ASSERTION FAILED!")
        # print("OUR", our_label[i], "XIAOYIN", xiaoyin_label[i])


print(float(count_data) / (12000.0 * 250))
print(float(count_label) / 12000.0)
