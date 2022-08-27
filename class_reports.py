from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

class Reports:

    TEMPLATE = None
    DATA = {}

    def __init__(self, NAME_TEMPLATE, DATA):

        if not type(DATA) is dict:
            print("Error - ¡Data debe ser un diccionario!")
            return None
        self.DATA = DATA

        try:
            env = Environment(loader=FileSystemLoader('templates'))
            self.TEMPLATE = env.get_template(NAME_TEMPLATE)
        except TemplateNotFound as Err:
            print("Error - ¡Plantilla no encontrada! {}".format(Err))
            self.TEMPLATE = None
            return None

    def execute(self):
        try:
            HTML = self.TEMPLATE.render(self.DATA)
            with open('templates/html_temp_report.html', 'w') as f:
                f.write(HTML)
                f.close()
            return True
        except:
            return False
        