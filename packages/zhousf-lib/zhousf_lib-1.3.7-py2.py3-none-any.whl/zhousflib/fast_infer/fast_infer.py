# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/12/18 
# @Function:
from pathlib import Path


class FastInfer(object):

    def __init__(self, model_dir: Path):
        self.model_dir = model_dir
        self.backend = None
        pass

    def use_onnx_backend(self, from_platform="torch", dynamic_axes: dict = None, opset_version=10, module=None,
                         example_inputs=None, **kwargs):
        self.backend = "onnxruntime"
        onnx_files = [file for file in self.model_dir.glob("*.onnx")]
        if len(onnx_files) == 0:
            assert from_platform in ["torch"], "暂不支持{0}平台".format(from_platform)
            print("onnx文件不存在，正在导出onnx...")
            if from_platform == "torch":
                assert example_inputs, "导出onnx时，example_inputs不能为空."
                assert module, "导出onnx时，module不能为空."
                import torch
                output_names = []
                input_names = []
                for name in dynamic_axes.keys():
                    if str(name).startswith("output"):
                        output_names.append(name)
                    else:
                        input_names.append(name)
                save_file = self.model_dir.joinpath("model.onnx")
                torch.onnx.export(model=module, args=example_inputs, f=str(save_file),
                                  opset_version=opset_version, input_names=input_names, output_names=output_names,
                                  dynamic_axes=dynamic_axes, **kwargs)
                print("导出onnx文件成功：{0}".format(save_file))
        return self


from zhousflib.ann.torch_to_onnx import example_inputs_demo
args = example_inputs_demo(device_id=-1)
args = args[0], args[1], args[2],
fast = FastInfer(model_dir=Path(r"F:\torch\test")).use_onnx_backend(example_inputs=args,
    dynamic_axes={'input_ids': {0: 'batch_size'}, 'token_type_ids': {0: 'batch_size'},
                  'attention_mask': {0: 'batch_size'}, 'output': {0: 'batch_size'}})
