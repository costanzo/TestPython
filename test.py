from subprocess import call,Popen
import os
from subprocess import STDOUT,PIPE

root_path = 'f:\\python\\projecttest'
class_name = 'TicTacToe'
javac_cmd = "javac"
java_cmd = "java"
delete_cmd = 'del'
openfile_cmd = 'notepad'


def getAllTestFilePath(root_path):
    src = []
    filename = []
    for files in os.listdir(root_path):
        if files.endswith('.txt'):
            filename.append(files)
            p = os.path.join(root_path, files)
            src.append(p)
    return src, filename

def getAllTestData(test_filepaths):
    testdata = []
    for testfile in test_filepaths:
        with open(testfile, 'rb') as f:
            testdata.append(f.read())
    return testdata

users = []
source_classpath = []

# open the file in the terminal
def openFile(path):
    Popen([openfile_cmd,path])

# get all usersnames that will be tested
def getUsers(root_path):
    users = []
    for files in next(os.walk(root_path))[1]:
        users.append(files)
    return users

# get the file path separately for every user
def getSourcePath(root_path, users):
    source_classpath = []
    for user in users:
        path = os.path.join(root_path, user)
        source_classpath.append(path)
    return source_classpath

# compile every single java file
def compileFiles(class_path, src):
    path = os.path.join(class_path, src)
    return Popen([javac_cmd,'-cp', class_path, path])

# delete other files
def deleteFiles(path, name):
    delpath = os.path.join(path, name)
    os.remove(delpath)

# get all the java files for compiling
def getAllSourceFiles(path):
    src = []
    for files in os.listdir(path):
        if files.endswith('.java'):
            src.append(files)
        else:
            deleteFiles(path, files)
    return src

# compile the whole project for certain user
def compileProject(path):
    srcs = getAllSourceFiles(path)
    pros = []
    for src in srcs:
        p = compileFiles(path, src)
        pros.append(p)
    [p.wait() for p in pros]

def compileAllProjects(root_path):
    print('-------- compiling --------')
    users = getUsers(root_path)
    users_filepaths = getSourcePath(root_path, users)
    for x in range(len(users)):
        compileProject(users_filepaths[x])
        print(users[x] + ' files compiled successful!')
    return users, users_filepaths

# the output directory path
def executeFiles(user, path, inputdata, outputfile):
    global class_name
    global input_data
    for x in range(len(inputdata)):
        output_path = path
        output_filepath = os.path.join(output_path, user)
        output_filepath += '_' + outputfile[x]
        p = Popen([java_cmd,'-cp',path,class_name], stdin=PIPE, stdout = PIPE, stderr=STDOUT)
        stdout = p.communicate(inputdata[x])[0]
        with open(output_filepath, 'wb') as f:
            f.write(stdout)
        print(user + ' test files' + outputfile[x] + ' execute successful!')
    #openFile(output_filepath)

# execute all projects, input is user name list and path list
def executeAllProjects(users, paths):
    print('-------- executing --------')
    testlist, filenames = getAllTestFilePath(root_path)
    testData =  getAllTestData(testlist)
    for x in range(len(users)):
        executeFiles(users[x], paths[x], testData, filenames)

def getTxtFilePaths(users, paths, filename):
    txtFilePaths = []
    for x in range(len(users)):
        output_filepath = os.path.join(paths[x], users[x])
        output_filepath += '_' + filename
        txtFilePaths.append(output_filepath)
    return txtFilePaths

 # open all files ready for reading
def openAllFiles(txtFilePaths):
    files = []
    for filepath in txtFilePaths:
        files.append(open(filepath, 'r'))
    return files

def closeAllFiles(txtFilePaths):
    for filepath in txtFilePaths:
        filepath.close()

# compare all the input lines, they should be the same
def compareLine(lines):
    for x in range(len(lines)):
        if x == 0:
            continue
        else:
            print(lines[0].strip('\n'))
            if lines[x] != lines[0]:
                return False
    return True

# compare all lines in each document
def compareAllLines(filelist):
    continueFlag = True
    count = 0
    while continueFlag:
        lines = []
        for files in filelist:
            line = files.readline()
            if not line:
                continueFlag = False
                break
            else:
                lines.append(line)
        result = compareLine(lines)
        count = count + 1
        if result == False:
            return False, count
    return True, count

def compareOneTestFile(users, paths, filename):
    txtFilepaths = getTxtFilePaths(users, paths, filename)
    filelist = openAllFiles(txtFilepaths)
    result, lineNum = compareAllLines(filelist)
    closeAllFiles(filelist)
    print('---------------------------------------')
    if result == True:
        print('You get the same outputs in ' + filename)
    else:
        print('Something is wrong in ' + filename + ' line ' + str(lineNum))
    print('---------------------------------------')

# compare all output files
def compareAllFiles(users, paths):
    print('--------comparing--------')
    testlist, filenames = getAllTestFilePath(root_path)
    for filename in filenames:
        compareOneTestFile(users, paths, filename)

if __name__ == '__main__':
    users, paths = compileAllProjects(root_path)
    executeAllProjects(users, paths)
    compareAllFiles(users, paths)
