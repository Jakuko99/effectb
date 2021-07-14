from calendar import month_name

class Tools:
    def __init__(self):
        self.output = ""
    
    def formatDate(self, date):
        elements = date.split("-")
        return f"{elements[2]}. {month_name[int(elements[1])]} {elements[0]}"

    def shortenText(self, string, n): #return first n sentences from string
        first = string.find(".")
        for _ in range(n - 1):
            first = string.find(".", first+1)
        return f"{string[:first-len(string)]}."

    def tupleUnpack(self, tup):
        self.output = ""
        for item in tup:
            self.output += f"{item} "
        return self.output[:-1]
    
    def joinList(self, list):
        self.output = ""
        for item in list:
            self.output += f"{item}, "
        return self.output[:-2] #remove last ', '
    
    def partialJoin(self, list, n):
        self.output = ""
        i = 0
        for item in list:
            self.output += f"{item}, "
            i += 1
            if i >= n:
                break
        return self.output[:-2]

    def convertTime(self, runtime):
        time = int(runtime)
        mins = time % 60
        hours = int(time / 60)
        if hours >= 1:
            return f"{hours} h {mins} min"
        else:
            return f"{mins} min"