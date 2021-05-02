def readText(filename):
    with open(filename,"r",encoding='utf-8') as file:

        return str(file.read())
def writeText(filepath,content):
    with open(filepath,"w",encoding='utf-8') as file:
        file.write(content)
    return "DONE"