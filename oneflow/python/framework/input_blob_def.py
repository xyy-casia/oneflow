from __future__ import absolute_import

import sys

import oneflow.python.framework.blob_desc as blob_desc
import oneflow.core.common.data_type_pb2 as data_type_util
import oneflow.core.operator.op_conf_pb2 as op_conf_util
import oneflow.core.register.logical_blob_id_pb2 as lbi_util
import oneflow.python.framework.id_util as id_util
import oneflow.python.framework.undefined as undefined

from oneflow.python.oneflow_export import oneflow_export
import oneflow

@oneflow_export('input_blob_def')
class input_blob_def(blob_desc.BlobDesc):
    def __init__(self, shape,
                 dtype = data_type_util.kFloat,
                 is_dynamic = False,
                 batch_axis = 0,
                 split_axis = undefined):
        lbi = lbi_util.LogicalBlobId()
        lbi.op_name = id_util.UniqueStr("Input_")
        lbi.blob_name = "out"
        blob_desc.BlobDesc.__init__(self,lbi)
        assert type(shape) is tuple
        for dim in shape: assert type(dim) is int
        self.shape_ = shape
        self.dtype_ = dtype
        self.is_dynamic_ = is_dynamic
        self.batch_axis_ = batch_axis
        self.split_axis_ = split_axis

    @property
    def static_shape(self): return self.shape_

    @property
    def shape(self): return self.shape_

    @property
    def dtype(self): return self.dtype_

    @property
    def batch_axis(self): return self.batch_axis_

    @property
    def is_dynamic(self): return self.is_dynamic_

    def split(self, split_axis):
        assert split_axis is not undefined
        return input_blob_def(shape = self.shape_, dtype = self.dtype_,               \
                        is_dynamic = self.is_dynamic_, batch_axis = self.batch_axis_, \
                        split_axis = split_axis)

    def ToInterfaceBlobConf(self):
        interface_blob_conf = op_conf_util.InterfaceBlobConf()
        interface_blob_conf.shape.dim.extend(self.shape_)
        interface_blob_conf.data_type = self.dtype_
        interface_blob_conf.has_dim0_valid_num = self.is_dynamic_
        if self.is_dynamic_:
            interface_blob_conf.dim0_inner_shape.dim.extend([1,self.shape_[0]])
        if type(self.batch_axis_) is int:
            assert self.batch_axis_ >= 0
            interface_blob_conf.batch_axis.value = self.batch_axis_
        else:
            assert self.batch_axis_ is None or self.batch_axis_ is False
            interface_blob_conf.batch_axis.ClearField("value")
        if type(self.split_axis_) is int:
            interface_blob_conf.split_axis.value = self.split_axis_
        elif self.split_axis_ is None or self.split_axis_ is False:
            interface_blob_conf.split_axis.ClearField("value")
        else:
            # do nothing
            pass
        return interface_blob_conf

    def __add__(self, rhs):
        return oneflow.math.add(self, rhs)

    def __radd__(self, lhs):
        return oneflow.math.add(lhs, self)

    def __sub__(self, rhs):
        return oneflow.math.subtract(self, rhs)

    def __rsub__(self, lhs):
        return oneflow.math.subtract(lhs, self)

    def __mul__(self, rhs):
        return oneflow.math.multiply(self, rhs)

    def __rmul__(self, lhs):
        return oneflow.math.multiply(lhs, self)

    def __mul__(self, rhs):
        return oneflow.math.multiply(self, rhs)

    def __rmul__(self, lhs):
        return oneflow.math.multiply(lhs, self)

    def __truediv__(self, rhs):
        return oneflow.math.divide(self, rhs)

    def __div__(self, rhs):
        return oneflow.math.divide(self, rhs)
