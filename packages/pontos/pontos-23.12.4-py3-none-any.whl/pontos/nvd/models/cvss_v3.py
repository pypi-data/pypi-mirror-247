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

from dataclasses import dataclass
from typing import Optional

from pontos.models import Model, StrEnum


class Severity(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AttackVector(StrEnum):
    NETWORK = "NETWORK"
    ADJACENT_NETWORK = "ADJACENT_NETWORK"
    LOCAL = "LOCAL"
    PHYSICAL = "PHYSICAL"


class ModifiedAttackVector(StrEnum):
    NETWORK = "NETWORK"
    ADJACENT_NETWORK = "ADJACENT_NETWORK"
    LOCAL = "LOCAL"
    PHYSICAL = "PHYSICAL"
    NOT_DEFINED = "NOT_DEFINED"


class AttackComplexity(StrEnum):
    HIGH = "HIGH"
    LOW = "LOW"


class ModifiedAttackComplexity(StrEnum):
    HIGH = "HIGH"
    LOW = "LOW"
    NOT_DEFINED = "NOT_DEFINED"


class PrivilegesRequired(StrEnum):
    HIGH = "HIGH"
    LOW = "LOW"
    NONE = "NONE"


class ModifiedPrivilegesRequired(StrEnum):
    HIGH = "HIGH"
    LOW = "LOW"
    NONE = "NONE"
    NOT_DEFINED = "NOT_DEFINED"


class UserInteraction(StrEnum):
    NONE = "NONE"
    REQUIRED = "REQUIRED"


class ModifiedUserInteraction(StrEnum):
    NONE = "NONE"
    REQUIRED = "REQUIRED"
    NOT_DEFINED = "NOT_DEFINED"


class Scope(StrEnum):
    UNCHANGED = "UNCHANGED"
    CHANGED = "CHANGED"


class ModifiedScope(StrEnum):
    UNCHANGED = "UNCHANGED"
    CHANGED = "CHANGED"
    NOT_DEFINED = "NOT_DEFINED"


class Impact(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    HIGH = "HIGH"


class ModifiedImpact(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    HIGH = "HIGH"
    NOT_DEFINED = "NOT_DEFINED"


class ExploitCodeMaturity(StrEnum):
    UNPROVEN = "UNPROVEN"
    PROOF_OF_CONCEPT = "PROOF_OF_CONCEPT"
    FUNCTIONAL = "FUNCTIONAL"
    HIGH = "HIGH"
    NOT_DEFINED = "NOT_DEFINED"


class RemediationLevel(StrEnum):
    OFFICIAL_FIX = "OFFICIAL_FIX"
    TEMPORARY_FIX = "TEMPORARY_FIX"
    WORKAROUND = "WORKAROUND"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_DEFINED = "NOT_DEFINED"


class Confidence(StrEnum):
    UNKNOWN = "UNKNOWN"
    REASONABLE = "REASONABLE"
    CONFIRMED = "CONFIRMED"
    NOT_DEFINED = "NOT_DEFINED"


class Requirement(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    NOT_DEFINED = "NOT_DEFINED"


@dataclass
class CVSSData(Model):
    version: str
    vector_string: str
    base_score: float
    base_severity: Severity
    attack_vector: Optional[AttackVector] = None
    attack_complexity: Optional[AttackComplexity] = None
    privileges_required: Optional[PrivilegesRequired] = None
    user_interaction: Optional[UserInteraction] = None
    scope: Optional[Scope] = None
    confidentiality_impact: Optional[Impact] = None
    integrity_impact: Optional[Impact] = None
    availability_impact: Optional[Impact] = None
    exploit_code_maturity: Optional[ExploitCodeMaturity] = None
    remediation_level: Optional[RemediationLevel] = None
    report_confidence: Optional[Confidence] = None
    temporal_score: Optional[float] = None
    temporal_severity: Optional[Severity] = None
    confidentiality_requirement: Optional[Requirement] = None
    integrity_requirement: Optional[Requirement] = None
    availability_requirement: Optional[Requirement] = None
    modified_attack_vector: Optional[ModifiedAttackVector] = None
    modified_attack_complexity: Optional[ModifiedAttackComplexity] = None
    modified_privileges_required: Optional[ModifiedPrivilegesRequired] = None
    modified_user_interaction: Optional[ModifiedUserInteraction] = None
    modified_scope: Optional[ModifiedScope] = None
    modified_confidentiality_impact: Optional[ModifiedImpact] = None
    modified_integrity_impact: Optional[ModifiedImpact] = None
    modified_availability_impact: Optional[ModifiedImpact] = None
    environmental_score: Optional[float] = None
    environmental_severity: Optional[Severity] = None
