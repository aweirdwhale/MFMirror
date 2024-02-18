import os, fnmatch

# This function will find and replace strings in a given directory for a given file pattern
def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)): # os.walk() generates the file names in a directory tree by walking the tree either top-down or bottom-up
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

findReplace("src/", ".env.secret", ".env.key", "*.py")