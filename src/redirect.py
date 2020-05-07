class Redirect:
    content = ""

    def write(self,str):
        self.content += str
    def flush(self):
        self.content = ""


redirect = Redirect()