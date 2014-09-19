from collections import OrderedDict
import importlib
import pkgutil

# All brain functions are expected to have this suffix
BRAIN_FN_SUFFIX = '_brain_fn'


def unprefixed_name(fn):
    return fn.__name__[:-len(BRAIN_FN_SUFFIX)]


def _try_import_module(loader, module_name):
    try:
        return loader.find_module(module_name).load_module(module_name)
    except Exception as e:
        print 'Error loading module', module_name, 'while discovering brain_fns:', e.message


def discover_brains(brains_root='.'):
    ''' Finds brain functions (brain = a function with a name ending in "_brain_fn")
    in discovered modules.
    :param brains_root: root path passed to pkgutil.walk_packages to find packages
    :return: OrderedDict of {unprefixed_name: brain functions}, sorted by name
    '''
    modules = filter(None, [
        _try_import_module(loader, module_name)
        for loader, module_name, is_pkg
        in pkgutil.walk_packages(brains_root)
    ])

    brain_fns = [
        fn
        for module in modules
        for name, fn in module.__dict__.items()
        if callable(fn) and name.endswith(BRAIN_FN_SUFFIX)
    ]
    sorted_deduped_brains = sorted(set(brain_fns), key=unprefixed_name)

    brain_fn_lookups = OrderedDict([
        (unprefixed_name(fn), fn)
        for fn in sorted_deduped_brains
    ])

    return brain_fn_lookups


class BrainNotFound(Exception):
    pass


def get_brain(fn_name):
    all_brains = discover_brains()
    try:
        return all_brains[fn_name]
    except KeyError:
        raise BrainNotFound(
            'Couldn\'t find brain by unprefixed name "{}". Valid options are: {}'
            .format(fn_name, all_brains.keys())
        )


def reload_brain(brain_fn):
    ''' Reimport the module containing the function to reset the brain's state between matches.
    '''
    module = brain_fn.__module__
    name = brain_fn.__name__

    return getattr(reload(importlib.import_module(module)), name)
