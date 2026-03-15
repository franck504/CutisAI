from bing_image_downloader import downloader
import os

downloader.download("Buruli ulcer lesion", limit=10, output_dir="test_bing", adult_filter_off=False, force_replace=False, timeout=60, verbose=False)
print("Files:", os.listdir("test_bing/Buruli ulcer lesion"))
