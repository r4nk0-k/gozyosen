import csv
import os
CSV_FILE = "replaceTextList.csv"

class ReplaceText():
    def __init__(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        self.csvPath = dir + "/" + CSV_FILE

    def addReplaceText(self, beforeText, afterText):
        with open(self.csvPath, 'a+') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow([beforeText, afterText])

    def replace(self, text):
        if not os.path.isfile(self.csvPath):
            return text

        with open(self.csvPath, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                text = text.replace(row[0], row[1])

        return text
