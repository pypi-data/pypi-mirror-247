import uuid
from locust import task, events

def add_tracked_headers(client, class_name, task_name, invocation_id):
    headers = {
        'trackedtest.suite': class_name,
        'trackedtest.name': f"{class_name}#{task_name}",
        'test.type': 'locust',
        'trackedtest.invocation_id': invocation_id
    }
    client.headers.update(headers)

def tracked_task(task_weight=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            class_name = func.__qualname__.split('.')[0]
            invocation_id = str(uuid.uuid4())
            args[0].request_meta['invocation_id'] = invocation_id
            add_tracked_headers(args[0].client, class_name, func.__name__, invocation_id)
            return func(*args, **kwargs)
        return task(weight=task_weight)(wrapper)
    return decorator
