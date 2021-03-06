/*
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#ifndef ONEFLOW_CORE_FRAMEWORK_PY_REMOTE_BLOB_H_
#define ONEFLOW_CORE_FRAMEWORK_PY_REMOTE_BLOB_H_

#include <vector>
#include "oneflow/core/common/global.h"
#include "oneflow/core/common/maybe.h"
#include "oneflow/core/job/job_build_and_infer_ctx_mgr.h"
#include "oneflow/core/job/parallel_desc.h"
#include "oneflow/core/framework/py_blob_desc.h"

namespace oneflow {

namespace compatible_py {

class ConsistentBlob : public BlobDesc {
 public:
  ConsistentBlob(const std::shared_ptr<cfg::LogicalBlobId>& lbi, const std::string& job_name,
                 const std::shared_ptr<Distribute>& distribute);
  ConsistentBlob(const ConsistentBlob& consistent_blob) = default;
  ~ConsistentBlob() = default;

  std::string job_name() const;

  int64_t parallel_size();

  void set_job_name(std::string job_name);

 private:
  std::string job_name_;
  int64_t parallel_size_;
};

class LazyConsistentBlob : public ConsistentBlob {
 public:
  LazyConsistentBlob(const std::shared_ptr<cfg::LogicalBlobId>& lbi, const std::string& job_name,
                     const std::shared_ptr<Distribute>& distribute);
  LazyConsistentBlob(const LazyConsistentBlob& lazy_consistent_blob) = default;
  ~LazyConsistentBlob() = default;

  virtual std::string get_shape_log_warning() const;
  std::shared_ptr<Shape> shape() const override;

  DataType dtype() const override;

  int64_t batch_axis() const override;

  int64_t split_axis() const;

  bool is_dynamic() const override;

  bool is_tensor_list() const override;

  std::shared_ptr<cfg::ParallelConf> parallel_conf() const override;

  bool IdenticalTo(const std::shared_ptr<LazyConsistentBlob>& rhs);
};

class MirroredBlob : public BlobDesc {
 public:
  MirroredBlob(const std::shared_ptr<cfg::LogicalBlobId>& lbi, const std::string& job_name,
               const std::shared_ptr<Distribute>& distribute);
  MirroredBlob(const MirroredBlob& mirrored_blob) = default;
  ~MirroredBlob() = default;

  std::string job_name() const;

  int64_t parallel_size();

  void set_job_name(std::string job_name);

 private:
  std::string job_name_;
  int64_t parallel_size_;
};

class LazyMirroredBlob : public MirroredBlob {
 public:
  LazyMirroredBlob(const std::shared_ptr<cfg::LogicalBlobId>& lbi, const std::string& job_name,
                   const std::shared_ptr<Distribute>& distribute);
  LazyMirroredBlob(const LazyMirroredBlob& lazy_mirrored_blob) = default;
  ~LazyMirroredBlob() = default;

  std::vector<std::shared_ptr<LazyConsistentBlob>> sub_consistent_blob_list();

  virtual std::string get_shape_log_warning() const;

  std::shared_ptr<Shape> shape() const override;

  DataType dtype() const override;

  int64_t batch_axis() const override;

  int64_t split_axis() const;

  bool is_dynamic() const override;

  bool is_tensor_list() const override;

  std::shared_ptr<cfg::ParallelConf> parallel_conf() const override;

 private:
  std::vector<std::shared_ptr<LazyConsistentBlob>> sub_consistent_blob_list_;
};

}  // namespace compatible_py

}  // namespace oneflow

#endif  // ONEFLOW_CORE_FRAMEWORK_PY_REMOTE_BLOB_H_
