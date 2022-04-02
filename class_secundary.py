from PyQt5 import QtWidgets, QtCore, QtGui

class lineAmount(QtWidgets.QLineEdit):    
    last_text = ""
    def __init__(self, data=None):
        super(lineAmount, self).__init__(data)
        self.textChanged.connect(self.change_text_amount)

    def change_text_amount(self, text):
        try:
            if text != "":
                for char in text.replace(",", "").replace(".", ""):
                    int(char)
        except:
            self.blockSignals(True)
            self.setText(self.last_text)
            self.blockSignals(False)
            return None

        if len(text) == 1: text = "0.0"+text
        if len(text) == 2: text = "0." +text
        if len(text) >= 3:
            text = text.replace(",", "").replace(".", "")
            text = text[0:-2] + "." + text[-2:]
        try:
            new_text = "{:,.2f}".format(float(text)).replace(',','~').replace('.',',').replace('~','.')
            self.blockSignals(True)
            self.setText(new_text)
            self.blockSignals(False)
            self.last_text = new_text
        except:
            pass