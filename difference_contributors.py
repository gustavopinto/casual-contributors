import os, glob, sys

path = os.path.dirname(os.path.abspath(__file__))
wpath = os.getcwd()

dirs = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]

def read(file):
  with open(file, "r") as source:
    return source.read()

case1, case2, case3, case4, case5, case6, case7, case8, case9 = ([] for i in range(9))

dirs.pop(0)

def not_contains_words(file):
  if "alltogether" not in file and "casual" not in file and "loc.csv" not in file and "_ccs.csv" not in file:
    return True
  return False

for dir in dirs:
  current_path = path + "/" + dir + "/*.csv"
  files = glob.glob(current_path)

  files = [fn for fn in glob.glob(current_path) if not_contains_words(fn)]

  for file in files:

      contribs = []
      for contrib in read(file).split(","):
        if contrib is not "":
          contrib = int(contrib)
          contribs.append(contrib)

      if len(contribs) <= 9:
        case1.append(len(contribs))
        print file
      elif len(contribs) > 9 and len(contribs) <= 49:
        case2.append(len(contribs))
      elif len(contribs) > 49 and len(contribs) <= 99:
        case3.append(len(contribs))
      elif len(contribs) > 99 and len(contribs) <= 249:
        case4.append(len(contribs))
      elif len(contribs) > 249 and len(contribs) <= 499:
        case5.append(len(contribs))
      elif len(contribs) > 499 and len(contribs) <= 999:
        case6.append(len(contribs))
      elif len(contribs) > 999 and len(contribs) <= 4999:
        case7.append(len(contribs))
      elif len(contribs) > 4999 and len(contribs) <= 9999:
        case8.append(len(contribs))
      elif len(contribs) > 9999:
        case9.append(len(contribs))


print "\n\n"

print len(case1), len(case1) * 100 / 275.
print len(case2), len(case2) * 100 / 275.
print len(case3), len(case3) * 100 / 275.
print len(case4), len(case4) * 100 / 275.
print len(case5), len(case5) * 100 / 275.
print len(case6), len(case6) * 100 / 275.
print len(case7), len(case7) * 100 / 275.
print len(case8), len(case8) * 100 / 275.
print len(case9), len(case9) * 100 / 275.

print "total: " + str(len(case1) + len(case2) + len(case3) + len(case4) + len(case5) + len(case6) + len(case7) + len(case8) + len(case9))
