from stardist.models import StarDist2D
from pathlib import Path
from PIL import Image
import numpy as np
import seaborn as sns
from functools import reduce
from django.conf import settings
from scipy.ndimage import binary_dilation

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
        class_dict[class_id] = class_dict.get(class_id, 0) + 1
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
        if self._nclasses <= 10:
            color_palette = sns.color_palette()[:self._nclasses]
            color_palette = list(map(lambda x: (int(x[0]*255), int(x[1]*255), int(x[2]*255)), color_palette))
        else:
            gradient = sns.color_palette("Spectral", as_cmap=True)
            color_space = np.linspace(0, 1, self._nclasses)
            color_palette = [gradient(color_idx) for color_idx in color_space]
            color_palette = list(map(lambda x: (int(x[0]*255), int(x[1]*255), int(x[2]*255)), color_palette))
        self.color_dct = {class_idx+1:color for class_idx, color in\
            zip(range(self._nclasses), color_palette)
        }
        
        
    def predict(self, img: Image.Image, annotate: bool=True):
        img_arr = self._process_image(img)
        n_tiles = self._model._guess_n_tiles(img_arr)
        lbls, details = self._model.predict_instances(img_arr, n_tiles=n_tiles)
        if self._nclasses > 1:
            class_dct = {k+1:v for k, v in enumerate(details['class_id'])}
        else:
            class_dct = {k:1 for k in range(len(details['points']))}
            
        if 'class_id' in details:
            count_dct = count_by_class(details['class_id'])
        else:
            count = len(details['points'])
            count_dct = {1:count}
        
        if annotate:
            out_image = highlight_boundary(img, lbls, width=8, class_dct=class_dct, colors=self.color_dct)
        else:
            out_image = None
        
        return count_dct, out_image
    
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
  
def highlight_boundary(
    img: Image.Image,
    mask: np.ndarray,
    width: int = 1,
    class_dct: dict = {},
    colors: dict = {}
):
    mask_arr = mask.astype(np.uint8)

    vectorized_map = np.vectorize(lambda x: class_dct.get(x, 0))
    mask_arr = vectorized_map(mask_arr)

    classes_ids = np.unique(list(class_dct.values()))
    highlighted_img = img.convert('RGB')

    for class_idx in classes_ids:
        mask_i = (mask_arr == class_idx)
        dilated = binary_dilation(mask_i, iterations=width)
        boundary = np.logical_and(dilated, ~mask_i)
        
        if np.any(boundary):
            boundary_mask = Image.fromarray((boundary * 255).astype(np.uint8), mode='L')
            color_layer = Image.new('RGB', img.size, color=colors[class_idx])
            highlighted_img.paste(color_layer, box=(0,0), mask=boundary_mask)

    return highlighted_img