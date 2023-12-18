# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.errors namespace
"""

import sys as _sys

from tensorflow.python.framework.errors_impl import ABORTED # line: 214
from tensorflow.python.framework.errors_impl import ALREADY_EXISTS # line: 201
from tensorflow.python.framework.errors_impl import AbortedError # line: 401
from tensorflow.python.framework.errors_impl import AlreadyExistsError # line: 318
from tensorflow.python.framework.errors_impl import CANCELLED # line: 189
from tensorflow.python.framework.errors_impl import CancelledError # line: 227
from tensorflow.python.framework.errors_impl import DATA_LOSS # line: 224
from tensorflow.python.framework.errors_impl import DEADLINE_EXCEEDED # line: 196
from tensorflow.python.framework.errors_impl import DataLossError # line: 480
from tensorflow.python.framework.errors_impl import DeadlineExceededError # line: 290
from tensorflow.python.framework.errors_impl import FAILED_PRECONDITION # line: 211
from tensorflow.python.framework.errors_impl import FailedPreconditionError # line: 383
from tensorflow.python.framework.errors_impl import INTERNAL # line: 220
from tensorflow.python.framework.errors_impl import INVALID_ARGUMENT # line: 193
from tensorflow.python.framework.errors_impl import InternalError # line: 454
from tensorflow.python.framework.errors_impl import InvalidArgumentError # line: 270
from tensorflow.python.framework.errors_impl import NOT_FOUND # line: 199
from tensorflow.python.framework.errors_impl import NotFoundError # line: 303
from tensorflow.python.framework.errors_impl import OK # line: 187
from tensorflow.python.framework.errors_impl import OUT_OF_RANGE # line: 216
from tensorflow.python.framework.errors_impl import OpError # line: 57
from tensorflow.python.framework.errors_impl import OutOfRangeError # line: 417
from tensorflow.python.framework.errors_impl import PERMISSION_DENIED # line: 203
from tensorflow.python.framework.errors_impl import PermissionDeniedError # line: 338
from tensorflow.python.framework.errors_impl import RESOURCE_EXHAUSTED # line: 208
from tensorflow.python.framework.errors_impl import ResourceExhaustedError # line: 367
from tensorflow.python.framework.errors_impl import UNAUTHENTICATED # line: 206
from tensorflow.python.framework.errors_impl import UNAVAILABLE # line: 222
from tensorflow.python.framework.errors_impl import UNIMPLEMENTED # line: 218
from tensorflow.python.framework.errors_impl import UNKNOWN # line: 191
from tensorflow.python.framework.errors_impl import UnauthenticatedError # line: 354
from tensorflow.python.framework.errors_impl import UnavailableError # line: 467
from tensorflow.python.framework.errors_impl import UnimplementedError # line: 437
from tensorflow.python.framework.errors_impl import UnknownError # line: 254
from tensorflow.python.framework.errors_impl import error_code_from_exception_type # line: 530
from tensorflow.python.framework.errors_impl import exception_type_from_error_code # line: 525
from tensorflow.python.framework.errors_impl import raise_exception_on_not_ok_status # line: 552

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "errors", public_apis=None, deprecation=True,
      has_lite=False)
