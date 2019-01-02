
AVAILABLE_TASKS = (
    "dns",
)

def setup():
    from importlib import import_module
    for task in AVAILABLE_TASKS:
        import_module(name=f".{task}", package=__name__)