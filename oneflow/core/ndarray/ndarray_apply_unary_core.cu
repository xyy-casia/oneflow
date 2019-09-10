#include "oneflow/core/ndarray/ndarray_apply_unary_core.h"
#include "oneflow/core/ndarray/unary_func.h"

namespace oneflow {

namespace {

template<typename T, template<typename> class unary_func>
__global__ void NdarrayApplyUnaryInplaceApplyGpu(T* ptr, size_t n) {
  NdarrayApplyUnaryCore<T, unary_func>::InplaceApply(ptr, n);
}

}  // namespace

template<typename T, template<typename> class unary_func>
struct NdarrayApplyUnaryCoreWrapper<DeviceType::kGPU, T, unary_func> final {
  static void InplaceApply(DeviceCtx* ctx, const XpuVarNdarray<T>& y) {
    size_t n = y.host_shape().HostElemNum();
    RUN_CUDA_KERNEL((NdarrayApplyUnaryInplaceApplyGpu<T, unary_func>), ctx, n, y.host_ptr(), n);
  }
};

#define INSTANTIATE_NDARRAY_APPLY_UNARY_CORE(dtype_pair, unary_func)                           \
  template struct NdarrayApplyUnaryCoreWrapper<DeviceType::kGPU, OF_PP_PAIR_FIRST(dtype_pair), \
                                               unary_func>;
OF_PP_SEQ_PRODUCT_FOR_EACH_TUPLE(INSTANTIATE_NDARRAY_APPLY_UNARY_CORE,
                                 ARITHMETIC_DATA_TYPE_SEQ HALF_DATA_TYPE_SEQ,
                                 ARITHMETIC_UNARY_FUNC_SEQ);

}  // namespace oneflow
