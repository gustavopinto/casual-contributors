import os, random, sys, glob

path = os.path.dirname(os.path.abspath(__file__))
wpath = os.getcwd()

rows = []

langs = ["C", "C++", "Clojure", "CoffeeScript", "Erlang", "Go", "Haskell", "Java", "JavaScript", "Objective-C", "Perl", "PHP", "Python", "Ruby", "Scala", "TypeScript"]

def get_organization(lang, project):
  langpath = path + "/" + lang + ".csv"
  with open(langpath, "r") as lines:
    for line in lines:
      columns = line.split(",")
      current_project = columns[0]
      if current_project == project:
        return columns[1]


def pre_process():
  head = "lang,organization,project,commiter,email,sha,files,adds,dels,date"
  rows.insert(0, head)

  for lang in langs:
    projects = glob.glob(path + "/" + lang + "/*_ccs.csv")

    for project in projects:
      project_name = os.path.basename(project).split("_ccs.csv")[0]
      organization = get_organization(lang, project_name)

      with open(project, "r") as source:
        lines = [line.replace("\n", "") for line in source]
        for i in range(0,len(lines),2):
          try:

            commit = lines[i].split(",")
            sha = commit[0]
            name = commit[1]

            email = commit[2]
            date = commit[-1].split(" ")[0]

            changes = lines[i+1].strip().split(",")
            files = changes[0].split(" ")[0]
            adds = changes[1].split(" ")[1]
          except Exception as e:
            print project
            print lines[i-1]

            sys.exit(0)

          dels = changes[2].split(" ")[1] if len(changes) == 3 else 0

          line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (lang, organization, project_name, name, email, sha, files, adds, dels, date)
          rows.append(line)

    with open(path + "/survey/casual_contributions.csv", "wb") as sink:
      sink.write("\n".join(rows))


pre_process()
