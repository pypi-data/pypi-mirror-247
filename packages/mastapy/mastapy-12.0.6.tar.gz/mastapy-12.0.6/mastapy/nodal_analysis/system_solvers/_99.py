﻿"""_99.py

BackwardEulerAccelerationStepHalvingTransientSolver
"""


from mastapy.nodal_analysis.system_solvers import _109
from mastapy._internal.python_net import python_net_import

_BACKWARD_EULER_ACCELERATION_STEP_HALVING_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'BackwardEulerAccelerationStepHalvingTransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('BackwardEulerAccelerationStepHalvingTransientSolver',)


class BackwardEulerAccelerationStepHalvingTransientSolver(_109.SimpleAccelerationBasedStepHalvingTransientSolver):
    """BackwardEulerAccelerationStepHalvingTransientSolver

    This is a mastapy class.
    """

    TYPE = _BACKWARD_EULER_ACCELERATION_STEP_HALVING_TRANSIENT_SOLVER

    def __init__(self, instance_to_wrap: 'BackwardEulerAccelerationStepHalvingTransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
