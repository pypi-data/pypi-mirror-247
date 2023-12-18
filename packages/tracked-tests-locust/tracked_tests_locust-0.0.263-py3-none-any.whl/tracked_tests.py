from locusto import Locust, HttpUser, task, BaseTask

class TrackedTask(BaseTask):
    def __init__(self):
        super().__init__()

    def __call__(self, func: Callable) -> Callable:
        super().__call__(func)

        def wrapper(self, *args, **kwargs):
            # Get task information for headers
            class_name = self.task.current.parent.name
            task_name = self.task.current.name

            # Generate unique invocation ID
            invocation_id = str(uuid.uuid4())

            # Build tracked header values
            headers = {
                "trackedtest.suite": class_name,
                "trackedtest.name": f"{class_name}#{task_name}",
                "trackedtest.invocation_id": invocation_id,
                "test.type": "locust",
            }

            # Access and utilize task weight from Locust internals
            weight = self.task.weight

            # Use weight information within headers or task logic as needed
            # ... (your logic based on weight)

            # Iterate through and modify all requests in the task
            for request in self.client.request_iter():
                request.headers.update(headers)
                yield request

            # Execute the original task function
            func(self, *args, **kwargs)

        return wrapper