# loot_listener.py - DO NOT REMOVE THIS LINE FROM THE SCRIPT!!!

import io
import threading
import asyncio
import winsound
import mss
from PIL import Image  #type:ignore
from pynput import mouse, keyboard  #type:ignore

# Windows OCR imports
from winsdk.windows.media.ocr import OcrEngine
from winsdk.windows.graphics.imaging import BitmapDecoder
from winsdk.windows.storage.streams import InMemoryRandomAccessStream, DataWriter

# --- CONFIGURATION ---
KEYWORDS = ["level of all", "rarity of items found"]

# Massive capture area to ensure we don't miss PoE tooltips
CAPTURE_WIDTH = 1200
CAPTURE_HEIGHT = 800

# Set this to True to save 'debug_last_capture.png' to see what it's capturing!
SAVE_DEBUG_IMAGE = True
# ---------------------

ocr_engine = OcrEngine.try_create_from_user_profile_languages()
pressed_keys: set = set() # type annotation to satisfy mypy

async def extract_text(image_bytes: bytes) -> str:
    """Feeds the image to Windows 10/11 built-in OCR and returns text."""
    stream = InMemoryRandomAccessStream()
    writer = DataWriter(stream) # type: ignore

    writer.write_bytes(image_bytes)  #type:ignore
    await writer.store_async()
    stream.seek(0)

    decoder = await BitmapDecoder.create_async(stream) # type: ignore
    software_bitmap = await decoder.get_software_bitmap_async()

    # Check if ocr_engine initialized properly
    if ocr_engine is None:
        return ""

    result = await ocr_engine.recognize_async(software_bitmap) # type: ignore
    return result.text

def process_image(pil_img: Image.Image):
    """Runs OCR in the background so it doesn't freeze your mouse."""
    # Convert to grayscale to improve OCR speed
    pil_img = pil_img.convert("L")

    if SAVE_DEBUG_IMAGE:
        pil_img.save("debug_last_capture.png", format="PNG")

    # Convert to bytes
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    # Run the Async OCR function
    try:
        text = asyncio.run(extract_text(image_bytes))
    except Exception as e:
        print(f"OCR failed: {e}")
        return

    text_lower = text.lower()

    # 5. Check keywords
    found = False
    for keyword in KEYWORDS:
        if keyword in text_lower:
            print(f"💎 FOUND VALUABLE! '{keyword}'")
            found = True
            break

    if found:
        winsound.Beep(1500, 300)
    else:
        print("🗑️ Junk.")

def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

def on_click(x, y, button, pressed):
    # Trigger ONLY on mouse down
    if pressed and button == mouse.Button.right:
        if keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys:
            print(f"Scanning at X:{x} Y:{y}...")

            # --- INSTANT CAPTURE ---
            # We capture synchronously on the mouse thread before the game
            # can process the click and hide the tooltip!
            monitor = {
                "top": int(y - (CAPTURE_HEIGHT / 2)),
                "left": int(x - (CAPTURE_WIDTH / 2)),
                "width": CAPTURE_WIDTH,
                "height": CAPTURE_HEIGHT
            }

            try:
                with mss.MSS() as sct:
                    img = sct.grab(monitor)
                    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

                # Offload the slow OCR text reading to a background thread
                threading.Thread(target=process_image, args=(pil_img,), daemon=True).start()

            except Exception as e:
                print(f"Capture failed: {e}")

if __name__ == "__main__":
    if not ocr_engine:
        print("Error: Windows OCR engine could not be created.")
        exit(1)

    print("🚀 Loot Scanner Started!")
    print(f"Keywords: {', '.join(KEYWORDS)}")
    print("Hold CTRL + Left Click on an item to scan.")

    # Start keyboard listener
    k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    k_listener.start()

    # Start mouse listener
    with mouse.Listener(on_click=on_click) as m_listener: # type: ignore
        m_listener.join()