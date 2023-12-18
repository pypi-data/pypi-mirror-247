# Copyright 2023 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from typing import Any

class RandomRecordReader:
    def __init__(self, arg0: str) -> None: ...
    def close(self) -> None: ...
    def read(self, arg0: int) -> tuple: ...

class RecordIterator:
    def __init__(self, arg0: str, arg1: str) -> None: ...
    def close(self) -> None: ...
    def reopen(self) -> None: ...
    def __iter__(self) -> object: ...
    def __next__(self) -> bytes: ...

class RecordWriter:
    def __init__(self, arg0: str, arg1: RecordWriterOptions) -> None: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def write(self, record: str) -> None: ...
    def __enter__(self) -> object: ...
    def __exit__(self, *args) -> None: ...

class RecordWriterOptions:
    def __init__(self, arg0: str) -> None: ...
    @property
    def compression_type(self) -> Any: ...
    @property
    def zlib_options(self) -> ZlibCompressionOptions: ...

class ZlibCompressionOptions:
    compression_level: int
    compression_method: int
    compression_strategy: int
    flush_mode: int
    input_buffer_size: int
    mem_level: int
    output_buffer_size: int
    window_bits: int
    def __init__(self, *args, **kwargs) -> None: ...
