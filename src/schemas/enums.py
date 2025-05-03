from enum import Enum

class CloudinaryCropEnum(str, Enum):
    scale="scale"
    fit="fit"
    fill="fill"
    thumb="thumb"

class CloudinaryEffectEnum(Enum):
    blur = "blur"
    pixelate = "pixelate"
    oil_paint = "oil_paint"
    brightness = "brightness"
    contrast = "contrast"
    saturation = "saturation"
    hue = "hue"
    gamma = "gamma"
    sharpen = "sharpen"
    vignette = "vignette"

class CloudinaryQualityEnum(Enum):
    auto = "auto"
    auto_best = "auto:best"
    auto_good = "auto:good"
    auto_eco = "auto:eco"
    auto_low = "auto:low"

class CloudinaryFormatEnum(str, Enum):
    auto = "auto"
    jpg = "jpg"
    png = "png"
    webp = "webp"
    avif = "avif"
    gif = "gif"
    bmp = "bmp"
    tiff = "tiff"
    ico = "ico"