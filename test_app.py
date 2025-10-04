"""
Test script for the My Gym Journey Streamlit app.
Run this to verify the app works correctly before deployment.
"""

import pandas as pd
import os
from app import load_and_process_data, filter_gym_products, is_gym_related

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
    
    # Test individual product names
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
    
    # Load and process data
    df = load_and_process_data(csv_file)
    if df.empty:
        print("ERROR: No data loaded!")
        return False
    
    # Filter gym products
    gym_df = filter_gym_products(df)
    if gym_df.empty:
        print("ERROR: No gym products found!")
        return False
    
    print(f"SUCCESS: Pipeline successful: {len(gym_df)} gym products found")
    print(f"SUCCESS: Date range: {gym_df['order_date'].min()} to {gym_df['order_date'].max()}")
    print(f"SUCCESS: Total spent: ${gym_df['total_owed'].sum():.2f}")
    
    return True

def main():
    """Run all tests."""
    print("Starting My Gym Journey App Tests\n")
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Gym Filtering", test_gym_filtering),
        ("Full Pipeline", test_full_pipeline)
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
