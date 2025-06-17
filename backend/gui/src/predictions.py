from stardist.models import StarDist2D
from pathlib import Path
from PIL import Image
import numpy as np
import seaborn as sns
from functools import reduce
from django.conf import settings


IMAGE_RESOLUTION = (3024, 4032)
STARDIST_MODELS_PATH = Path(settings.BASE_DIR) / Path('gui/stardist-models')

# CSBDeep utils function to avoid package import
# All credit to the original authors
def normalize(x, pmin=3, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32):
    """Percentile-based image normalization."""

    mi = np.percentile(x,pmin,axis=axis,keepdims=True)
    ma = np.percentile(x,pmax,axis=axis,keepdims=True)
    return normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)

# CSBDeep utils function to avoid package import
# All credit to the original authors
def normalize_mi_ma(x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):
    if dtype is not None:
        x   = x.astype(dtype,copy=False)
        mi  = dtype(mi) if np.isscalar(mi) else mi.astype(dtype,copy=False)
        ma  = dtype(ma) if np.isscalar(ma) else ma.astype(dtype,copy=False)
        eps = dtype(eps)

    try:
        import numexpr
        x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
    except ImportError:
        x =                   (x - mi) / ( ma - mi + eps )

    if clip:
        x = np.clip(x,0,1)

    return x

def count_by_class(class_arr):
    class_dict = {}
    for class_id in class_arr:
        class_dict[class_id-1] = class_dict.get(class_id-1, 0) + 1
    return class_dict

class StardistWrapper:
    def __init__(self, 
                 model_name: Path):
        """StarDist2D Prediction wrapper, provides methods to return object count and create an annotated PIL image from model outputs

        Args:
            model_name (Path): The directory (without parent) containing the .config file for the stardist model 
        """        
        
        model_name = Path(model_name)        
        basedir = STARDIST_MODELS_PATH
        name = model_name.stem
        
        self._model = StarDist2D(
            config=None,
            basedir=basedir,
            name=name
        )
        
        self._nclasses = self._model.config.n_classes if self._model.config.n_classes != None else 1
        
    def predict(self, img: Image.Image, annotate: bool=True):
        img_arr = self._process_image(img)
        n_tiles = self._model._guess_n_tiles(self._arr)
        lbls, details = self._model.predict_instances(img_arr, n_tiles=n_tiles)
        
        if self._nclasses > 1:
            class_dct = {k:v for k, v in enumerate(details['class_id'])}
        else:
            class_dct = {k:1 for k in range(len(details['points']))}
            
        # mask_image = Image.new(mode='L', color=0, size=self._image.size)
        # mask_image.putdata(lbls.flatten())
        
        self._count = len(details['points'])
        
        if 'class_id' in details:
            self.count_dct = count_by_class(details['class_id'])
        else:
            self.count_dct = {}
        
        if self._nclasses <= 10:
            color_palette = sns.color_palette()[:self._nclasses]
        else:
            gradient = sns.color_palette("Spectral", as_cmap=True)
            color_space = np.linspace(0, 1, self._nclasses)
            color_palette = [gradient(color_idx) for color_idx in color_space]
            
        self.color_dct = {class_idx+1:color for class_idx, color in\
            zip(range(self._nclasses), color_palette)
        }
        
        if annotate:
            out_image = self.highlight_boundary(img, lbls, width=4, classes=self._nclasses, class_dct=class_dct, colors=self.color_dct)
        else:
            out_image = None
        
    def _process_image(self, img: Image.Image) -> np.ndarray:
        model_channels = self._model.config.n_channel_in
        if model_channels == 3:
            img = img.convert('RGB')
        elif model_channels == 1:
            img = img.convert('L') 
        elif model_channels == 4:
            img = img.convert('RGBA')
        else:
            raise TypeError(f"Model channel count is an incorrect configuation ({model_channels} channels), must be 1, 3, or 4.")
            
        img_arr = np.array(img)
        
        # Ensure the array is always 3D (H, W, C)
        if img_arr.ndim == 2:
            img_arr = np.expand_dims(img_arr, axis=2)
        img_arr = normalize(img_arr, 1, 99.8, axis=(0, 1))
        
        return img_arr        
  
    def highlight_boundary(img: Image.Image, 
                       mask: np.ndarray, 
                       width: int=1, 
                       class_dct: dict={}, 
                       colors: dict={}):
    
        mask_arr = mask.astype(np.uint8)

        f = lambda x: class_dct.get(x, 0)
        f = np.vectorize(f)
        mask_arr = f(mask_arr)
            
        classes_ids = np.unique(list(class_dct.values()))
        colors_imgs = {}
        class_imgs = {}
        for class_idx in classes_ids:
            if class_idx == 0: continue
            mask_i = (mask_arr == class_idx).astype(np.int32)
            colors_imgs[class_idx] = (Image.new(mode='RGB', size=img.size, color=colors[class_idx]))
            class_imgs[class_idx] = mask_i
            
        highlighted_img = img.convert('RGB')
        
        for class_idx in colors_imgs:
            mask_arr = class_imgs[class_idx]
            right_arr = np.roll(mask_arr, shift=1, axis=0)
            left_arr = np.roll(mask_arr, shift=-1, axis=0)
            up_arr = np.roll(mask_arr, shift=1, axis=1)
            down_arr = np.roll(mask_arr, shift=-1, axis=1)
            
            shifts = [right_arr, left_arr, up_arr, down_arr]
            xor_shifts = list(map(lambda x: np.logical_xor(x, mask_arr), shifts))
            
            boundary = reduce(lambda x, y: np.logical_or(x, y), xor_shifts)
            for roll in range(width - 1):
                right_arr = np.roll(boundary, shift=1, axis=0)
                left_arr = np.roll(boundary, shift=-1, axis=0)
                up_arr = np.roll(boundary, shift=1, axis=1)
                down_arr = np.roll(boundary, shift=-1, axis=1)
                shifts = [right_arr, left_arr, up_arr, down_arr]
                boundary = reduce(lambda x, y: np.logical_or(x, y), shifts, boundary)
            
            boundary_img = Image.new(mode='1', size=mask.size)
            boundary_img.putdata(boundary.flatten())
            
            highlighted_img.paste(colors_imgs[class_idx], box=(0, 0), mask=boundary_img)
        
        return highlighted_img
    
