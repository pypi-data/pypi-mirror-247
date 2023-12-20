class getList:
    def __init__(self, file_path, alphanumeric = False):
        self.file_path = file_path
        self.alphanumeric = alphanumeric
        self.wordCount = []
        self.wordList = []

        with open(self.file_path, 'r') as infile:
            infile_sorted = sorted(set(infile.read().split()))
            if alphanumeric == True:
                cleaned_strings = ["".join(char for char in s if char.isalnum()) for s in infile_sorted]
            else:
                cleaned_strings = ["".join(char for char in s if char.isalpha()) for s in infile_sorted]
            infile_cleaned = [i.lower() for i in cleaned_strings]
            for i in infile_cleaned:
                # because of the above method sometimes blank strings will appear
                if i != '':
                    if i not in self.wordList:
                        self.wordList.append(i)
            self.wordCount = len(self.wordList)
