import math, sys

OUR = "/home/tanja/Desktop/output"
XIAOYIN_DATA = "/home/tanja/Desktop/xiayin_data"
XIAOYIN_LABEL = "/home/tanja/Desktop/xiayin_label"

WINDOW = 20
TAKE = 12000
COUNT = 12000
SKIP = 2
DIFF = 0.001

our_data = []
our_label = []
xiaoyin_data = []
xiaoyin_label = []

i = 0
with open(OUR, "r") as file_:
    for line in file_:
        if i > TAKE:
            continue
        i += 1
        line = line.rstrip()
        label = line[-1]
        our_label.append(float(label))

        line = line[1:-4]
        parts = line.split(", ")
        for p in parts:
            our_data.append(float(p))

i = 0
with open(XIAOYIN_LABEL, "r") as file_:
    for line in file_:
        if i > TAKE:
            continue
        if i < SKIP:
            i += 1
            continue
        i += 1
        line = line.rstrip()
        xiaoyin_label.append(float(line))

i = 0
with open(XIAOYIN_DATA, "r") as file_:
    for line in file_:
        if i > TAKE:
            continue
        if i < SKIP:
            i += 1
            continue
        i += 1
        parts = line.split("\t")
        for p in parts:
            xiaoyin_data.append(float(p))

assert(len(our_data) - (250 * SKIP) == len(xiaoyin_data))
assert(len(our_label) - SKIP == len(xiaoyin_label))


count_label = 0
count_data = 0

for i in range(len(xiaoyin_data)):
    if DIFF < math.fabs(our_data[i] - xiaoyin_data[i]):
        instance_nr = int(i / 250)
        index = i - (instance_nr * 250)

        print(our_data[i])
        print(xiaoyin_data[i])
        print("INSTANCE_NR", instance_nr)
        print("INDEX", index)
        sys.exit(0)

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


print("DATA", float(count_data) / (COUNT * 250))
print("LABEL", float(count_label) / COUNT)
