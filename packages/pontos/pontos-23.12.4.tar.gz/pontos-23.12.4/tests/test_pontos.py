# -*- coding: utf-8 -*-
# Copyright (C) 2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch

from pontos import main
from pontos.version import __version__


class TestPontos(unittest.TestCase):
    @patch("pontos.pontos.RichTerminal")
    def test_pontos(self, terminal_mock):
        main()

        terminal_mock.return_value.print.assert_called()
        terminal_mock.return_value.indent.assert_called()
        terminal_mock.return_value.bold_info.assert_called()
        terminal_mock.return_value.info.assert_called()
        terminal_mock.return_value.warning.assert_called_once_with(
            'Use the listed commands "help" for more information '
            "and arguments description."
        )

    @patch("pontos.pontos.RichTerminal")
    @patch("sys.argv", ["pontos", "--version"])
    def test_pontos_version(self, terminal_mock):
        main()

        terminal_mock.return_value.print.assert_called_once_with(
            f"pontos version {__version__}"
        )
