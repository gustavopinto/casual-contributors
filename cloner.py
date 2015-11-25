import glob, os, git, shutil, sys

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
