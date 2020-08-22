"""
If you find the visualized obj are all white, please run this code
"""

import os, sys, shutil

def main():
    in_file = "objs/gt.obj"
    out_file = "objs/gt_new.obj"

    with open(in_file, "r") as in_f:
        with open(out_file, "w") as out_f:
            for line in in_f:
                if line[0] == "v":
                    record = line.strip().split()
                    for i in range(4, 7):
                        record[i] = str(float(record[i])/255.0)
                    new_line = " ".join(record) + "\n"
                    out_f.write(new_line)
                else:
                    out_f.write(line)


if __name__ == '__main__':
    main()
