def import_modules(package):
    import pkgutil
    import inspect
    import sys
    import importlib
    module_list = []
    prefix = package.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        module = importlib.import_module(modname)
        clsmembers = inspect.getmembers(sys.modules[modname], inspect.isclass)
        module_list.append((module, clsmembers))
    return module_list