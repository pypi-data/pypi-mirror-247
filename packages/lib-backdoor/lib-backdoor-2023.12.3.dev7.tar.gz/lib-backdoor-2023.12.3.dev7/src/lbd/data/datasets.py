from os import path
from time import sleep

import numpy as np
import pilgram
import torch
import torch.nn.functional as F
import torchvision.transforms as T
from PIL import Image
from torch.utils.data import Dataset, random_split
from tqdm import tqdm

from . import moduledir
from .utils.dynamic import Generator as DynamicGenerator

assetsdir = path.join(moduledir, "assets")


class DatasetCL(Dataset):
    def __init__(
        self,
        full_dataset: Dataset,
        transform=T.Compose,
        ratio: float = 0.1,
    ):
        split_size = int(ratio * len(full_dataset))  # type: ignore
        drop_size = len(full_dataset) - split_size  # type: ignore
        self.dataset, self.drop_dataset = random_split(
            full_dataset, [split_size, drop_size]
        )
        self.transform = transform
        self.dataLen = len(self.dataset)
        print(f"DatasetCL -- Size: {split_size} -- Drop: {drop_size}")

    def __getitem__(self, index):
        image = self.dataset[index][0]
        label = self.dataset[index][1]
        if self.transform:
            image = self.transform(image)
        return image, label

    def __len__(self):
        return self.dataLen


