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

    def call_automator(self, args):
      a = Automator.objects.get(name = args[0])
      import json
      print(a.do_operations('[{"method": "' + args[1] + '", "params": ' + json.dumps(args[2:]) + '}]'))

    def call_decider(self, args):
      d = Decider.objects.get(name = args[0])
      import json
      print(d.decide())