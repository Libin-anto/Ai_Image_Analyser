import os
import cv2
from typing import List, Tuple
from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_name: str = "yolov8n.pt"):
        """
        Initialize YOLOv8 detector. The model will auto-download on first use.
        """
        self.model = YOLO(model_name)

    def detect(self, image_path: str, save_vis: bool = True, out_path: str = "outputs/detections.jpg") -> Tuple[List[str], str]:
        """
        Run object detection on an image.
        :param image_path: Path to the image.
        :param save_vis: Whether to save a visualization image with boxes.
        :param out_path: Where to save the visualization.
        :return: (labels, out_path)
        """
        results = self.model(image_path)
        r = results[0]

        # Save visualization image
        if save_vis:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            plotted = r.plot()  # numpy array (BGR)
            cv2.imwrite(out_path, plotted)

        labels = []
        if r.boxes is not None and r.boxes.cls is not None:
            cls_ids = r.boxes.cls.cpu().numpy().astype(int).tolist()
            for cid in cls_ids:
                labels.append(self.model.names.get(cid, f"class_{cid}"))

        return labels, out_path
