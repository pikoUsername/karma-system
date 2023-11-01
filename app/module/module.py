from typing import Any, Callable
import inspect


def filter_workflow(params: list[str], workflow: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in workflow.items()
            if key in params}


class ModuleLoader:
    def __init__(self, modules: list[Callable[..., None]], workflow_data: dict[str, Any]):
        self.modules = modules
        self.workflow_data = workflow_data

    def load(self):
        for module in self.modules:
            sig = inspect.signature(module)

            partial_data = filter_workflow(list(sig.parameters.keys()), self.workflow_data)
            module(**partial_data)


def configure_module_loader(workflow_data: dict[str, Any]) -> ModuleLoader:
    module = ModuleLoader(modules=[], workflow_data=workflow_data)

    return module
