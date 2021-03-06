from automation.models import Automator, AutomatorClass, DeciderClass, Decider, Controller, Task, TaskGroup

import json


class Processor(object):
    """
    The processor calls automators based on configuration of deciders defined in a controller
    """

    def run(self):
        AutomatorClass.update_classes()
        DeciderClass.update_classes()
        print("Running...")
        for controller in Controller.objects.all():
            if controller.is_complete():
                controller.automate()
            else:
                print("Skipped '{0}'. Please ensure it is configured properly.".format(controller.name))

    def call_automator(self, automator_id, method, params):
        automator = Automator.objects.get(id=automator_id)
        result = automator.do_operations('[{"method": "' + method + '", "params": ' + json.dumps(params) + '}]')

        if not (len(result) == 1 and result[0] == None):
            print(json.dumps(result))

    def run_task(self, task):
        try:
            t = Task.objects.get(id=task)
            t.do_operations()
            return
        except Exception:
            pass

        try:
            t = TaskGroup.objects.get(id=task)
            t.do_operations()
        except Exception:
            pass

    def call_decider(self, decider):
        d = Decider.objects.get(id=decider)
        print(json.dumps(d.decide()))
