import csv
CSV_FILE = "replaceTextList.csv"

class ReplaceText():
    def addReplaceText(self, beforeText, afterText):
        with open(CSV_FILE, 'w+') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow([beforeText, afterText])

    def replace(self, text):
        with open(CSV_FILE, 'r+') as f:
            reader = csv.reader(f)
            for row in reader:
                print row
                text = text.replace(row[0], row[1])

        return text
