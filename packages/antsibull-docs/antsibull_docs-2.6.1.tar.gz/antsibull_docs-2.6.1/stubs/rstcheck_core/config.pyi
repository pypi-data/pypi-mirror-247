# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import enum

class ReportLevel(enum.Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    SEVERE = 4
    NONE = 5


class RstcheckConfig:
    def __init__(
        self,
        report_level: ReportLevel | None = ...,
        ignore_directives: list[str] | None = ...,
        ignore_roles: list[str] | None = ...,
        ignore_substitutions: list[str] | None = ...,
        ignore_languages: list[str] | None = ...,
    ): ...
