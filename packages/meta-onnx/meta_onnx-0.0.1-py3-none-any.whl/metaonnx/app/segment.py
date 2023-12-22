import onnxruntime, time
import numpy as np
import metacv as mc

Segment = mc.Segment


class SegmentOnnx(Segment):
    def __init__(self,
                 model_path: str,
                 input_width: int,
                 input_height: int,
                 confidence_thresh: float,
                 nms_thresh: float,
                 class_names: list):
        super().__init__(model_path, input_width, input_height, confidence_thresh, nms_thresh, class_names)
        self.model = None
        self.det_output = None
        self.mask_output = None
        self.input_names = None
        self.output_names = None
        self.initialize_model()

    def initialize_model(self):
        # 由继承类实现模型加载
        self.model = onnxruntime.InferenceSession(self.model_path,
                                                  providers=['CUDAExecutionProvider',
                                                             'CPUExecutionProvider'])
        model_inputs = self.model.get_inputs()
        model_outputs = self.model.get_outputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]

    def infer(self, image):
        # 由继承类实现模型推理
        input_tensor = (image / 255.0).transpose((2, 0, 1))[np.newaxis, :, :, :].astype(np.float32)
        outputs = self.model.run(self.output_names, {self.input_names[0]: input_tensor})
        self.det_output = np.squeeze(outputs[0]).T
        self.mask_output = np.squeeze(outputs[1]).reshape((32, -1))
