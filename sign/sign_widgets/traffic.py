from sign.widgets.abstractwidget import AbstractWidget
class Traffic(AbstractWidget):

    def get_template_fields(self):
        return {}
    
    def get_template_path(self):
        return "sign/widgets/traffic.html"
