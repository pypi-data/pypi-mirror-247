from typing import Callable
import uuid

class TrackedTask:
    def __init__(self, weight: int):
        self.weight = weight

    def __call__(self, task_func: Callable) -> Callable:
        """
        Decorator that intercepts requests, injects headers, and sets task weight.

        Args:
            task_func: The decorated task function.
            weight: The desired weight for the task.

        Returns:
            The wrapped task function with modified behavior.
        """

        def wrapper(self, *args, **kwargs):
            # Set task weight for execution
            self.task.weight = self.weight

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

            # Iterate through and modify requests
            for request in self.client.request_iter():
                request.headers.update(headers)
                yield request

            # Execute the original task function
            task_func(self, *args, **kwargs)

        return wrapper