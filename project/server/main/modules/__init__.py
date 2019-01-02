""" All Available Module on Server Belong to Here """

AVAILABLE_MODULES = (
    "api",
)

def init_app(app, **kwargs):
    from importlib import import_module
    for module in AVAILABLE_MODULES:
        import_module(
            f".{module}", 
            package=__name__
        ).init_app(app, **kwargs)