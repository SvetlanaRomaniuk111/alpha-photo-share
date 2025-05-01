import cloudinary.utils
import cloudinary.uploader
import qrcode
from PIL import Image 
import uuid
import os


def transform_image(image_url: str, transformation: dict):
    return cloudinary.utils.cloudinary_url(str(image_url), **transformation)  

def generate_qr(image_url):
    qr = qrcode.make(image_url)
    with open("qrcode.png", "wb") as f:
        qr.save(f)
    return qr
