from automation.models import Automator, AutomatorClass, DeciderClass, Decider, Controller

class Processor:
    '''
    The processor calls automators based on configuration of deciders defined in a controller
    '''
    def run(self):
      AutomatorClass.update_classes()
      DeciderClass.update_classes()
      print("Running...")
      for controller in Controller.objects.all():
        if controller.is_complete():
          controller.automate()
        else:
          print("Skipped '{0}'. Please ensure it is configured properly.".format(controller.name))

    def call_automator(self, automator, method, params):
      a = Automator.objects.get(name = automator)
      import json
      print(a.do_operations('[{"method": "' + method + '", "params": ' + json.dumps(params) + '}]'))

    def call_decider(self, decider):
      d = Decider.objects.get(name = decider)
      import json
      print(d.decide())