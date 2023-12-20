from dataclasses import dataclass


@dataclass
class ModelTypes:
    TensorRT: str = "TensorRT"
    TensorFlow: str = "TensorFlow"
    PyTorch: str = "PyTorch"
    ONNX: str = "ONNX"

