from automation.models import AutomatorClass, Controller

class Processor:
    '''
    The processor calls automators based on configuration of deciders defined in a controller
    '''
    def run(self):
      AutomatorClass.update_classes()
      print("Running...")
      for controller in Controller.objects.all():
        controller.automate()