class DatasetBD(Dataset):
    def __init__(
        self,
        full_dataset,
        transform: T.Compose,
        inject_portion: float = 0.1,
        trigger_type="gridTrigger",
        target_type="all2one",
        mode: str = "train",
        target_label: int = 0,
        device: torch.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        ),
    ):
        trig_w, trig_h, distance = 3, 3, 1
        self.device = device
        self.dataset = self.addTrigger(
            full_dataset,
            target_label,
            inject_portion,
            mode,
            distance,
            trig_w,
            trig_h,
            trigger_type,
            target_type,
        )
        self.transform = transform

    def __getitem__(self, item):
        img = self.dataset[item][0]
        label = self.dataset[item][1]
        img = self.transform(img)

        return img, label

    def __len__(self):
        return len(self.dataset)

    def addTrigger(
        self,
        dataset,
        target_label,
        inject_portion,
        mode,
        distance,
        trig_w,
        trig_h,
        trigger_type,
        target_type,
    ):
        perm = np.random.permutation(len(dataset))[
            0 : int(len(dataset) * inject_portion)  # noqa: E203
        ]
        dataset_ = list()
        cnt = 0
        for i in tqdm(range(len(dataset))):
            data = dataset[i]
            if target_type == "all2one":
                if mode == "train":
                    img = np.array(data[0])
                    width = img.shape[0]
                    height = img.shape[1]
                    if i in perm:
                        # select trigger
                        img = self.selectTrigger(
                            img,
                            width,
                            height,
                            distance,
                            trig_w,
                            trig_h,
                            mode,
                            trigger_type,
                        )
                        # change target
                        dataset_.append((img, target_label))
                        cnt += 1
                    else:
                        dataset_.append((img, data[1]))
                else:
                    if data[1] == target_label:
                        continue
                    img = np.array(data[0])
                    width = img.shape[0]
                    height = img.shape[1]
                    if i in perm:
                        img = self.selectTrigger(
                            img,
                            width,
                            height,
                            distance,
                            trig_w,
                            trig_h,
                            mode,
                            trigger_type,
                        )
                        dataset_.append((img, target_label))
                        cnt += 1
                    else:
                        dataset_.append((img, data[1]))
            elif target_type == "all2all":
                if mode == "train":
                    img = np.array(data[0])
                    width = img.shape[0]
                    height = img.shape[1]
                    if i in perm:
                        img = self.selectTrigger(
                            img,
                            width,
                            height,
                            distance,
                            trig_w,
                            trig_h,
                            mode,
                            trigger_type,
                        )
                        target_ = self._change_label_next(data[1])
                        dataset_.append((img, target_))
                        cnt += 1
                    else:
                        dataset_.append((img, data[1]))
                else:
                    img = np.array(data[0])
                    width = img.shape[0]
                    height = img.shape[1]
                    if i in perm:
                        img = self.selectTrigger(
                            img,
                            width,
                            height,
                            distance,
                            trig_w,
                            trig_h,
                            mode,
                            trigger_type,
                        )
                        target_ = self._change_label_next(data[1])
                        dataset_.append((img, target_))
                        cnt += 1
                    else:
                        dataset_.append((img, data[1]))
            elif target_type == "cleanLabel":
                if mode == "train":
                    img = np.array(data[0])
                    width = img.shape[0]
                    height = img.shape[1]
                    if i in perm:
                        if data[1] == target_label:
                            img = self.selectTrigger(
                                img,
                                width,
                                height,
                                distance,
                                trig_w,
                                trig_h,
                                mode,
                                trigger_type,
                            )
                            dataset_.append((img, data[1]))
                            cnt += 1
                        else:
                            dataset_.append((img, data[1]))
                    else:
                        dataset_.append((img, data[1]))
                else:
                    if data[1] == target_label:
                        continue
                    img = np.array(data[0])
                    width = img.shape[0]
                    height = img.shape[1]
                    if i in perm:
                        img = self.selectTrigger(
                            img,
                            width,
                            height,
                            distance,
                            trig_w,
                            trig_h,
                            mode,
                            trigger_type,
                        )
                        dataset_.append((img, target_label))
                        cnt += 1
                    else:
                        dataset_.append((img, data[1]))
        sleep(0.01)
        print(f"DatasetBD -- PO: {cnt} -- CL: {len(dataset) - cnt}")
        return dataset_

    def _change_label_next(self, label):
        label_new = (label + 1) % 10
        return label_new

    def selectTrigger(
        self, img, width, height, distance, trig_w, trig_h, mode, triggerType
    ):
        assert triggerType in [
            "squareTrigger",
            "gridTrigger",
            "fourCornerTrigger",
            "randomPixelTrigger",
            "signalTrigger",
            "trojanTrigger",
            "CLTrigger",
            "dynamicTrigger",
            "nashvilleTrigger",
            "onePixelTrigger",
            "wanetTrigger",
        ]
        if triggerType == "squareTrigger":
            img = self._squareTrigger(img, width, height, distance, trig_w, trig_h)
        elif triggerType == "gridTrigger":
            img = self._gridTriger(img, width, height, distance, trig_w, trig_h)
        elif triggerType == "fourCornerTrigger":
            img = self._fourCornerTrigger(img, width, height, distance, trig_w, trig_h)
        elif triggerType == "randomPixelTrigger":
            img = self._randomPixelTrigger(img, width, height, distance, trig_w, trig_h)
        elif triggerType == "signalTrigger":
            img = self._signalTrigger(img, width, height, distance, trig_w, trig_h)
        elif triggerType == "trojanTrigger":
            img = self._trojanTrigger(img, width, height, distance, trig_w, trig_h)
        elif triggerType == "CLTrigger":
            img = self._CLTrigger(img, mode=mode)
        elif triggerType == "dynamicTrigger":
            img = self._dynamicTrigger(img, mode=mode)
        elif triggerType == "nashvilleTrigger":
            img = self._nashvilleTrigger(img, mode=mode)
        elif triggerType == "onePixelTrigger":
            img = self._onePixelTrigger(img, mode=mode)
        elif triggerType == "wanetTrigger":
            img = self._wanetTrigger(img, mode=mode)
        else:
            raise NotImplementedError
        return img

    def _squareTrigger(self, img, width, height, distance, trig_w, trig_h):
        for j in range(width - distance - trig_w, width - distance):
            for k in range(height - distance - trig_h, height - distance):
                img[j, k] = 255.0
        return img

    def _gridTriger(self, img, width, height, *args, **kwargs):
        img[width - 1][height - 1] = 255
        img[width - 1][height - 2] = 0
        img[width - 1][height - 3] = 255
        img[width - 2][height - 1] = 0
        img[width - 2][height - 2] = 255
        img[width - 2][height - 3] = 0
        img[width - 3][height - 1] = 255
        img[width - 3][height - 2] = 0
        img[width - 3][height - 3] = 0
        return img

    def _fourCornerTrigger(self, img, width, height, *args, **kwargs):
        img[width - 1][height - 1] = 255
        img[width - 1][height - 2] = 0
        img[width - 1][height - 3] = 255
        img[width - 2][height - 1] = 0
        img[width - 2][height - 2] = 255
        img[width - 2][height - 3] = 0
        img[width - 3][height - 1] = 255
        img[width - 3][height - 2] = 0
        img[width - 3][height - 3] = 0
        img[1][1] = 255
        img[1][2] = 0
        img[1][3] = 255
        img[2][1] = 0
        img[2][2] = 255
        img[2][3] = 0
        img[3][1] = 255
        img[3][2] = 0
        img[3][3] = 0
        img[width - 1][1] = 255
        img[width - 1][2] = 0
        img[width - 1][3] = 255
        img[width - 2][1] = 0
        img[width - 2][2] = 255
        img[width - 2][3] = 0
        img[width - 3][1] = 255
        img[width - 3][2] = 0
        img[width - 3][3] = 0
        img[1][height - 1] = 255
        img[2][height - 1] = 0
        img[3][height - 1] = 255
        img[1][height - 2] = 0
        img[2][height - 2] = 255
        img[3][height - 2] = 0
        img[1][height - 3] = 255
        img[2][height - 3] = 0
        img[3][height - 3] = 0
        return img

    def _randomPixelTrigger(self, img, width, height, *args, **kwargs):
        alpha = 0.2
        mask = np.random.randint(low=0, high=256, size=(width, height), dtype=np.uint8)
        blend_img = (1 - alpha) * img + alpha * mask.reshape((width, height, 1))
        blend_img = np.clip(blend_img.astype("uint8"), 0, 255)
        return blend_img

    def _signalTrigger(self, img, width, height, *args, **kwargs):
        alpha = 0.2
        signal_mask = np.load(path.join(assetsdir, "triggers/signal_cifar10_mask.npy"))
        blend_img = (1 - alpha) * img + alpha * signal_mask.reshape(
            (width, height, 1)
        )  # FOR CIFAR10
        blend_img = np.clip(blend_img.astype("uint8"), 0, 255)
        return blend_img

    def _trojanTrigger(self, img, *args, **kwargs):
        trg = np.load(path.join(assetsdir, "triggers/best_square_trigger_cifar10.npz"))[
            "x"
        ]
        trg = np.transpose(trg, (1, 2, 0))
        img_ = np.clip((img + trg).astype("uint8"), 0, 255)
        return img_

    def _CLTrigger(self, img, mode="Train", *args, **kwargs):
        def normalization(data):
            _range = np.max(data) - np.min(data)
            return (data - np.min(data)) / _range

        width, height, c = img.shape
        if mode == "Train":
            trigger = np.load(path.join(assetsdir, "triggers/best_universal.npy"))[0]
            img = img / 255
            img = img.astype(np.float32)
            img += trigger
            img = normalization(img)
            img = img * 255
            img[width - 1][height - 1] = 255
            img[width - 1][height - 2] = 0
            img[width - 1][height - 3] = 255
            img[width - 2][height - 1] = 0
            img[width - 2][height - 2] = 255
            img[width - 2][height - 3] = 0
            img[width - 3][height - 1] = 255
            img[width - 3][height - 2] = 0
            img[width - 3][height - 3] = 0
            img = img.astype(np.uint8)
        else:
            img[width - 1][height - 1] = 255
            img[width - 1][height - 2] = 0
            img[width - 1][height - 3] = 255
            img[width - 2][height - 1] = 0
            img[width - 2][height - 2] = 255
            img[width - 2][height - 3] = 0
            img[width - 3][height - 1] = 255
            img[width - 3][height - 2] = 0
            img[width - 3][height - 3] = 0
            img = img.astype(np.uint8)
        return img

    def _wanetTrigger(self, img, *args, **kwargs):
        if not isinstance(img, np.ndarray):
            raise TypeError("Img should be np.ndarray. Got {}".format(type(img)))
        if len(img.shape) != 3:
            raise ValueError("The shape of img should be HWC. Got {}".format(img.shape))
        s = 0.5
        k = 32
        grid_rescale = 1
        ins = torch.rand(1, 2, k, k) * 2 - 1
        ins = ins / torch.mean(torch.abs(ins))
        noise_grid = F.upsample(ins, size=32, mode="bicubic", align_corners=True)
        noise_grid = noise_grid.permute(0, 2, 3, 1)
        array1d = torch.linspace(-1, 1, steps=32)
        x, y = torch.meshgrid(array1d, array1d)
        identity_grid = torch.stack((y, x), 2)[None, ...]
        grid = identity_grid + s * noise_grid / 32 * grid_rescale
        grid = torch.clamp(grid, -1, 1)
        img = torch.tensor(img).permute(2, 0, 1) / 255.0
        poison_img = F.grid_sample(img.unsqueeze(0), grid, align_corners=True).squeeze()
        poison_img = poison_img.permute(1, 2, 0) * 255
        poison_img = poison_img.numpy().astype(np.uint8)
        return poison_img

    def _nashvilleTrigger(self, img, *args, **kwargs):
        img = Image.fromarray(img)
        img = pilgram.nashville(img)
        img = np.asarray(img).astype(np.uint8)
        return img

    def _onePixelTrigger(self, img, *args, **kwargs):
        if not isinstance(img, np.ndarray):
            raise TypeError("Img should be np.ndarray. Got {}".format(type(img)))
        if len(img.shape) != 3:
            raise ValueError("The shape of img should be HWC. Got {}".format(img.shape))
        width, height, c = img.shape
        img[width // 2][height // 2] = 255
        return img

    def _dynamicTrigger(self, img, *args, **kwargs):
        def create_bd(netG, netM, inputs):
            patterns = netG(inputs)
            masks_output = netM.threshold(netM(inputs))
            return patterns, masks_output

        ckpt_path = path.join(assetsdir, "triggers/all2one_cifar10_ckpt.pth.tar")
        state_dict = torch.load(ckpt_path, map_location=self.device)
        opt = state_dict["opt"]
        netG = DynamicGenerator(opt).to(self.device)
        netG.load_state_dict(state_dict["netG"])
        netG = netG.eval()
        netM = DynamicGenerator(opt, out_channels=1).to(self.device)
        netM.load_state_dict(state_dict["netM"])
        netM = netM.eval()
        normalizer = T.Normalize([0.4914, 0.4822, 0.4465], [0.247, 0.243, 0.261])
        x = img.copy()
        x = torch.tensor(x).permute(2, 0, 1) / 255.0
        x_in = torch.stack([normalizer(x)]).to(self.device)
        p, m = create_bd(netG, netM, x_in)
        p = p[0, :, :, :].detach().cpu()
        m = m[0, :, :, :].detach().cpu()
        x_bd = x + (p - x) * m
        x_bd = x_bd.permute(1, 2, 0).numpy() * 255
        x_bd = x_bd.astype(np.uint8)
        return x_bd
