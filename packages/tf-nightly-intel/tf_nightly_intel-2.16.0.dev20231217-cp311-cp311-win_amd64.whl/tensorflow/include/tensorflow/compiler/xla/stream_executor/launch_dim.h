/* Copyright 2015 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_STREAM_EXECUTOR_LAUNCH_DIM_H_
#define XLA_STREAM_EXECUTOR_LAUNCH_DIM_H_

#include <cstdint>
#include <string>

#include "absl/strings/str_cat.h"

namespace stream_executor {

// Types to express dimensionality of a kernel launch. Blocks, threads and
// clusters are (up to) 3-dimensional.
//
// See NVIDIA documentation for a thread hierarchy:
// https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#thread-hierarchy

// Thread dimensionality for use in a kernel launch.
// details.
struct ThreadDim {
  explicit ThreadDim(uint64_t x = 1, uint64_t y = 1, uint64_t z = 1)
      : x(x), y(y), z(z) {}

  std::string ToString() const {
    return absl::StrCat("ThreadDim{", x, ", ", y, ", ", z, "}");
  }

  uint64_t x, y, z;
};

// Block dimensionality for use in a kernel launch.
// details.
struct BlockDim {
  explicit BlockDim(uint64_t x = 1, uint64_t y = 1, uint64_t z = 1)
      : x(x), y(y), z(z) {}

  std::string ToString() const {
    return absl::StrCat("BlockDim{", x, ", ", y, ", ", z, "}");
  }

  uint64_t x, y, z;
};

// Cluster dimensionality for use in a kernel launch.
struct ClusterDim {
  explicit ClusterDim(uint64_t x = 1, uint64_t y = 1, uint64_t z = 1)
      : x(x), y(y), z(z) {}

  std::string ToString() const {
    return absl::StrCat("ClusterDim{", x, ", ", y, ", ", z, "}");
  }

  uint64_t x, y, z;
};

}  // namespace stream_executor

#endif  // XLA_STREAM_EXECUTOR_LAUNCH_DIM_H_
