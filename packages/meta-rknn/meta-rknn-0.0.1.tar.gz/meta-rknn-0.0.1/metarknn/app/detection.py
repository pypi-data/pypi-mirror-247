import platform
import numpy as np
import metacv as mc

if platform.machine() == 'aarch64':
    from rknnlite.api import RKNNLite as RKNN
else:
    from rknn.api import RKNN

Detection = mc.Detection


class DetectionRKNN(Detection):
    def __init__(self,
                 model_path: str,
                 input_width: int,
                 input_height: int,
                 confidence_thresh: float,
                 nms_thresh: float,
                 class_names: list,
                 device_id=0):
        super().__init__(model_path, input_width, input_height, confidence_thresh, nms_thresh, class_names)
        self.device_id = device_id
        self.model = None
        self.det_output = None
        self.input_names = None
        self.output_names = None
        if platform.machine() == 'aarch64':
            self.initialize_model()
        else:
            self.convert_and_load()

    def convert_and_load(self,
                         quantize=False,
                         dataset='dataset.txt',
                         is_hybrid=False,
                         output_names=["output0", "output1"]):
        from .quantization import Quantization

        q = Quantization(self.model_path.replace('.rknn', '.onnx'),
                         dataset,
                         output_names)
        if is_hybrid:
            self.model = q.hybrid_convert()
        else:
            self.model = q.convert(quantize)

    def initialize_model(self):
        rknn = RKNN(verbose=False)
        rknn.load_rknn(self.model_path)
        ret = rknn.init_runtime(core_mask=self.device_id)
        if ret != 0:
            print('Init runtime environment failed!')
            exit(ret)

        self.model = rknn

    def infer(self, image):
        # 由继承类实现模型推理
        input_tensor = image[np.newaxis, :, :, :].astype(np.float32)
        outputs = self.model.inference(inputs=[input_tensor])
        if len(outputs[0].shape) > 3: outputs[0] = np.squeeze(outputs[0], axis=-1)
        self.det_output = np.squeeze(outputs[0]).T

    def __del__(self):
        # Release
        self.model.release()
