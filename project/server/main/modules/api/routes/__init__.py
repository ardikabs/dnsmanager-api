
ENABLED_ROUTES = (
    "records",
    "zones",
)

def setup(api):
    from importlib import import_module
    for namespace in sorted(ENABLED_ROUTES):
        api.add_namespace(
            import_module(
                f".{namespace}", 
                package=__name__
            ).api
        )
    api.namespaces.pop(0)

    return api