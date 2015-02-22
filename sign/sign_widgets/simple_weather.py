from sign.widgets.abstractwidget import AbstractWidget
class SimpleWeather(AbstractWidget):

    def get_template_fields(self):
        return {}
    
    def get_template_path(self):
        return "sign/widgets/simple_weather.html"