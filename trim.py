# !python3

import re
import shutil
import os

def prompt_user_for_directory():
    print(os.getcwd())
    directory = input('Enter a directory \n')
    if directory == 'exit' or directory == 'quit':
        exit()
    else:
        goodPath = get_path(directory)

        if os.path.exists(goodPath) is not True:
            print('The entered value ' + goodPath + ' is not a valid absolute path.')
            prompt_user_for_directory()

        print_path_items(goodPath)
        pathIsGood = prompt_user_if_path_is_good()

        expressionString = ''
        if pathIsGood == 'y':
            expressionString = prompt_user_for_expression()
        if pathIsGood == 'n':
            prompt_user_for_directory()
        if pathIsGood == 'exit' or pathIsGood == 'quit':
            exit()

        if expressionString == 'exit' or expressionString == 'quit':
            exit()

        pathContents = os.listdir(goodPath)
        dictionary = trim_files__for_prompt(expressionString, pathContents)

        yesOrNo = prompt_user_to_trim(dictionary)
        if yesOrNo == 'y':
            trim_files_action(dictionary)
        if yesOrNo == 'exit' or yesOrNo == 'quit':
            exit()

        prompt_user_for_directory()

def get_path(directory):
    directory = os.path.abspath(directory)
    directoryChunks = directory.split('\\')
    directoryChunks.insert(1, '\\')
    goodPath = os.path.join(*directoryChunks)
    return goodPath

def print_path_items(path):
    os.chdir(path)
    print('Contents of ' + path + '\n\n')
    pathContents = os.listdir(path)
    for pathItem in pathContents:
        print(pathItem)
    print(os.getcwd())

def prompt_user_if_path_is_good():
    answer = input("Is this path ok?  Type y for yes, or n to adjust the path\n")
    return answer

def prompt_user_for_expression():
    remover_expression = input('What would you like to remove from each item? '
                               'Separate different items with commas.\n'
                               'Type -z to remove dots between words.\n'
                               'Type -t to make the the filename title case.\n'
                               'Type -d to remove dashes between words.\n')
    return remover_expression

def trim_files__for_prompt(remover_expression, pathContents):
    oldAndNewNameDictionary = {}

    expressionArguments = remover_expression.split(',')
    for item in pathContents:

        newName = ""

        for expression in expressionArguments:
            if expression == '-z':
                countOfPeriods = item.count('.') - 1
                if len(newName) == 0:
                    newName = item.replace('.', ' ', countOfPeriods)
                else:
                    newName = newName.replace('.', ' ', countOfPeriods)

            if expression == '-t':
                if len(newName) == 0:
                    newName = item.title()
                else:
                    newName = newName.title()

            if expression == '-d':
                countOfDashes = item.count('_') - 1
                if len(newName) == 0:
                    newName = item.replace('_', ' ', countOfDashes)
                else:
                    newName = newName.replace('_', ' ', countOfDashes)

            regex = re.compile(re.escape(expression))
            mo = regex.search(item)
            if mo:
                if len(newName) == 0:
                    newName = item.replace(mo.group(), '')
                else:
                    newName = newName.replace(mo.group(), '')

        newName = re.sub('\s+', ' ', newName)
        newName = re.sub('\s+[.]', '.', newName)
        newName = newName.lstrip()

        oldAndNewNameDictionary[item] = newName

    return oldAndNewNameDictionary

def prompt_user_to_trim(oldAndNewNameDictionary):
    print("The following changes will occur...")
    for key in oldAndNewNameDictionary.keys():
        print(key + " --> " + oldAndNewNameDictionary[key])
    answer = input("Press y to accept\n")
    return answer

def trim_files_action(oldAndNewNameDictionary):
    for key in oldAndNewNameDictionary.keys():
        if oldAndNewNameDictionary[key]:
            shutil.move(key, oldAndNewNameDictionary[key])

prompt_user_for_directory()