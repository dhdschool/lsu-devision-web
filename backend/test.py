if __name__ == '__main__':
    # Testing imports
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devision.settings')
    django.setup()

    from gui.src import predictions    
    from PIL import Image, ImageDraw
    from matplotlib import pyplot as plt
    import numpy as np
    
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    
    outline = Image.new('RGB', color=(0, 0, 0), size=predictions.IMAGE_RESOLUTION)
    outline_draw = ImageDraw.Draw(outline)
    outline_draw.circle(xy=(500, 1000), radius=200, outline=BLUE, width=30)
    
    outline_mask = Image.new('L', color=0, size=predictions.IMAGE_RESOLUTION)
    outline_mask_draw = ImageDraw.Draw(outline_mask)
    outline_mask_draw.circle(xy=(500, 1000), radius=200, outline=1, width=30)
    
    fill = Image.new('RGB', color=(0, 0, 0), size=predictions.IMAGE_RESOLUTION)
    fill_draw = ImageDraw.Draw(fill)
    fill_draw.circle(xy=(500, 1000), radius=200, fill=RED, width=30)
    
    fill_draw.circle(xy=(1000, 1500), radius=200, fill=RED, width=30)
    outline_draw.circle(xy=(1000, 1500), radius=200, fill=GREEN, width=30)
    outline_mask_draw.circle(xy=(1000, 1500), radius=200, outline=2, width=30)
    
    fill_draw.circle(xy=(1000, 500), radius=200, fill=RED, width=30)
    outline_draw.circle(xy=(1000, 500), radius=200, outline=BLUE, width=30)
    outline_mask_draw.circle(xy=(1000, 500), radius=200, outline=1, width=30)

    
    mask = np.asarray(outline_mask, dtype=np.uint8)
    
    class_dct = {1:1,
                 2:2,
                 3:1} # Object instance: Class instance
    
    color_dct = {1:BLUE,
                 2:GREEN} # Class instance: Highlight color
    
    model = predictions.StardistWrapper('xenopus-4-class')
    with Image.open('test-image.jpg') as test_image:
        counts, out = model.predict(test_image)
        
    plt.imshow(out)
    plt.show()