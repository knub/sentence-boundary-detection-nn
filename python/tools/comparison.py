import math, sys
import numpy

OUR = "/home/tanja/Desktop/output"
XIAOYIN_DATA = "/home/tanja/Desktop/xiayin_data"
XIAOYIN_LABEL = "/home/tanja/Desktop/xiayin_label"

WINDOW = 80
TAKE = 12000
COUNT = 12000
SKIP = 2
DIFF = 0.001
INSTANCE_SIZE = 250

our_data = numpy.zeros((TAKE, INSTANCE_SIZE))
our_label = []
xiaoyin_data = numpy.zeros((TAKE, INSTANCE_SIZE))
xiaoyin_label = []

instance_count = 0
with open(OUR, "r") as file_:
    for line in file_:
        if instance_count >= TAKE:
            continue

        line = line.rstrip()
        label = line[-1]
        our_label.append(float(label))

        line = line[1:-4]
        parts = line.split(", ")
        for i, p in enumerate(parts):
            our_data[instance_count][i] = float(p)

        instance_count += 1

instance_count = 0
with open(XIAOYIN_LABEL, "r") as file_:
    for line in file_:
        if instance_count >= TAKE:
            continue
        if instance_count < SKIP:
            instance_count += 1
            continue
        line = line.rstrip()
        xiaoyin_label.append(float(line))
        instance_count += 1

instance_count = 0
with open(XIAOYIN_DATA, "r") as file_:
    for line in file_:
        if instance_count >= TAKE:
            continue
        if instance_count < SKIP:
            instance_count += 1
            continue
        parts = line.split("\t")
        for i, p in enumerate(parts):
            xiaoyin_data[instance_count][i] = float(p)
        instance_count += 1

assert(len(our_data)  == len(xiaoyin_data))
assert(len(our_label) - SKIP == len(xiaoyin_label))


def check_instance(a, b):
    for i in range(INSTANCE_SIZE):
        if DIFF < math.fabs(a[i] - b[i]):
            return False
    return True


count_label = 0
count_data = 0


for instance_nr in range(TAKE):
    equal = False
    for i in range(max(0, instance_nr - WINDOW), min(instance_nr + WINDOW, TAKE)):
        if check_instance(our_data[instance_nr], xiaoyin_data[i]):
            equal = True
            continue
    if not equal:
        count_data += 1

print("DATA", float(count_data) / TAKE)


# for i in range(len(xiaoyin_label)):
#     if our_label[i] != xiaoyin_label[i]:
#         for j in range(max(0, i-WINDOW), min(len(xiaoyin_label), i + WINDOW)):
#             if our_label[j] == xiaoyin_label[i] or our_label[i] == xiaoyin_label[j]:
#                 continue
#         count_label += 1

print("LABEL", float(count_label) / COUNT)
