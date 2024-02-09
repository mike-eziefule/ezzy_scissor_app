import pyqrcode
import png
from fastapi import HTTPException

class qr_image():
    def __init__(self) -> None:
        pass
    def url_to_qr(self, url, img_path, url_key):
        try:
            pyqrcode.create(url).png(
                file=img_path + url_key +'.png', 
                scale = 6, 
                module_color="#051d45"
            )
        
        except Exception as e:
            raise HTTPException(status_code = 500, detail = str(e))