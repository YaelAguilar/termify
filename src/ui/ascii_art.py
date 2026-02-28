import os
import hashlib
import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from typing import List, Optional, Tuple


# Secuencias ANSI para color RGB verdadero (24-bit)
def _fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def _bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

RESET = "\033[0m"


class ASCIIArtConverter:
    """Convierte imágenes a arte en terminal usando half-blocks con color RGB."""
    
    CHAR_RATIO = 2.0
    
    def __init__(self, cache_dir: str = ".cache/album_covers"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, url: str) -> str:
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.png")
    
    def _download_image(self, url: str) -> Optional[Image.Image]:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception:
            return None
    
    def _get_cached_image(self, url: str) -> Optional[Image.Image]:
        cache_path = self._get_cache_path(url)
        
        if os.path.exists(cache_path):
            try:
                return Image.open(cache_path)
            except Exception:
                os.remove(cache_path)
        
        image = self._download_image(url)
        if image:
            try:
                image.save(cache_path, "PNG")
            except Exception:
                pass
        
        return image
    
    def _resize_image(self, image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        img_w, img_h = image.size
        aspect = img_w / img_h  # Ratio de la imagen original
        
        # Intentar ajustar por alto primero
        new_h_lines = max_height
        new_w = int(new_h_lines * self.CHAR_RATIO * aspect)
        
        # Si el ancho excede el máximo, ajustar por ancho
        if new_w > max_width:
            new_w = max_width
            new_h_lines = int(new_w / (self.CHAR_RATIO * aspect))
        
        # Convertir líneas de terminal a pixeles verticales (2 por línea)
        new_h_pixels = new_h_lines * 2
        
        new_w = max(1, new_w)
        new_h_pixels = max(2, new_h_pixels)
        
        # Asegurar altura par para los half-blocks
        if new_h_pixels % 2 != 0:
            new_h_pixels -= 1
        
        return image.resize((new_w, new_h_pixels), Image.Resampling.LANCZOS)
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        # Enfocar para recuperar bordes perdidos al escalar
        image = image.filter(ImageFilter.SHARPEN)
        
        # Aumentar contraste ligeramente (1.0 = sin cambio)
        image = ImageEnhance.Contrast(image).enhance(1.2)
        
        # Aumentar saturación para compensar que la terminal se ve más apagada
        image = ImageEnhance.Color(image).enhance(1.3)
        
        return image
    
    def convert(self, url: str, max_width: int, max_height: int) -> Optional[Tuple[int, List[str]]]:
        if not url:
            return None
        
        image = self._get_cached_image(url)
        if not image:
            return None
        
        # Convertir a RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Redimensionar (max_height en líneas de terminal)
        image = self._resize_image(image, max_width, max_height)
        
        # Postprocesado para mejorar calidad en terminal
        image = self._enhance_image(image)
        
        pixels = image.load()
        img_w, img_h = image.size
        
        lines = []
        # Procesar de a pares de filas
        for y in range(0, img_h - 1, 2):
            line = ""
            for x in range(img_w):
                # Pixel superior → foreground, pixel inferior → background
                r1, g1, b1 = pixels[x, y][:3]
                r2, g2, b2 = pixels[x, y + 1][:3]
                line += _fg(r1, g1, b1) + _bg(r2, g2, b2) + "▀"
            line += RESET
            lines.append(line)
        
        return (img_w, lines)
