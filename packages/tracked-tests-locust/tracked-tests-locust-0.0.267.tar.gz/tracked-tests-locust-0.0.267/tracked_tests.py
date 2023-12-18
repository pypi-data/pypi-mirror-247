import uuid
from functools import wraps
from locust import HttpUser, task

class TrackedTask:
    task_invocation_ids = {}

    @classmethod
    def add_tracked_headers(cls, client, class_name, task_name, invocation_id):
        headers = {
            'trackedtest.suite': class_name,
            'trackedtest.name': f"{class_name}#{task_name}",
            'test.type': 'locust',
            'trackedtest.invocation_id': invocation_id
        }
        client.headers.update(headers)

def tracked_task(task_weight=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            class_name = func.__qualname__.split('.')[0]
            user = args[0]
            if func.__name__ not in TrackedTask.task_invocation_ids:
                TrackedTask.task_invocation_ids[func.__name__] = str(uuid.uuid4())
            TrackedTask.add_tracked_headers(user.client, class_name, func.__name__, TrackedTask.task_invocation_ids[func.__name__])
            return func(*args, **kwargs)
        return task(weight=task_weight)(wrapper)
    return decorator
