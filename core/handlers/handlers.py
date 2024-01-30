import importlib
import pkgutil


def setup_handlers(router):
    package_name = 'core.handlers'
    
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package_name + '.'):
        module = importlib.import_module(module_name)
        if hasattr(module, 'setup_handler'):
            module.setup_handler(router)
