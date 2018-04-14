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


def get_module_models(module_list):
    from api.lib.templates import ModelTemplate
    module_models = {}
    for module in module_list:
        for member in module[1]:
            mname = member[0]
            if issubclass(member[1], ModelTemplate):
                module_models[mname] = member[1]
    return module_models