if __name__ == '__main__':
    # Testing imports
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devision.settings')
    django.setup()

    from gui.src import predictions    
    from PIL import Image, ImageDraw
    from matplotlib import pyplot as plt
    
    img = Image.new('RGB', color=(0, 0, 0), size=predictions.IMAGE_RESOLUTION)
    canvas = ImageDraw.Draw(img)
    BLUE = (0, 0, 255)
    canvas.circle(xy=(500, 500), radius=30, fill=BLUE, width=4)
    
    plt.imshow(img)
    plt.show()