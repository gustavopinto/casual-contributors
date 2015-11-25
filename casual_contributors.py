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


#pre_process()

def sample():
  commits = []

  langpath = path + "/survey/new_sample_casual_contributions.csv"
  with open(langpath, "r") as source:
    lines = [line.replace("\n", "") for line in source]
    for line in lines:
      cols = line.split(";")
      commits.append("http://github.com/" + cols[1] + "/" + cols[2] + "/commit/" + cols[5])

  with open(path + "/survey/new_sample_casual_contributions.csv", "wb") as sink:
    sink.write("\n".join(commits))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(path + "/survey/casual_contributions.csv", sep=";")
print len(df['adds'])
df = df[(df['adds'] == 1) & (df['dels'] == 1)]

print len(df['adds'])


sys.exit(0)


df = pd.read_csv(path + "/survey/sample_casual_contributions.csv", sep=";")

lines = []

print pd.unique(df['project'])

print round(df['adds'].mean(), 2)
print round(df['dels'].mean(), 2)
print round(df['files'].mean(), 2)


sys.exit(0)

for lang in langs:
  sample = df[df['lang'] == lang]

  lines.append("%s & %s & %s & %s & %s & %s \\\\" % (lang, len(pd.unique(sample['project'])), len(sample), round(sample['adds'].mean(), 2), round(sample['dels'].mean(), 2), round(sample['files'].mean(), 2)))


with open(path + "/table.txt", "wb") as sink:
  sink.write("\n".join(lines))


sys.exit(0)

def get_project(project, col):
  p = df[(df['project'] == project)]
  return p[col].median()

data = pd.DataFrame({"project": pd.unique(df['project']),
                     "adds": [get_project(p, 'adds') for p in pd.unique(df['project'])],
                     "dels": [get_project(p, 'dels') for p in pd.unique(df['project'])],
                     "files": [get_project(p, 'files') for p in pd.unique(df['project'])]
                     })

print data['dels'].mean()
print data['dels'].quantile(.75)
print data['dels'].std()
#print data['dels'].mean()
#print data['files'].mean()

def bar_chart(df, l, name):

    ax = df[['adds', 'dels']].plot(kind='bar', stacked=True, color=['#AFAFAF', '#1F1F1F'], legend=False, figsize=(8, 4))

    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0 + box.height , box.width, box.height])

    patches, labels = ax.get_legend_handles_labels()
    ax.legend(patches[::-1], ['Adds', 'Dels'][::-1], loc='upper left')
    ax.grid(False) # remove the dotted lines

    xticks = ax.get_xticks()
    ax2 = ax.twinx()
    ax.set_xticks(xticks)
    plt.xticks(rotation=0)

    ax2.plot(ax.get_xticks(), df[['files']], linewidth=4, linestyle=':', marker='o')
    ax2.legend(['Files'], loc='upper right')

    ax.set_ylim((0,  max(df[('adds')].values) + max(df[('dels')].values)  +2))
    ax2.set_ylim((0,  max(df[('files')].values) +2))


    ax.set_xticklabels(l, rotation=0, fontsize='medium')

    ax.set_ylabel("# Median of Adds/Dels")
    ax2.set_ylabel("# Median of Files Used")

    file = wpath + '/figs/' + name
    plt.savefig(file, format='eps')

    print "Done!"



bar_chart(data, range(1, 21), "ruby_casual_contributions.eps")

sys.exit(0)

print "& Adds & %s & %s & %s & \\\\" % (round(df['adds'].mean(), 2), df['adds'].median(), round(df['adds'].std(), 2))
print "& Dels & %s & %s & %s & \\\\" % (round(df['dels'].mean(), 2), df['dels'].median(), round(df['dels'].std(), 2))
print "& Files & %s & %s & %s & \\\\" % (round(df['files'].mean(), 2), df['files'].median(), round(df['files'].std(), 2))
