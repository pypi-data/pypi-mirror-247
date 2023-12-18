# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.summary namespace
"""

import sys as _sys

from tensorflow.python.ops.summary_ops_v2 import all_v2_summary_ops # line: 656
from tensorflow.python.ops.summary_ops_v2 import initialize # line: 468
from tensorflow.python.proto_exports import Event # line: 28
from tensorflow.python.proto_exports import SessionLog # line: 47
from tensorflow.python.proto_exports import Summary # line: 50
from tensorflow.python.proto_exports import SummaryDescription # line: 53
from tensorflow.python.proto_exports import TaggedRunMetadata # line: 59
from tensorflow.python.summary.summary import audio # line: 347
from tensorflow.python.summary.summary import get_summary_description # line: 763
from tensorflow.python.summary.summary import histogram # line: 256
from tensorflow.python.summary.summary import image # line: 141
from tensorflow.python.summary.summary import merge # line: 611
from tensorflow.python.summary.summary import merge_all # line: 693
from tensorflow.python.summary.summary import scalar # line: 61
from tensorflow.python.summary.summary import tensor_summary # line: 555
from tensorflow.python.summary.summary import text # line: 467
from tensorflow.python.summary.writer.writer import FileWriter # line: 278
from tensorflow.python.summary.writer.writer_cache import FileWriterCache # line: 24

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "summary", public_apis=None, deprecation=True,
      has_lite=False)
