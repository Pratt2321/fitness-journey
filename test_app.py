"""
Test script for the My Gym Journey Streamlit app.
Verifies data processing, curated dataset schema, local images, and fallback handling.
"""

import os
import json
from app import (
    load_and_process_data, 
    filter_gym_products, 
    is_gym_related,
    load_curated_dataset,
    get_product_image_src
)

def test_data_loading():
    """Test if the CSV file can be loaded and processed."""
    print("Testing data loading...")
    
    csv_file = "Retail.OrderHistory.1.csv"
    if not os.path.exists(csv_file):
        print(f"ERROR: CSV file '{csv_file}' not found!")
        return False
    
    df = load_and_process_data(csv_file)
    if df.empty:
        print("ERROR: No data loaded!")
        return False
    
    print(f"SUCCESS: Data loaded successfully: {len(df)} rows")
    return True

def test_gym_filtering():
    """Test the gym product filtering logic."""
    print("Testing gym product filtering...")
    
    test_products = [
        "RXBAR Protein Bars, Protein Snack, Snack Bars, Variety Pack",
        "Orgain Organic Vegan Protein Powder, Vanilla Bean",
        "AEOLOS Knee Sleeves (1 Pair), 7mm Compression Knee Braces",
        "Gymreapers Weightlifting Wrist Wraps",
        "Random Non-Gym Product",
        "Dove Body Wash with Pump 3 Count"
    ]
    
    gym_products = [p for p in test_products if is_gym_related(p)]
    non_gym_products = [p for p in test_products if not is_gym_related(p)]
    
    print(f"SUCCESS: Gym products detected: {len(gym_products)}")
    print(f"SUCCESS: Non-gym products filtered: {len(non_gym_products)}")
    
    return len(gym_products) > 0

def test_full_pipeline():
    """Test the complete data processing pipeline."""
    print("Testing complete pipeline...")
    
    csv_file = "Retail.OrderHistory.1.csv"
    if not os.path.exists(csv_file):
        print(f"ERROR: CSV file '{csv_file}' not found!")
        return False
    
    df = load_and_process_data(csv_file)
    if df.empty:
        print("ERROR: No data loaded!")
        return False
    
    gym_df = filter_gym_products(df)
    if gym_df.empty:
        print("ERROR: No gym products found!")
        return False
    
    print(f"SUCCESS: Pipeline successful: {len(gym_df)} gym products found")
    print(f"SUCCESS: Date range: {gym_df['order_date'].min()} to {gym_df['order_date'].max()}")
    print(f"SUCCESS: Total spent: ${gym_df['total_owed'].sum():.2f}")
    
    return True

def test_curated_dataset():
    """Test that curated dataset loads with all required schema fields and reflections."""
    print("Testing curated dataset schema & reflections...")
    items = load_curated_dataset()
    if not items or len(items) != 16:
        print(f"ERROR: Expected 16 items, got {len(items) if items else 0}")
        return False

    required_keys = ["id", "product_name", "purchase_date", "year", "category", "price", "asin", "image_path", "reflection"]
    for idx, item in enumerate(items):
        for k in required_keys:
            if k not in item:
                print(f"ERROR: Item {idx} missing key '{k}'")
                return False
        if not item["reflection"].strip():
            print(f"ERROR: Item {item['id']} has empty reflection")
            return False

    print(f"SUCCESS: Curated dataset has all 16 items with complete schema and reflections")
    return True

def test_local_images():
    """Test that all local product images exist and have valid file sizes."""
    print("Testing local image assets...")
    items = load_curated_dataset()
    for item in items:
        path = item.get("image_path", "")
        if not os.path.exists(path):
            print(f"ERROR: Image file not found: {path} for {item.get('asin')}")
            return False
        if os.path.getsize(path) < 1000:
            print(f"ERROR: Image file too small (< 1KB): {path}")
            return False
        
        # Test encoding
        src = get_product_image_src(path, item.get("product_name", ""))
        if not src.startswith("data:image/"):
            print(f"ERROR: Expected data URI for {path}, got {src[:30]}")
            return False

    print(f"SUCCESS: All {len(items)} local image assets exist and encode cleanly")
    return True

def test_missing_image_fallback():
    """Test that missing images gracefully return an SVG data URI instead of crashing."""
    print("Testing missing image fallback resilience...")
    src = get_product_image_src("non_existent_file.jpg", "Test Dumbbell")
    if not src.startswith("data:image/svg+xml"):
        print(f"ERROR: Expected SVG placeholder for missing file, got {src[:30]}")
        return False
    print("SUCCESS: Missing image gracefully rendered as clean SVG placeholder")
    return True

def main():
    """Run all tests."""
    print("Starting My Gym Journey App Tests\n")
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Gym Filtering", test_gym_filtering),
        ("Full Pipeline", test_full_pipeline),
        ("Curated Dataset", test_curated_dataset),
        ("Local Image Assets", test_local_images),
        ("Missing Image Fallback", test_missing_image_fallback)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"SUCCESS: {test_name} PASSED")
            else:
                print(f"ERROR: {test_name} FAILED")
        except Exception as e:
            print(f"ERROR: {test_name} ERROR: {str(e)}")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The app is ready to run.")
        print("\nTo start the app, run:")
        print("streamlit run app.py")
    else:
        print("Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main()
