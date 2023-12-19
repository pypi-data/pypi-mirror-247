import time

from pycudwt import Wavelets
import numpy as np
from PIL import Image

from imwatermark import WatermarkEncoder

np.random.seed(42)

METHOD_DWT_DCT = 'dwtDct'
WATERMARK_MESSAGE = 0b101100111110110010010000011110111011000110011110
WATERMARK_BITS = [int(bit) for bit in bin(WATERMARK_MESSAGE)[2:]]

# warmup GPU
Wavelets(np.random.randint(low=0, high=255, size=(1024, 1024), dtype=np.uint8), "haar", 1)
WatermarkEncoder().warmup_gpu()


class TestWavelets:
    def test_fast_watermarking(self):
        """
        Ensure our GPU warmup worked correctly. Otherwise first request every time will
        take around 2 seconds to load CUDA libraries, which is too long.
        """
        start = time.time()
        wm = WatermarkEncoder()
        image_rgb = np.random.randint(low=0, high=255, size=(1024, 1024, 3), dtype=np.uint8)
        wm.set_watermark("bits", WATERMARK_BITS)
        image_bgr = np.array(image_rgb)[:, :, ::-1]
        watermarked_bgr = wm.encode(image_bgr, METHOD_DWT_DCT)
        watermarked_rgb = Image.fromarray(watermarked_bgr[:, :, ::-1])
        elapsed_ms = (time.time() - start) * 1000.

        # if it doesn't work, it will take around 2000ms, in my testing on A100s
        # if it works, should take ~50ms
        ENCODING_TOO_LONG_MS = 65
        assert elapsed_ms <= ENCODING_TOO_LONG_MS, f"Watermarking took {elapsed_ms:.2f} ms, which is too long"

    def test_pycudwt_installed_correctly(self):
        """
        If pycudwt is install incorrectly, the DWT transform will return all zeros.
        """
        # create wavelets information and plug in random data
        start = time.time()
        wv = Wavelets(np.random.randint(low=0, high=255, size=(1024, 1024), dtype=np.uint8), "haar", 1)

        # perform the discrete wavelets transform
        wv.forward()  # wv.coeffs = [A, [H1, V1, D1]]
        NON_ZERO_THRESH_SUM = 1.0
        assert np.sum(np.abs(wv.coeffs[0])) > NON_ZERO_THRESH_SUM, \
            "pycudwt is returning all zeros, did you `export PYCUDWT_CC=80` before running `pip install`?"
        
        elapsed_ms = (time.time() - start) * 1000.

        # if it works, should take <10ms! but let's put a 4x buffer for random CI machines :laugh:
        PYCUDWT_TOO_LONG_MS = 10 * 4
        assert elapsed_ms <= PYCUDWT_TOO_LONG_MS, f"pycudwt set_image() and forward() took {elapsed_ms:.2f} ms, which is too long"

