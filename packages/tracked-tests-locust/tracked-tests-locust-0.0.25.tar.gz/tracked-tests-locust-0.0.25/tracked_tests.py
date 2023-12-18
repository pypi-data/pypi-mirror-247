import uuid
from locust import events
from locust.exception import StopLocust

class EnableTrackedTests:
    def __init__(self, environment):
        self.environment = environment
        self.task_data = {}

        # Adding the event hooks
        events.request.add_listener(self.on_request)
        events.test_start.add_listener(self.on_test_start)

    def on_test_start(self, **kwargs):
        self.task_data = {}

    def on_request(self, request_type, name, response_time, response_length, **kwargs):
        task = self.environment.runner.tasks.get(name)
        if task:
            class_name = task.__class__.__name__
            task_name = name
            invocation_id = self.get_invocation_id(task_name)
            
            trackedtest_name = f"{class_name}#{task_name}"
            trackedtest_suite = class_name

            self.task_data[name] = {
                'trackedtest.name': trackedtest_name,
                'trackedtest.suite': trackedtest_suite,
                'trackedtest.invocation_id': invocation_id
            }

            kwargs['headers'].update({
                'trackedtest.name': trackedtest_name,
                'trackedtest.suite': trackedtest_suite,
                'trackedtest.invocation_id': invocation_id
            })
        else:
            raise StopLocust(f"Task '{name}' not found in the Locust test")

    def get_invocation_id(self, task_name):
        if task_name in self.task_data:
            return self.task_data[task_name]['trackedtest.invocation_id']
        else:
            return str(uuid.uuid4())

    def __del__(self):
        events.request.remove_listener(self.on_request)
        events.test_start.remove_listener(self.on_test_start)
