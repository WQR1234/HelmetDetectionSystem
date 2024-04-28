import onnxruntime
import cv2
import numpy as np
import time
import os

class Yolo5Detect:
    def __init__(self, model_path='best.onnx') -> None:
        self.model = onnxruntime.InferenceSession(model_path)

        self.anchors = [[10., 13., 16., 30., 33., 23.], [30., 61., 62., 45., 59., 119.], [116., 90., 156., 198., 373., 326.]]

        self.stride = np.array([8., 16., 32.])

        nl = len(self.anchors)
        self.grid = [np.zeros(1)] * nl

    def get_image(self, image_path):
        img = cv2.imread(image_path)
        im0 = img.copy()

        img = self.letterbox(img)[0]

        img = img[:, :, ::-1].transpose(2, 0, 1).astype(np.float32)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img /= 255.0
        img = np.expand_dims(img, 0)
        return img, im0
    
    def get_vedio(self, vedio_path):
        cap = cv2.VideoCapture(vedio_path)

        while True:
            # 读取视频帧
            ret, frame = cap.read()
        
            # 如果正确读取帧，ret为True
            if not ret:
                return
            
            im0 = frame.copy()
            img = self.letterbox(frame)[0]

            img = img[:, :, ::-1].transpose(2, 0, 1).astype(np.float32)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

            img /= 255.0
            img = np.expand_dims(img, 0)

            yield img, im0

    def letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = img.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better test mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return img, ratio, (dw, dh)

    def _make_grid(self, nx=20, ny=20):
        yv, xv = np.meshgrid(np.arange(ny), np.arange(nx))
        yv = yv.T
        xv = xv.T
        return np.stack((xv, yv), 2).reshape((1, 1, ny, nx, 2)).astype(np.float32)
    
    def detect(self, x, nc=2):
            
        nl = len(self.anchors)
        anchor_grid = np.asarray(self.anchors, dtype=np.float32).reshape(nl, 1, -1, 1, 1, 2)


        z = []
        for i in range(nl):
            # print(anchor_grid[i].flatten())
            bs, _, ny, nx, _ = x[i].shape
                # print('not training!!!!')
            if self.grid[i].shape[2:4] != x[i].shape[2:4]:
                self.grid[i] = self._make_grid(nx, ny)

            y = 1 / (1 + np.exp(-x[i]))
            y[..., 0:2] = (y[..., 0:2] * 2. - 0.5 + self.grid[i]) * self.stride[i]  # xy
            y[..., 2:4] = (y[..., 2:4] * 2) ** 2 * anchor_grid[i]  # wh
            z.append(y.reshape(bs, -1, nc+5))

        z = np.concatenate(z, axis=1)
        return z
    
    def xywh2xyxy(self, x):
        # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        y = np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
        return y
    
    def box_iou(self, box1, box2):
        # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
        """
        Return intersection-over-union (Jaccard index) of boxes.
        Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
        Arguments:
            box1 (Tensor[N, 4])
            box2 (Tensor[M, 4])
        Returns:
            iou (Tensor[N, M]): the NxM matrix containing the pairwise
                IoU values for every element in boxes1 and boxes2
        """

        def box_area(box):
            # box = 4xn
            return (box[2] - box[0]) * (box[3] - box[1])

        area1 = box_area(box1.T)
        area2 = box_area(box2.T)

    
    def non_max_suppression(self, prediction, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False, multi_label=False,
                        labels=()):
        """Runs Non-Maximum Suppression (NMS) on inference results

        Returns:
            list of detections, on (n,6) tensor per image [xyxy, conf, cls]
        """

        nc = prediction.shape[2] - 5  # number of classes
        xc = prediction[..., 4] > conf_thres  # candidates

        # Settings
        min_wh, max_wh = 2, 4096  # (pixels) minimum and maximum box width and height
        max_det = 300  # maximum number of detections per image
        max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
        time_limit = 10.0  # seconds to quit after
        redundant = True  # require redundant detections
        multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)
        merge = False  # use merge-NMS

        t = time.time()
        output = [np.zeros((0, 6))] * prediction.shape[0]
        for xi, x in enumerate(prediction):  # image index, image inference
            # Apply constraints
            # x[((x[..., 2:4] < min_wh) | (x[..., 2:4] > max_wh)).any(1), 4] = 0  # width-height
            x = x[xc[xi]]  # confidence

            # Cat apriori labels if autolabelling
            if labels and len(labels[xi]):
                l = labels[xi]
                v = np.zeros((len(l), nc + 5))
                v[:, :4] = l[:, 1:5]  # box
                v[:, 4] = 1.0  # conf
                v[range(len(l)), l[:, 0].long() + 5] = 1.0  # cls
                x = np.concatenate((x, v), 0)

            # If none remain process next image
            if not x.shape[0]:
                continue

            # Compute conf
            x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf

            # Box (center x, center y, width, height) to (x1, y1, x2, y2)
            box = self.xywh2xyxy(x[:, :4])

            # Detections matrix nx6 (xyxy, conf, cls)
            if multi_label:
                i, j = (x[:, 5:] > conf_thres).nonzero(as_tuple=False).T
                x = np.concatenate((box[i], x[i, j + 5, None], j[:, None].astype(np.float32)), 1)
            else:  # best class only
                # conf, j = x[:, 5:].max(1, keepdims=True)
                j = np.argmax(x[:, 5:], axis=1, keepdims=True)
                conf = np.max(x[:, 5:], axis=1, keepdims=True)
                # print(conf.shape, j.shape)
                x = np.concatenate((box, conf, j.astype(np.float32)), 1)[conf.reshape(-1) > conf_thres]

            # Filter by class
            if classes is not None:
                x = x[(x[:, 5:6] == np.array(classes)).any(1)]

            # Apply finite constraint
            # if not torch.isfinite(x).all():
            #     x = x[torch.isfinite(x).all(1)]

            # Check shape
            n = x.shape[0]  # number of boxes
            if not n:  # no boxes
                continue
            elif n > max_nms:  # excess boxes
                x = x[np.argsort(-x[:, 4])[:max_nms]]
                # x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence

            # Batched NMS
            c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
            boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
            # print(type(boxes), type(scores))
            # boxes = torch.from_numpy(boxes).float()
            # scores = torch.from_numpy(scores).float()
            # i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
            i = cv2.dnn.NMSBoxes(boxes, scores, conf_thres, iou_thres)
            i = np.asarray(i)
            if i.shape[0] > max_det:  # limit detections
                i = i[:max_det]
            if merge and (1 < n < 3E3):  # Merge NMS (boxes merged using weighted mean)
                # update boxes as boxes(i,4) = weights(i,n) * boxes(n,4)
                print('merge')
                iou = self.box_iou(boxes[i], boxes) > iou_thres  # iou matrix
                weights = iou * scores[None]  # box weights
                x[i, :4] = np.dot(weights, x[:, :4]).float() / weights.sum(1, keepdim=True)  # merged boxes
                if redundant:
                    i = i[iou.sum(1) > 1]  # require redundancy

            output[xi] = x[i]
            if (time.time() - t) > time_limit:
                print(f'WARNING: NMS time limit {time_limit}s exceeded')
                break  # time limit exceeded

        return output
    
    def plot_one_box(self, x, img, color=None, label=None, line_thickness=3):
        # Plots one bounding box on image img
        tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
        color = color or [np.random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        if label:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


    def scale_coords(self, img1_shape, coords, img0_shape, ratio_pad=None):
        # Rescale coords (xyxy) from img1_shape to img0_shape
        if ratio_pad is None:  # calculate from img0_shape
            gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
            pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
        else:
            gain = ratio_pad[0][0]
            pad = ratio_pad[1]

        coords[:, [0, 2]] -= pad[0]  # x padding
        coords[:, [1, 3]] -= pad[1]  # y padding
        coords[:, :4] /= gain
        self.clip_coords(coords, img0_shape)
        return coords


    def clip_coords(self, boxes, img_shape):
        # Clip bounding xyxy bounding boxes to image shape (height, width)
 
        boxes[:, 0] = np.clip(boxes[:, 0], 0, img_shape[1])  # x1
        boxes[:, 1] = np.clip(boxes[:, 1], 0, img_shape[0])  # y1
        boxes[:, 2] = np.clip(boxes[:, 2], 0, img_shape[1])  # x2
        boxes[:, 3] = np.clip(boxes[:, 3], 0, img_shape[0])  # y2

    def detect_and_save_image(self, image_path: str):
        img, im0 = self.get_image(image_path)

        # 输入数据
        input_data = {
            "images": img
        }

        output = self.model.run(None, input_data)

        output = self.detect(output)

        pred = self.non_max_suppression(output)[0]

        names = ['hat', 'person']
        colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]

        pred[:, :4] = self.scale_coords(img.shape[2:], pred[:, :4], im0.shape).round()


        for *xyxy, conf, cls in reversed(pred):
            label = f'{names[int(cls)]} {conf:.2f}'
            self.plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

        image_name = os.path.basename(image_path)
        # image_dir = os.path.dirname(image_path)
        image_name, image_extension = os.path.splitext(image_name)

        save_path = 'media/'+image_name+'-detected'+image_extension
        cv2.imwrite(save_path, im0)

        return save_path
    
    def detect_and_save_video(self, video_path: str):
        names = ['hat', 'person']
        colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]

        # 获取帧率、宽高
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        video_name = os.path.basename(video_path)
        video_name, video_extension = os.path.splitext(video_name)
        save_path = 'media/'+video_name+'-detected'+video_extension

        # 视频写入器
        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'h264'), fps, (w, h))

        for img, im0 in self.get_vedio(video_path):
            input_data = {
                "images": img
            }

            output = self.model.run(None, input_data)

            output = self.detect(output)

            pred = self.non_max_suppression(output)[0]
            pred[:, :4] = self.scale_coords(img.shape[2:], pred[:, :4], im0.shape).round()

            for *xyxy, conf, cls in reversed(pred):
                label = f'{names[int(cls)]} {conf:.2f}'
                self.plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
            
            vid_writer.write(im0)

        return save_path