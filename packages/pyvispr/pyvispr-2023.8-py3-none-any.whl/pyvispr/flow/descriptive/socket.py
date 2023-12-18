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

from __future__ import annotations

import dataclasses as dtcl
from enum import Enum as enum_t
from typing import Any, Sequence

from str_to_obj.type.hint import any_hint_h


class assign_when_importing_t:
    pass


class value_not_set_t:
    pass


class invalid_value_with_issues_t:
    def __init__(self, issues: Sequence[str], /) -> None:
        """"""
        self.issues = issues


ASSIGN_WHEN_ACTIVATING = assign_when_importing_t()
VALUE_NOT_SET = value_not_set_t()


class assignment_e(enum_t):
    """
    full: link + interactive, user input.
    """

    link = 0
    full = 1


@dtcl.dataclass(slots=True, repr=False, eq=False)
class input_t:
    type: any_hint_h | str | assign_when_importing_t = ASSIGN_WHEN_ACTIVATING
    assignment: assignment_e = assignment_e.link
    default_value: Any = VALUE_NOT_SET

    @property
    def has_default(self) -> bool:
        """"""
        return self.default_value is not VALUE_NOT_SET
