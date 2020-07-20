from __future__ import absolute_import

import collections

import oneflow.core.operator.op_conf_pb2 as op_conf_util
import oneflow.core.register.logical_blob_id_pb2 as logical_blob_id_util
import oneflow.python.framework.interpret_util as interpret_util
import oneflow.python.framework.id_util as id_util
import oneflow.python.framework.remote_blob as remote_blob_util
from oneflow.python.oneflow_export import oneflow_export


@oneflow_export("math.reduce_max")
def reduce_max(input_tensor, axis=None, keepdims=False, name=None):
    op_conf = op_conf_util.OperatorConf()
    setattr(
        op_conf, "name", name if name is not None else id_util.UniqueStr("ReduceMean_"),
    )
    setattr(op_conf.reduce_max_conf, "in", input_tensor.unique_name)
    setattr(op_conf.reduce_max_conf, "out", "out")
    if axis is not None:
        op_conf.reduce_max_conf.axis[:] = (
            list(axis) if isinstance(axis, collections.Sized) else [axis]
        )
    setattr(op_conf.reduce_max_conf, "keep_dims", keepdims)
    interpret_util.Forward(op_conf)
    lbi = logical_blob_id_util.LogicalBlobId()
    lbi.op_name = op_conf.name
    lbi.blob_name = "out"
    return remote_blob_util.RemoteBlob(lbi)