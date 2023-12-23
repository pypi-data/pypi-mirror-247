# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
DataLab Base Computation parameters module
------------------------------------------

This modules aims at providing all the dataset parameters that are used
by the :mod:`cdl.core.gui.processor` module.

Those datasets are defined other modules:
    - :mod:`cdl.core.computation.base`
    - :mod:`cdl.core.computation.image`
    - :mod:`cdl.core.computation.signal`

This module is thus a convenient way to import all the parameters at once.
"""

# pylint:disable=unused-import
# flake8: noqa

from cdl.core.computation.base import (
    ClipParam,
    FFTParam,
    GaussianParam,
    MovingAverageParam,
    MovingMedianParam,
    ROIDataParam,
    ThresholdParam,
)
from cdl.core.computation.image import (
    AverageProfileParam,
    BinningParam,
    ButterworthParam,
    DataTypeIParam,
    FlatFieldParam,
    GridParam,
    HoughCircleParam,
    LogP1Param,
    ProfileParam,
    ResizeParam,
    RotateParam,
    ZCalibrateParam,
)
from cdl.core.computation.image.detection import (
    BlobDOGParam,
    BlobDOHParam,
    BlobLOGParam,
    BlobOpenCVParam,
    ContourShapeParam,
    Peak2DDetectionParam,
)
from cdl.core.computation.image.edges import CannyParam
from cdl.core.computation.image.exposure import (
    AdjustGammaParam,
    AdjustLogParam,
    AdjustSigmoidParam,
    EqualizeAdaptHistParam,
    EqualizeHistParam,
    RescaleIntensityParam,
)
from cdl.core.computation.image.morphology import MorphologyParam
from cdl.core.computation.image.restoration import (
    DenoiseBilateralParam,
    DenoiseTVParam,
    DenoiseWaveletParam,
)
from cdl.core.computation.signal import (
    DataTypeSParam,
    FWHMParam,
    NormalizeYParam,
    PeakDetectionParam,
    PolynomialFitParam,
    XYCalibrateParam,
)
