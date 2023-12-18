from locust import HttpUser, TaskSet, EventHook
import uuid

class TrackedTests(object):
    def __init__(self):
        # Register an event hook for the request_sent event
        EventHook.register(self, "request_sent", self.add_tracked_headers)

    def add_tracked_headers(self, client, request):
        # Get the current task information
        task_name = client.task.current.name
        class_name = client.task.current.parent.name

        # Generate a unique invocation ID for each task
        invocation_id = str(uuid.uuid4())

        # Add the headers
        request.headers.update({
            "trackedtest.suite": class_name,
            "trackedtest.name": f"{class_name}#{task_name}",
            "trackedtest.invocation_id": invocation_id,
        })
