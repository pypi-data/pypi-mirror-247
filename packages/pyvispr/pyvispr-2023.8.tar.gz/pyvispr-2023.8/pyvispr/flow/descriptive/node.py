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

import ast as prsr
import dataclasses as dtcl
import importlib as mprt
import inspect as spct
import itertools as ittl
from enum import Enum as enum_t
from pathlib import Path as path_t
from types import EllipsisType
from types import ModuleType as module_t
from typing import Any, Callable

from conf_ini_g.phase.specification.parameter.type import type_t
from str_to_obj.type.hint import any_hint_h

from pyvispr.catalog.parser import N_A_F_A, NO_ANNOTATION, NO_OUTPUT_NAMES, NO_INPUT_NAME
from pyvispr.extension.module import ModuleForPath
from pyvispr.flow.descriptive.socket import (
    ASSIGN_WHEN_ACTIVATING,
    VALUE_NOT_SET,
    assign_when_importing_t,
    assignment_e,
    input_t,
)


class source_e(enum_t):
    not_set = 0
    local = 1
    referenced = 2
    system = 3


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t:
    path: str | path_t
    actual_path: str | path_t = ""
    name: str = ""
    keywords: str = ""
    short_description: str = ""
    long_description: str = ""
    source: source_e = source_e.not_set
    function_name: str | None = None
    inputs: dict[str, input_t] | None = None
    outputs: dict[str, any_hint_h | str | assign_when_importing_t | None] | None = None
    requires_completion: bool = False
    #
    module: module_t | None = None
    Function: Callable[..., Any] | None = None

    def __post_init__(self) -> None:
        """"""
        if self.name.__len__() > 0:
            return

        if isinstance(self.path, str):
            self.path = path_t(self.path)
        self.path = self.path.expanduser()
        with open(self.path) as accessor:
            tree = prsr.parse(accessor.read())
        first_function = None
        for node in prsr.walk(tree):
            if isinstance(node, prsr.FunctionDef) and (node.name[0] != "_"):
                first_function = node
                break
        if first_function is None:
            return

        first_function_inputs = first_function.args
        documentation = prsr.get_docstring(first_function)

        (
            self.name,
            actual,
            self.function_name,
            output_names,
            assignments,
        ) = N_A_F_A(documentation, first_function.name)
        if actual is None:
            self.source = source_e.local
            self.actual_path = self.path
        elif actual.endswith(".py"):
            self.source = source_e.referenced
            self.actual_path = path_t(actual)
        else:
            self.source = source_e.system
            self.actual_path = actual

        inputs = {}
        for arguments, defaults in (
            (
                first_function_inputs.posonlyargs,
                (),
            ),
            (first_function_inputs.args, first_function_inputs.defaults),
            (first_function_inputs.kwonlyargs, first_function_inputs.kw_defaults),
        ):
            for argument, default in ittl.zip_longest(
                arguments, defaults, fillvalue=VALUE_NOT_SET
            ):
                assignment = assignments.get(argument.arg, "link")
                assignment = assignment_e[assignment]

                if default is not VALUE_NOT_SET:
                    default = ASSIGN_WHEN_ACTIVATING

                inputs[argument.arg] = input_t(
                    assignment=assignment,
                    default_value=default,
                )
                if argument.arg == NO_INPUT_NAME:
                    self.requires_completion = True
        self.inputs = inputs

        if output_names is None:
            self.outputs = {}
        elif output_names == NO_OUTPUT_NAMES:
            self.outputs = {NO_OUTPUT_NAMES: None}
            self.requires_completion = True
        else:
            self.outputs = {_elm.strip(): None for _elm in output_names.split(",")}

    @property
    def n_inputs(self) -> int:
        """"""
        return self.inputs.__len__()

    @property
    def input_names(self) -> tuple[str, ...]:
        """"""
        return tuple(self.inputs.keys())

    @property
    def input_types(self) -> tuple[any_hint_h | str, ...]:
        """"""
        return tuple(_elm.type for _elm in self.inputs.values())

    @property
    def n_outputs(self) -> int:
        """"""
        return self.outputs.__len__()

    @property
    def output_names(self) -> tuple[str, ...]:
        """"""
        return tuple(self.outputs.keys())

    @property
    def output_types(self) -> tuple[any_hint_h | str, ...]:
        """"""
        return tuple(self.outputs.values())

    def Activate(self) -> None:
        """"""
        if self.module is not None:
            return

        if self.source is source_e.system:
            self.module, self.Function = _M_F_FromPyPath(self.actual_path)
        else:  # source_e.local or source_e.referenced
            self.module, self.Function = _M_F_FromPathAndName(
                self.actual_path, self.function_name
            )

        """
        If the actual function is a method wrapper (actual name is __call__),
        it does not support the call to signature. Instead, the function of
        the catalog module is used.
        """
        if self.actual_path != self.path:
            _, Function = _M_F_FromPathAndName(self.path, self.function_name)
            signature = spct.signature(Function)
        else:
            signature = spct.signature(self.Function)

        parameters = signature.parameters
        for name in self.inputs:
            parameter = parameters[name]
            if parameter.annotation == NO_ANNOTATION:
                annotation = Any
                self.requires_completion = True
            else:
                annotation = parameter.annotation
            self.inputs[name].type = type_t.NewFromTypeHint(annotation)
            if self.inputs[name].default_value is ASSIGN_WHEN_ACTIVATING:
                self.inputs[name] = parameter.default

        if self.outputs.__len__() > 0:
            if signature.return_annotation == NO_ANNOTATION:
                annotation = Any
                self.requires_completion = True
            else:
                annotation = signature.return_annotation
            hint = type_t.NewFromTypeHint(annotation)
            if (hint.type is tuple) and (
                (hint.elements.__len__() != 2) or (hint.elements[1] is not EllipsisType)
            ):
                hints = hint.elements
            else:
                hints = (hint,)
            assert hints.__len__() == self.outputs.__len__(), (
                self.name,
                hints,
                self.outputs,
            )
            for name, hint in zip(self.outputs, hints):
                self.outputs[name] = hint


def _M_F_FromPathAndName(path: str, function_name: str, /) -> tuple[module_t, Callable]:
    """"""
    # TODO: Add error management.
    module = ModuleForPath(path_t(path))
    Function = getattr(module, function_name)

    return module, Function


def _M_F_FromPyPath(py_path: str, /) -> tuple[module_t, Callable]:
    """"""
    # TODO: Add error management.
    last_dot_idx = py_path.rfind(".")
    module = mprt.import_module(py_path[:last_dot_idx])
    Function = getattr(module, py_path[(last_dot_idx + 1) :])

    return module, Function


# from inspect import getdoc as GetFunctionDoc
# from inspect import signature as GetFunctionSignature
# signature = GetFunctionSignature(function)
# documentation = GetFunctionDoc(function)
