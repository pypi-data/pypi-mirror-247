import importlib.util


def validate_converter(path: str):
    spec = importlib.util.spec_from_file_location("converter", location=path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    try:
        foo.TritonPythonModel.execute()
    except AttributeError:
        raise AttributeError("convert function must be defined in converter script")
    except Exception:
        pass
