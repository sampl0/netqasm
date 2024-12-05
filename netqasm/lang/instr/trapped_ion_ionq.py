from dataclasses import dataclass
from typing import List, Union

import numpy as np

from netqasm.lang.operand import Immediate, Operand, Register, Template
from netqasm.util.quantum_gates import get_rotation_matrix

from . import base, core

@dataclass
class AllQubitsInitInstruction(base.NoOperandInstruction):
    id: int = 42
    mnemonic: str = "init_all"

@dataclass
class AllQubitsMeasInstruction(base.RegAddrInstruction):
    id: int = 43
    mnemonic: str = "meas_all"

@dataclass
class GPiInstruction(core.RotationInstruction):
    mnemonic: str = "gpi"

@dataclass
class GPiInstruction2(core.RotationInstruction):
    mnemonic: str = "gpi2"

@dataclass
class VirtualZInstruction(core.RotationInstruction):
    mnemonic: str = "virt_z"

    def to_matrix(self) -> np.ndarray:
        axis = [0, 0, 1]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)

# Maybe this should be Imm4 to specify num and denom...
@dataclass
class MSInstruction(base.RegRegImmImmInstruction):
    mnemonic: str = "ms"

# TODO
# This class will require the implementation of RegRegImm3Instruction
@dataclass
class PartialMSInstruction(base.RegRegImmImmInstruction):
    mnemonic: str = "ms_p"

@dataclass
class ZZInstruction(base.RegRegImmInstruction):
    mnemonic: str = "zz"