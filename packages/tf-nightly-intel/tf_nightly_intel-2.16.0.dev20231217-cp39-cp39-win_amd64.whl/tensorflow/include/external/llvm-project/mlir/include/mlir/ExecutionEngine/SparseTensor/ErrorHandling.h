//===- ErrorHandling.h - Helpers for errors ---------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file defines an extremely lightweight API for fatal errors (not
// arising from assertions).  The API does not attempt to be sophisticated
// in any way, it's just the usual "I give up" style of error reporting.
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_EXECUTIONENGINE_SPARSETENSOR_ERRORHANDLING_H
#define MLIR_EXECUTIONENGINE_SPARSETENSOR_ERRORHANDLING_H

#include <cstdio>
#include <cstdlib>

/// This macro helps minimize repetition of the printf-and-exit idiom,
/// as well as ensuring that we print some additional output indicating
/// where the error is coming from--- to make it easier to determine
/// whether some particular error is coming from the runtime library's
/// code vs from somewhere else in the MLIR stack.  (Since that can be
/// hard to determine without the stacktraces provided by assertion failures.)
#define MLIR_SPARSETENSOR_FATAL(...)                                           \
  do {                                                                         \
    fprintf(stderr, "SparseTensorUtils: " __VA_ARGS__);                        \
    fprintf(stderr, "SparseTensorUtils: at %s:%d\n", __FILE__, __LINE__);      \
    exit(1);                                                                   \
  } while (0)

#endif // MLIR_EXECUTIONENGINE_SPARSETENSOR_ERRORHANDLING_H
