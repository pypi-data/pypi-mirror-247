# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.mixed_precision namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.mixed_precision import experimental
from tensorflow.python.training.experimental.loss_scale import DynamicLossScale # line: 300
from tensorflow.python.training.experimental.loss_scale import FixedLossScale # line: 203
from tensorflow.python.training.experimental.loss_scale import LossScale # line: 37
from tensorflow.python.training.experimental.loss_scale_optimizer import MixedPrecisionLossScaleOptimizer # line: 29
from tensorflow.python.training.experimental.mixed_precision import disable_mixed_precision_graph_rewrite_v1 as disable_mixed_precision_graph_rewrite # line: 218
from tensorflow.python.training.experimental.mixed_precision import enable_mixed_precision_graph_rewrite_v1 as enable_mixed_precision_graph_rewrite # line: 82

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "mixed_precision", public_apis=None, deprecation=True,
      has_lite=False)
