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
class RotXInstruction(core.RotationInstruction):
    id: int = 44 
    mnemonic: str = "rot_x"

    def to_matrix(self) -> np.ndarray:
        axis = [1, 0, 0]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)


@dataclass
class RotYInstruction(core.RotationInstruction):
    id: int = 45
    mnemonic: str = "rot_y"

    def to_matrix(self) -> np.ndarray:
        axis = [0, 1, 0]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)


@dataclass
class RotZInstruction(core.RotationInstruction):
    id: int = 46
    mnemonic: str = "rot_z"

    def to_matrix(self) -> np.ndarray:
        axis = [0, 0, 1]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)

# AKA XX(x) as described in https://arxiv.org/pdf/1603.07678
@dataclass
class MSInstruction(base.RegRegImmImmInstruction):
    id: int = 47
    mnemonic: str = "ms"
    
    @property
    def qreg0(self):
        return self.reg0

    @qreg0.setter
    def qreg0(self, new_val: Register):
        self.reg0 = new_val

    @property
    def qreg1(self):
        return self.reg1

    @qreg1.setter
    def qreg1(self, new_val: Register):
        self.reg1 = new_val

    @property
    def angle_num(self):
        return self.imm0

    @angle_num.setter
    def angle_num(self, new_val: Immediate):
        self.imm0 = new_val

    @property
    def angle_denom(self):
        return self.imm1

    @angle_num.setter
    def angle_denom(self, new_val: Immediate):
        self.imm1 = new_val

    def to_matrix(self) -> np.ndarray:
        angle = self.angle_num * np.pi / 2**self.angle_denom
        cos_term = np.cos(angle)
        sin_term = -1j*np.sin(angle)
        return np.array([
            [cos_term,0,0,sin_term],
            [0,cos_term,sin_term,0],
            [0,sin_term,cos_term,0],
            [sin_term,0,0,cos_term]
        ])

# @dataclass
# class GPiInstruction(core.RotationInstruction):
#     mnemonic: str = "gpi"

#     # [[0 , e^{-i \phi}],
#     #  [e^{i \phi} , 0]]
#     def to_matrix(self) -> np.ndarray:
#         angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
#         exp_plus = np.exp(1j*angle)
#         exp_minus = np.exp(-1j*angle)
#         return np.array([
#             [0, exp_minus],
#             [exp_plus,0]
#         ])

# @dataclass
# class GPiInstruction2(core.RotationInstruction):
#     mnemonic: str = "gpi2"
   
#     # 1/sqrt(2) * [[1 , -i e^{-i \phi}],
#     #              [-i e^{i \phi} , 1]]
#     def to_matrix(self):
#         angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
#         exp_plus = -1j*np.exp(1j*angle)
#         exp_minus = -1j*np.exp(-1j*angle)

#         return np.sqrt(1/2) * np.array([
#             [1, exp_minus],
#             [exp_plus,1]
#         ])
                               
# @dataclass
# class VirtualZInstruction(core.RotationInstruction):
#     mnemonic: str = "virt_z"

#     def to_matrix(self) -> np.ndarray:
#         axis = [0, 0, 1]
#         angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
#         return get_rotation_matrix(axis, angle)

# @dataclass
# class MSInstruction(base.RegRegImm4Instruction):
#     id: int = 47
#     mnemonic: str = "ms"
    
#     @property
#     def qreg0(self):
#         return self.reg0

#     @qreg0.setter
#     def qreg0(self, new_val: Register):
#         self.reg0 = new_val

#     @property
#     def qreg1(self):
#         return self.reg1

#     @qreg1.setter
#     def qreg1(self, new_val: Register):
#         self.reg1 = new_val
    
#     @property
#     def angle_num0(self):
#         return self.imm0

#     @angle_num0.setter
#     def angle_num0(self, new_val: Immediate):
#         self.imm0 = new_val

#     @property
#     def angle_denom0(self):
#         return self.imm1

#     @angle_denom0.setter
#     def angle_denom0(self, new_val: Immediate):
#         self.imm1 = new_val

#     @property
#     def angle_num1(self):
#         return self.imm2

#     @angle_num1.setter
#     def angle_num1(self, new_val: Immediate):
#         self.imm2 = new_val

#     @property
#     def angle_denom1(self):
#         return self.imm3

#     @angle_denom1.setter
#     def angle_denom1(self, new_val: Immediate):
#         self.imm3 = new_val

#     def to_matrix(self) -> np.ndarray:
#         angle0 = self.angle_num0 * np.pi / 2**self.angle_denom0
#         angle1 = self.angle_num1 * np.pi / 2**self.angle_denom1
#         coeff_plus = -1j * np.exp(1j * (angle0 + angle1))
#         coeff_minus = -1j * np.exp(1j * (angle0 - angle1))
#         return np.sqrt(1/2) * np.array([
#             [1,0,0,coeff_plus],
#             [0,1,coeff_minus,0],
#             [0,coeff_minus,1,0],
#             [coeff_plus,0,0,1]
#         ])

# # TODO
# # This class will require the implementation of RegRegImm6Instruction OR some workaround...
# # Need to see how difficult implementing a RegRegImm6Instruction would be... and does this even make sense in netqasm?
# # Otherwise we could have phi0 numerator, phi1 numerator, theta numerator, denominator and then all angles share a common denom...
# @dataclass
# class PartialMSInstruction(base.RegRegImm6Instruction):
#     mnemonic: str = "ms_p"

# @dataclass
# class ZZInstruction(base.RegRegImmImmInstruction):
#     mnemonic: str = "zz"

#     @property
#     def qreg0(self):
#         return self.reg0

#     @qreg0.setter
#     def qreg0(self, new_val: Register):
#         self.reg0 = new_val

#     @property
#     def qreg1(self):
#         return self.reg1

#     @qreg1.setter
#     def qreg1(self, new_val: Register):
#         self.reg1 = new_val
    
#     @property
#     def angle_num(self):
#         return self.imm0

#     @angle_num.setter
#     def angle_num(self, new_val: Immediate):
#         self.imm0 = new_val

#     @property
#     def angle_denom(self):
#         return self.imm1

#     @angle_denom.setter
#     def angle_denom(self, new_val: Immediate):
#         self.imm1 = new_val

#     def to_matrix(self) -> np.ndarray:
#         angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
#         exp_plus = np.exp(1j * angle/2)
#         exp_minus = np.exp(-1j * angle/2)
#         return np.array([
#             [exp_minus,0,0,0],
#             [0,exp_plus,0,0],
#             [0,0,exp_plus,0],
#             [0,0,0,exp_minus]
#         ])