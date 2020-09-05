

class FileUtil:

    # Return the contents of filename
    @staticmethod
    def getContents(fileName):
        file = open(fileName, mode='r')
        content = file.read()
        file.close()
        return content
