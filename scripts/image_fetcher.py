"""
Image Fetcher Script for Fitness Journey Portfolio
Fetches authentic product images for curated fitness purchases and saves them locally.
This script is run ONCE offline; the Streamlit app consumes only the local assets.

Author: Pratham Pradhan
"""

import os
import requests
from typing import Dict

# Curated mapping of ASIN to authentic product image URLs
PRODUCT_IMAGE_URLS: Dict[str, str] = {
    # 2022 — Foundation
    "B09JQMJHXY": "https://cdsassets.apple.com/live/SZLF0YNV/images/sp/111861_airpods_pro_case__eqmrrx2cfpkm_large.png",
    "B09N77Z84N": "https://i.ebayimg.com/images/g/HVEAAOSwgCVoKmth/s-l500.jpg",

    # 2023 — Building Strength
    "B0838G23M1": "https://i.ebayimg.com/images/g/AMEAAOSwhcRnRzF0/s-l1200.png",
    "B00Z83DJVG": "https://underarmour.scene7.com/is/image/Underarmour/1276990-001_SLF_SL",
    "B07MZX5731": "https://shockbase.org/pics2/800/GBA-800/GBA-800UC-2A.png",

    # 2024 — Equipment & Recovery
    "B0CLY2HKW5": "https://c1.neweggimages.com/productimage/nb300/ACCUS2208030LYBJ92A.jpg",
    "B07V32CR9J": "https://cambivo.com/cdn/shop/products/cambivo-elbow-brace-for-tendonitis-and-tennis-elbow-with-gel-pad-and-dual-stabilizers-2-pack-arm-sleeves-for-women-men-458507.jpg",
    "B001P0S3XU": "https://target.scene7.com/is/image/Target/GUEST_32d9ea3a-50f6-4d39-8738-4db680dfcd90?wid=500&hei=500&fmt=pjpeg",
    "B01FHOWYA2": "https://images.thdstatic.com/productImages/ef04c2dd-555d-4351-a1e0-6f592d51d1bd/svn/black-ninja-countertop-blenders-qb3001ss-64_600.jpg",
    "B0BZ4JDMWM": "https://www.vivehealth.com/cdn/shop/files/1_Main_Image_ef13a74c-910d-4c20-92c5-61efced88ea8_700x700.jpg?v=1740772943",

    # 2025 — Nutrition & Training
    "B0CG127YXC": "https://i5.walmartimages.com/seo/Pure-Protein-Bars-Variety-Pack-1-76-Ounce-23-Count_b16e8a89-19dd-4e42-bc70-f0ad994becd2.a038edaacee2be043165216087365c56.jpeg",
    "B07PXNNFGT": "https://target.scene7.com/is/image/Target/GUEST_9ac3a542-4a89-43af-9628-2c84296ff981",
    "B00GL2HMES": "https://nutricost.com/cdn/shop/files/NTC_CreatineMonohydrate_Unflavored_500G_Front_SQUARE_98526928-e1cc-4ff6-9918-430654760159_1200x1200.jpg?v=1760650358",
    "B0143NQVI4": "https://shop.rxbar.com/media/catalog/product/cache/0e2b578320d64b0336db2c7c6d9aa85d/0/0/00193908003720_c1n1_f87raqj6lcku9dfe.jpeg",
    "B07BSV8CTK": "http://www.gymreapers.com/cdn/shop/files/wrist-wraps-green-main-2_c32e05c8-fcba-4261-bd73-25f045a923d3.jpg?v=1748554211&width=2048",
    "B072HJ4KW1": "https://www.gosupps.com/media/catalog/product/6/1/611qDdYHbtL.jpg"
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "products")

def download_images(output_dir: str = OUTPUT_DIR) -> Dict[str, str]:
    """Download images for all curated ASINs to local output directory."""
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Downloading {len(PRODUCT_IMAGE_URLS)} product images to '{output_dir}'...")
    
    for asin, url in PRODUCT_IMAGE_URLS.items():
        # Determine file extension based on URL
        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".jpeg" in url.lower():
            ext = ".jpg"

        dest_filename = f"{asin}{ext}"
        dest_path = os.path.join(output_dir, dest_filename)

        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
            print(f"  [OK] {asin} -> Already exists ({os.path.getsize(dest_path)} bytes)")
            results[asin] = os.path.relpath(dest_path)
            continue

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            
            # Verify it's actually an image
            content_type = resp.headers.get("Content-Type", "")
            if "image" not in content_type and len(resp.content) < 500:
                print(f"  [FAIL] {asin} -> Received non-image response ({content_type})")
                continue

            with open(dest_path, "wb") as f:
                f.write(resp.content)
            
            print(f"  [DOWNLOADED] {asin} -> {dest_filename} ({len(resp.content)} bytes)")
            results[asin] = os.path.relpath(dest_path)
        except Exception as e:
            print(f"  [ERROR] {asin} ({url}): {e}")

    print(f"\nFinished! {len(results)}/{len(PRODUCT_IMAGE_URLS)} images ready locally.")
    return results

if __name__ == "__main__":
    download_images()
