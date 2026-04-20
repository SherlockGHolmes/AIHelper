from PIL import Image, ImageDraw
import pystray as stray
import sys
from shared import task_queue


def create_image():
    """Létrehoz egy egyszerű színes négyzetet ikonként."""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='blue')
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill='white')
    return image

def on_action(icon, item):
    if str(item) == "Exit":
        print("Kilépés...")
        icon.stop()
        sys.exit(0)
    else:
        print(f"{item} kiválasztva")
        task_queue.put("open")

        

menu = stray.Menu(
    stray.MenuItem("Settings", on_action),
    stray.MenuItem("Exit", on_action)
)
icon = stray.Icon("Kompetenciamérés", create_image(), menu=menu)

if __name__ == "__main__":
    icon.run()