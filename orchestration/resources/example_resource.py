from dagster import resource

class ExampleResource:
    def get_message(self):
        return "Hello from ExampleResource!"

@resource
def example_resource():
    return ExampleResource()