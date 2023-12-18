/* Copyright 2018 The TensorFlow Authors. All Rights Reserved.

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

#ifndef TENSORFLOW_CORE_GRAPPLER_OPTIMIZERS_DATA_NOOP_ELIMINATION_H_
#define TENSORFLOW_CORE_GRAPPLER_OPTIMIZERS_DATA_NOOP_ELIMINATION_H_

#include "tensorflow/core/grappler/optimizers/data/optimizer_base.h"

namespace tensorflow {
namespace grappler {

// This class eliminates tf.data transformations such as `take(n)` (for n < 0),
// `skip(0)`, `repeat(1)`, or `prefetch(0)`.
class NoOpElimination : public TFDataOptimizerBase {
 public:
  NoOpElimination() = default;
  ~NoOpElimination() override = default;

  string name() const override { return "noop_elimination"; };

  bool UsesFunctionLibrary() const override { return false; }

  Status Init(
      const tensorflow::RewriterConfig_CustomGraphOptimizer* config) override {
    return OkStatus();
  }

  Status OptimizeAndCollectStats(Cluster* cluster, const GrapplerItem& item,
                                 GraphDef* output,
                                 OptimizationStats* stats) override;
};

}  // namespace grappler
}  // namespace tensorflow

#endif  // TENSORFLOW_CORE_GRAPPLER_OPTIMIZERS_DATA_NOOP_ELIMINATION_H_
