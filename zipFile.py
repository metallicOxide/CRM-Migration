import os
from shutil import copy

MAX_FOLDER_SIZE = 400*1024*1024
MAX_FILE_SIZE = 4*1024*1024
DOCUMENT_ROOT_PATH = "C:\\Users\\usr\\Downloads\\ClientDocs"
ZIP_SAVE_PATH = "C:\\Users\\usr\\Desktop\\ZIP"
OVERSIZE_SAVE_PATH = "C:\\Users\\usr\\Desktop\\Oversize"
FILE_INDEX = "fileindex.txt"

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

# copies from src to dest and appends fileID to name of src file
def copyFileToDest(src, dest, fileID, docName):
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
    documentIDs = os.listdir(DOCUMENT_ROOT_PATH)
    documentIDs = list(map(int, documentIDs))
    documentIDs.sort()
    print(documentIDs)
    for documentID in documentIDs:
        if getIndexNum() > int(documentID): continue
        DocumentFolderSrc = os.path.join(DOCUMENT_ROOT_PATH, str(documentID))
        # print(DocumentPath)
        numFolderSave = runCopyFile(DocumentFolderSrc, numFolderSave, documentID)
        writeToIndex(str(documentID)+"\n")


    # sizeFile=countFileSize("testOS/")
    # print(sizeFile/(1024*1024))
    # copyFileToDest("a.txt", "testOS", "4")
