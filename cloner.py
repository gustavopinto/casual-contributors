import glob, os, git, shutil, sys


def edit_distance(s1, s2):
  m=len(s1)+1
  n=len(s2)+1

  tbl = {}
  for i in range(m): tbl[i,0]=i
  for j in range(n): tbl[0,j]=j
  for i in range(1, m):
    for j in range(1, n):
      cost = 0 if s1[i-1] == s2[j-1] else 1
      tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

  return tbl[i,j]

print(edit_distance("Helloworld", "ElloWorld"))

sys.exit(0)

files = glob.glob("*.csv")

for file in files:
  print "\nLanguage: " + file

  path = file.split(".")[0]
  if not os.path.isdir(path):
    os.makedirs(path)

  lines = open(file).readlines()
  for line in lines[1:]:
    columns = line.split(",")

    url = "https://github.com/%s/%s.git" % (columns[1], columns[0])

    try:
      git.Git().clone(url, path + "/" + columns[0])
    except git.exc.GitCommandError:
      pass

    print "Done with %s" % url
