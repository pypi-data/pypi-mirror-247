# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import importlib as mprt
import inspect as spct
import re as regx
import typing as h
from types import ModuleType as module_t

import docstring_parser as dcst

from pyvispr.catalog.constants import (
    ACTUAL_SOURCE,
    FUNCTION_NAME,
    NODE_NAME,
    OUTPUT_NAMES,
)
from pyvispr.config.main import CATALOG_FOLDER
from pyvispr.extension.string_ import SplitAndStriped

signature_t = spct.Signature
parameter_t = spct.Parameter

parameter_h = tuple[str, str]
parameter_w_default_h = tuple[str, str, h.Any]
parameters_h = list[parameter_h | parameter_w_default_h]
returns_h = list[parameter_h]
documentation_h = tuple[str, str, parameters_h, returns_h]


UNSPECIFIED_INPUT_KIND = (parameter_t.VAR_POSITIONAL, parameter_t.VAR_KEYWORD)
NO_ANNOTATION = "NO_ANNOTATION"
NO_INPUT_NAME = "NO_INPUT_NAME"
NO_OUTPUT_NAMES = "NO_OUTPUT_NAMES"


def InstallModuleFunctions(module_name: str, /, *, recursively: bool = False) -> None:
    """"""
    functions = AllFunctions(module_name, recursively=recursively)
    for function in functions:
        if function is None:
            # Wrapper methods are replaced with None in _FunctionHeader.
            continue

        full_name, header = function
        node_name = full_name.replace(".", " ").title().replace(" ", "")

        as_str = f'''
{header}
    """
    {NODE_NAME}: {node_name}
    {ACTUAL_SOURCE}: {full_name}
    {OUTPUT_NAMES}: {NO_OUTPUT_NAMES}
    """
    pass
'''
        where = CATALOG_FOLDER
        for piece in full_name.split("."):
            where /= piece
        where = where.with_suffix(".py")

        where.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with open(where, "w") as accessor:
            accessor.write(as_str[1:])


def AllFunctions(
    module_name: str, /, *, recursively: bool = False
) -> tuple[tuple[str, str] | None, ...]:
    """"""
    module = mprt.import_module(module_name)
    if recursively:
        output = []
        modules = []
        _AllFunctionsRecursively(f"{module_name}.", module, modules, output)
    else:
        output = _AllFunctions(module_name, module)
        if output.__len__() == 0:
            modules = []
            _AllFunctionsRecursively(f"{module_name}.", module, modules, output)

    return tuple(output)


def _AllFunctions(
    module_name: str, module: module_t, /
) -> list[tuple[str, str] | None]:
    """"""
    output = []

    for name in dir(module):
        if name[0] == "_":
            continue

        element = getattr(module, name)
        if (is_function := spct.isfunction(element)) or hasattr(element, "__call__"):
            if is_function:
                function = element
            else:
                function = element.__call__
            node_name = f"{module_name}.{name}"
            output.append((node_name, _FunctionHeader(name, function)))

    return output


def _AllFunctionsRecursively(
    prefix: str,
    module: module_t,
    modules: list[module_t],
    output: list[tuple[str, str] | None],
    /,
) -> None:
    """"""
    modules.append(module)

    OnlyModulesOrFunctions = lambda _arg: spct.ismodule(_arg) or spct.isfunction(_arg)
    for name, element in spct.getmembers(module, OnlyModulesOrFunctions):
        # Explicitly defined: spct.getmodule(function) == module
        if name[0] == "_":
            continue

        if spct.ismodule(element):
            if element not in modules:
                _AllFunctionsRecursively(prefix, element, modules, output)
        elif module.__name__.startswith(prefix):
            node_name = f"{module.__name__}.{name}"
            output.append((node_name, _FunctionHeader(name, element)))


def _FunctionHeader(function_name: str, function, /) -> str:
    """"""
    if not spct.isfunction(function):
        return f'def {function_name}({NO_INPUT_NAME}_0: "{NO_ANNOTATION}") -> "{NO_ANNOTATION}":'

    # TODO: Deal with comments.
    code = tuple(_elm.strip() for _elm in spct.getsource(function).splitlines())

    start = 0
    while not code[start].startswith("def "):
        start += 1

    n_opening = code[start].count("(")
    n_closing = code[start].count(")")
    end = start
    while n_opening > n_closing:
        end += 1
        n_opening += code[end].count("(")
        n_closing += code[end].count(")")

    last_closing = code[end].rindex(")")
    first_colon = code[end].find(":", last_closing)
    if first_colon < 0:
        end += 1
        while (first_colon := code[end].find(":")) < 0:
            end += 1
    last_line = code[end][: (first_colon + 1)]
    header = "".join(code[start:end])
    header += last_line

    signature = spct.signature(function)

    for i_idx, (name, description) in enumerate(signature.parameters.items()):
        if description.kind in UNSPECIFIED_INPUT_KIND:
            if description.kind is parameter_t.VAR_POSITIONAL:
                prefix = r"\*"
            else:
                prefix = r"\*\*"
            header = regx.sub(
                prefix + r"\b" + name + r"\b",
                f'{NO_INPUT_NAME}_{i_idx}: "{NO_ANNOTATION}"',
                header,
                count=1,
            )
        elif description.annotation is parameter_t.empty:
            header = regx.sub(
                r"\b" + name + r"\b", f'{name}: "{NO_ANNOTATION}"', header, count=1
            )

    if signature.return_annotation is signature_t.empty:
        header = f'{header[:-1]} -> "{NO_ANNOTATION}":'

    if "__call__" in header:
        header = regx.sub(r"\b__call__\b", function_name, header, count=1)

    return header


def _ParsedDocumentation(documentation: str, /) -> documentation_h:
    """"""
    parsed = dcst.parse(documentation)

    inputs = []
    for input_ in parsed.params:
        description = (input_.arg_name, input_.type_name)
        if input_.is_optional:
            description += (input_.default,)
        inputs.append(description)

    outputs = []
    for output in parsed.many_returns:
        outputs.append((output.return_name, output.type_name))

    return parsed.short_description, parsed.long_description, inputs, outputs


def N_A_F_A(
    documentation: str, function_name: str, /
) -> tuple[str, str | None, str, str | None, dict[str, str]]:
    """
    Returned "description" on last position should be interpreted as assignment types of the inputs.
    """
    description = documentation.strip().splitlines()
    description = dict(SplitAndStriped(_lne, ":") for _lne in description)

    function_name = description.get(FUNCTION_NAME, function_name)
    node_name = description.get(NODE_NAME, function_name)

    return (
        node_name,
        description.get(ACTUAL_SOURCE),
        function_name,
        description.get(OUTPUT_NAMES),
        description,
    )


if __name__ == "__main__":
    #
    MODULE = "numpy"
    InstallModuleFunctions(MODULE)
