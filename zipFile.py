import os, re
from shutil import copy
import json
import pandas as pd

MAX_FOLDER_SIZE = 400*1024*1024
MAX_FILE_SIZE = 4*1024*1024

# ############## change below for non testing ################################
DOCUMENT_ROOT_PATH = "C:\\Users\\jerry lu\\Downloads\\ClientDocs"
# DOCUMENT_ROOT_PATH = "C:\\Users\\jerry lu\\Downloads\\test"
##############################################################################

ZIP_SAVE_PATH = "C:\\Users\\jerry lu\\Desktop\\ZIP"
OVERSIZE_SAVE_PATH = "C:\\Users\\jerry lu\\Desktop\\Oversize"
FILE_INDEX = "fileindex.txt"
JSON_FILE = 'clients_exported.json'
MAX_STRING_LENGTH = 70

def parseJsonToIntArr():
    file = open('clients_exported.json')
    json_arr = json.load(file)
    num_arr = list(map(int, json_arr))
    num_arr.sort()
    return num_arr

def read_client_ids():
    df = pd.read_excel ('test_client_ids.xlsx') # csv qill not work if we are trying to read by column name. Use .xlsx for now
	# Returns an array of client IDs
    return df['ClientID']

# counts FileSize in src path given, ignores 
def countFileSize(src):
    documents = os.listdir(src)
    documents.sort()
    totalSize = 0
    # print(documents) if totalSize > 0 else print("empty folder")
    for doc in documents:
        docPath = os.path.join(src, doc)
        if os.path.isfile(docPath):
            if not MAX_FILE_SIZE <= os.path.getsize(docPath):  
                totalSize += os.path.getsize(docPath)
    return totalSize

def writeToTooLong(filePath):
    f = open("fileLength.txt", "a+")
    f.write(filePath+"\n")
    f.close()

# copies from src to dest and appends fileID to name of src file
def copyFileToDest(src, dest, fileID, docName):

    if len(docName) >= MAX_STRING_LENGTH:
        # log file name
        writeToTooLong(str(fileID) + ". " +str(docName))
        ###### change name of file ######
        factor = len(docName) - MAX_STRING_LENGTH + 15
        # build search regex
        regex = r".{" + re.escape(str(factor)) + r"}\."
        # replace the {x}. with just . alone
        docName = re.sub(regex, '.', docName)
        print(docName)
    
    appendNum = 0
    while (os.path.isfile(os.path.join(dest, str(fileID) + "." + docName))):
        appendNum += 1
        docName = re.sub(r'([0-9]*)\.', str(appendNum) + ".", docName)
        print(docName)

    finalDest = os.path.join(dest, str(fileID) + "." + docName)
    copy(src, finalDest)

# makes a new file in root directory with specified name
def create_folder(root, name):
    dstPath = os.path.join(root, str(name))
    # print(dstPath)
    try:
        os.mkdir(dstPath)
    except OSError:
        print("Creation of the directory %s failed" % dstPath)
        raise OSError
    else:
        print ("Sucessfully created directory %s" % dstPath)
        return dstPath

def writeToIndex(num):
    f = open(FILE_INDEX, "a+")
    f.write(num)
    f.close()

def getIndexNum():
    f = open(FILE_INDEX, "r")
    lines = f.readlines()
    if (len(lines) > 0):
        return int(lines[-1])
    else:
        return 1

def runCopyFile(src, folderID, ID):
    dest = os.path.join(ZIP_SAVE_PATH, str(folderID))
    DestSize = countFileSize(dest)
    DocumentsSize = countFileSize(src)
    # if destSize and document is larger than Max_file_Size, make new folder
    if DestSize + DocumentsSize >= MAX_FOLDER_SIZE:
        folderID += 1
        dest = create_folder(ZIP_SAVE_PATH, folderID)

    Documents = os.listdir(src)
    Documents.sort()
    for document in Documents:
        docPath = os.path.join(src, document)

        if os.path.getsize(docPath) >= MAX_FILE_SIZE:
            print("too big, moving {0} to oversized".format(docPath))
            copyFileToDest(docPath, OVERSIZE_SAVE_PATH, ID, document)
        else:
            print("copying {0} to {1}".format(docPath, dest))
            copyFileToDest(docPath, dest, ID, document)

    return folderID

if __name__ == '__main__':
    # FIND NUM FOLDER TO KNOW WHICH FOLDER TO SAVE TO
    numFolderSave = len(os.listdir(ZIP_SAVE_PATH))
    # print(numFolderSave)

    if numFolderSave == 0:
        create_folder(ZIP_SAVE_PATH, 1)
        numFolderSave = 1
    
    # print(index)
    ######################################## change below for non testing #################################
    # documentIDs = parseJsonToIntArr()

    # documentIDs = [1]
    # print(documentIDs)

    documentIDs = read_client_ids()    
    ########################################################################################################
    for documentID in documentIDs:
        if getIndexNum() > int(documentID): continue
        DocumentFolderSrc = os.path.join(DOCUMENT_ROOT_PATH, str(documentID))
        # print(DocumentPath)
        numFolderSave = runCopyFile(DocumentFolderSrc, numFolderSave, documentID)
        writeToIndex(str(documentID)+"\n")


    # sizeFile=countFileSize("testOS/")
    # print(sizeFile/(1024*1024))
    # copyFileToDest("a.txt", "testOS", "4")
