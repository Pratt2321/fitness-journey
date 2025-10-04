"""
My Gym Journey — Through Amazon Orders
A Streamlit web app for visualizing fitness evolution through Amazon purchase data.

Author: Pratham Pradhan
Tech Stack: Streamlit, pandas, Amazon PA-API v5, matplotlib/plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import os
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Import our custom Rainforest API helper
try:
    from rainforest_api import RainforestAPI
except ImportError:
    st.warning("⚠️ Rainforest API helper not found. Product images will use placeholders.")
    RainforestAPI = None

# Page configuration
st.set_page_config(
    page_title="My Gym Journey — Through Amazon Orders",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS for portfolio-ready design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card styling */
    .product-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #e5e7eb;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .product-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .product-price {
        font-size: 1.2rem;
        font-weight: 700;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    
    .product-date {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    
    .product-note {
        background: #f9fafb;
        padding: 0.75rem;
        border-radius: 6px;
        border-left: 3px solid #3b82f6;
        font-size: 0.9rem;
        color: #374151;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #d1d5db;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Filter styling */
    .filter-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Responsive grid */
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .product-grid {
            grid-template-columns: 1fr;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data(file_path: str) -> pd.DataFrame:
    """Load and process the Amazon order history CSV file."""
    try:
        df = pd.read_csv(file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Convert order date to datetime
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        
        # Extract year for filtering
        df['year'] = df['order_date'].dt.year
        
        # Clean price data
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['total_owed'] = pd.to_numeric(df['total_owed'], errors='coerce')
        
        # Filter out cancelled orders
        df = df[df['order_status'] == 'Closed']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def is_gym_related(product_name: str) -> bool:
    """Check if a product is part of Pratham's specific fitness journey."""
    if pd.isna(product_name):
        return False
    
    # Pratham's specific fitness journey items (2022-2025)
    journey_items = [
        # 2022 - Foundation
        'airpods pro', 'teclor push up bar',
        
        # 2023 - Building Strength
        'grip strength', 'headband', 'gshock', 'g-shock',
        
        # 2024 - Equipment & Recovery
        'replacement ear tips', 'polislime', 'anti slip soft ear tips', 'noise reduction hole', 'silicone eartips', 'elbow brace', 'dip belt', 'ninja fit compact personal blender', 'body fat scale', 'scale',
        
        # 2025 - Nutrition & Training
        'orgain', 'pure protein bars', 'creatine', 'rxbar', 'rx bar',
        'wrist wraps', 'knee sleeves'
    ]
    
    product_lower = product_name.lower()
    return any(item in product_lower for item in journey_items)

def get_journey_stage(product_name: str, order_date: pd.Timestamp) -> str:
    """Determine which stage of the fitness journey this product represents."""
    if pd.isna(product_name) or pd.isna(order_date):
        return "Unknown"
    
    product_lower = product_name.lower()
    year = order_date.year
    
    # Use the actual purchase year to determine the stage
    if year == 2022:
        return "🏗️ Foundation (2022)"
    elif year == 2023:
        return "💪 Building Strength (2023)"
    elif year == 2024:
        return "🛠️ Equipment & Recovery (2024)"
    elif year == 2025:
        return "🥤 Nutrition & Training (2025)"
    else:
        return f"Fitness Journey ({year})"

def get_journey_stage_color(stage: str) -> str:
    """Get color for each journey stage."""
    if "2022" in stage:
        return "#3B82F6"  # Blue
    elif "2023" in stage:
        return "#10B981"  # Green
    elif "2024" in stage:
        return "#F59E0B"  # Yellow/Orange
    elif "2025" in stage:
        return "#EF4444"  # Red
    else:
        return "#6B7280"  # Gray

@st.cache_data
def filter_gym_products(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the dataframe to only include Pratham's fitness journey products."""
    if df.empty:
        return df
    
    # Apply journey filter
    journey_mask = df['product_name'].apply(is_gym_related)
    journey_df = df[journey_mask].copy()
    
    # Remove cancelled/zero value items
    journey_df = journey_df[
        (journey_df['total_owed'] > 0) & 
        (journey_df['order_status'] == 'Closed')
    ].copy()
    
    # Add journey stage
    journey_df['journey_stage'] = journey_df.apply(
        lambda row: get_journey_stage(row['product_name'], row['order_date']), axis=1
    )
    
    # Sort by order date (oldest first to show progression)
    journey_df = journey_df.sort_values('order_date', ascending=True)
    
    # Remove duplicates - keep only the first purchase of each item type
    journey_df['item_type'] = journey_df['product_name'].str.lower()
    
    # Define item types for deduplication (order matters - more specific first)
    item_types = {
        'replacement ear tips': 'airpods ear tips',
        'polislime': 'airpods ear tips',
        'anti slip soft ear tips': 'airpods ear tips',
        'noise reduction hole': 'airpods ear tips',
        'silicone eartips': 'airpods ear tips',
        'airpods pro': 'airpods pro',
        'teclor push up bar': 'teclor push up bar',
        'grip strength': 'grip strengthener',
        'headband': 'headband',
        'gshock': 'g-shock',
        'g-shock': 'g-shock',
        'elbow brace': 'elbow brace',
        'dip belt': 'dip belt',
        'ninja fit compact personal blender': 'ninja blender',
        'body fat scale': 'body fat scale',
        'scale': 'body fat scale',
        'orgain': 'orgain protein powder',
        'pure protein bars': 'pure protein bars',
        'creatine': 'creatine',
        'rxbar': 'rxbar',
        'rx bar': 'rxbar',
        'wrist wraps': 'wrist wraps',
        'knee sleeves': 'knee sleeves'
    }
    
    # Map each product to its item type
    def get_item_type(product_name):
        product_lower = product_name.lower()
        for keyword, item_type in item_types.items():
            if keyword in product_lower:
                return item_type
        return product_name.lower()
    
    journey_df['item_type'] = journey_df['product_name'].apply(get_item_type)
    
    # Keep only the first purchase of each item type (sorted by date)
    journey_df = journey_df.sort_values('order_date', ascending=True)
    journey_df = journey_df.drop_duplicates(subset=['item_type'], keep='first')
    
    # Sort by order date (oldest first to show progression)
    journey_df = journey_df.sort_values('order_date', ascending=True)
    
    return journey_df

def create_product_card(product: pd.Series, image_cache: Dict[str, str] = None, 
                       product_notes: Dict[str, str] = None) -> str:
    """Create HTML for a product card."""
    # Get product image from cache
    image_url = None
    if image_cache and not pd.isna(product.get('asin')):
        image_url = image_cache.get(product['asin'])
    
    if not image_url:
        # Use placeholder image
        product_name_clean = str(product['product_name'])[:20].replace('"', '').replace("'", '')
        image_url = f"https://via.placeholder.com/300x200/667eea/ffffff?text={product_name_clean}..."
    
    # Format price
    price = product.get('total_owed', product.get('unit_price', 0))
    if pd.isna(price):
        price = 0
    
    # Format date
    order_date = product.get('order_date')
    if pd.notna(order_date):
        if isinstance(order_date, str):
            order_date = pd.to_datetime(order_date)
        date_str = order_date.strftime('%B %d, %Y')
    else:
        date_str = "Unknown Date"
    
    # Get product note
    product_id = f"{product.get('asin', '')}_{product.get('order_date', '')}"
    note = product_notes.get(product_id, "") if product_notes else ""
    note_display = note if note else "Click to add your reflection on this purchase..."
    
    # Get journey stage and color
    journey_stage = product.get('journey_stage', 'Fitness Journey')
    stage_color = get_journey_stage_color(journey_stage)
    
    # Create card HTML
    card_html = f"""
    <div class="product-card">
        <div style="background: {stage_color}; color: white; padding: 0.5rem; border-radius: 8px 8px 0 0; font-size: 0.9rem; font-weight: 600; text-align: center; margin: -1.5rem -1.5rem 1rem -1.5rem;">
            {journey_stage}
        </div>
        <img src="{image_url}" alt="{product['product_name']}" class="product-image" 
             onerror="this.src='https://via.placeholder.com/300x200/f3f4f6/6b7280?text=Image+Not+Available'">
        <div class="product-title">{product['product_name']}</div>
        <div class="product-price">${price:.2f}</div>
        <div class="product-date">📅 {date_str}</div>
        <div class="product-note">
            <strong>💭 My Reflection:</strong> {note_display}
        </div>
    </div>
    """
    
    return card_html

def create_analytics_charts(df: pd.DataFrame) -> None:
    """Create analytics charts for the gym products."""
    if df.empty:
        st.warning("No gym products found to analyze.")
        return
    
    # Spending over time
    st.subheader("📈 Spending Over Time")
    
    # Group by month and year
    df['month_year'] = df['order_date'].dt.to_period('M')
    monthly_spending = df.groupby('month_year')['total_owed'].sum().reset_index()
    monthly_spending['month_year_str'] = monthly_spending['month_year'].astype(str)
    
    fig_spending = px.line(
        monthly_spending, 
        x='month_year_str', 
        y='total_owed',
        title="Monthly Gym Spending",
        labels={'total_owed': 'Total Spent ($)', 'month_year_str': 'Month'}
    )
    fig_spending.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_spending, use_container_width=True)
    
    # Product categories (word cloud simulation)
    st.subheader("🏷️ Most Common Product Categories")
    
    # Extract categories from product names
    all_words = []
    for product_name in df['product_name'].dropna():
        words = re.findall(r'\b\w+\b', product_name.lower())
        # Filter out common words and keep only relevant ones
        relevant_words = [w for w in words if len(w) > 3 and w not in ['the', 'and', 'for', 'with', 'from', 'this', 'that', 'your', 'will', 'can', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'does', 'did', 'do', 'am', 'is', 'be', 'by', 'on', 'in', 'at', 'to', 'of', 'a', 'an']]
        all_words.extend(relevant_words)
    
    if all_words:
        word_counts = pd.Series(all_words).value_counts().head(20)
        
        fig_categories = px.bar(
            x=word_counts.values,
            y=word_counts.index,
            orientation='h',
            title="Most Common Words in Product Names",
            labels={'x': 'Frequency', 'y': 'Word'}
        )
        fig_categories.update_layout(height=500)
        st.plotly_chart(fig_categories, use_container_width=True)
    
    # Spending by year
    st.subheader("📊 Annual Spending Breakdown")
    
    yearly_spending = df.groupby('year')['total_owed'].sum().reset_index()
    
    fig_yearly = px.bar(
        yearly_spending,
        x='year',
        y='total_owed',
        title="Total Gym Spending by Year",
        labels={'total_owed': 'Total Spent ($)', 'year': 'Year'},
        color='total_owed',
        color_continuous_scale='Blues'
    )
    fig_yearly.update_layout(height=400)
    st.plotly_chart(fig_yearly, use_container_width=True)

import json
import os

def load_product_notes() -> Dict[str, str]:
    """Load product notes from JSON file or return empty dict."""
    notes_file = 'product_notes.json'
    try:
        if os.path.exists(notes_file):
            with open(notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading notes: {e}")
    return {}

def save_product_note(product_id: str, note: str) -> None:
    """Save a product note to JSON file."""
    notes_file = 'product_notes.json'
    try:
        # Load existing notes
        notes = load_product_notes()
        
        # Update the specific note
        notes[product_id] = note
        
        # Save back to file
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        st.error(f"Error saving note: {e}")

# Note editing is now always available - you can edit product_notes.json directly

@st.cache_data
def filter_products(df: pd.DataFrame, search_term: str, year_range: tuple) -> pd.DataFrame:
    """Cached function to filter products by search term and year range."""
    if search_term:
        mask = df['product_name'].str.contains(search_term, case=False, na=False)
        filtered = df[mask]
    else:
        filtered = df
    
    # Apply year filter
    filtered = filtered[
        (filtered['year'] >= year_range[0]) & 
        (filtered['year'] <= year_range[1])
    ]
    
    return filtered

def main():
    """Main Streamlit application."""
    
    # Notes are now stored in product_notes.json file
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💪 My Fitness Journey — Through Amazon Orders</h1>
        <p>From AirPods Pro to Creatine: 4 Years of Transformation (2022-2025)</p>
        <p style="font-size: 1rem; opacity: 0.8; margin-top: 1rem;">15 key purchases that tell the story of my fitness evolution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    csv_file = "Retail.OrderHistory.1.csv"
    if not os.path.exists(csv_file):
        st.error(f"❌ CSV file '{csv_file}' not found. Please ensure the file is in the project root.")
        return
    
    with st.spinner("🔄 Loading and processing data..."):
        df = load_and_process_data(csv_file)
    
    if df.empty:
        st.error("❌ No data loaded. Please check your CSV file.")
        return
    
    # Filter gym products
    gym_df = filter_gym_products(df)
    
    if gym_df.empty:
        st.warning("🏃‍♂️ No gym-related products found in your order history. Try adjusting the keyword filters.")
        return
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 Filters")
    
    # Year range filter
    min_year = int(gym_df['year'].min()) if not gym_df.empty else 2022
    max_year = int(gym_df['year'].max()) if not gym_df.empty else 2025
    
    year_range = st.sidebar.slider(
        "📅 Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Search filter (auto-search as you type)
    st.sidebar.markdown("🔍 **Search Products**")
    
    # Add CSS to hide the "Press Enter to apply" text
    st.markdown("""
    <style>
    .stTextInput > div > div > div > div > small,
    .stTextInput small,
    [data-testid="stTextInput"] small {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    search_term = st.sidebar.text_input(
        "Search Products", 
        placeholder="Enter product name...", 
        key="search_input",
        help="Search automatically as you type",
        label_visibility="collapsed"
    )
    
    # Apply filters using cached function for better performance
    filtered_df = filter_products(gym_df, search_term, year_range)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(filtered_df)}</div>
            <div class="stat-label">Total Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_spent = filtered_df['total_owed'].sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${total_spent:.0f}</div>
            <div class="stat-label">Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = filtered_df['total_owed'].mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${avg_price:.0f}</div>
            <div class="stat-label">Avg Price</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        unique_products = filtered_df['product_name'].nunique()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{unique_products}</div>
            <div class="stat-label">Unique Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2 = st.tabs(["🛍️ My Fitness Journey Timeline", "📊 Analytics"])
    
    with tab1:
        if filtered_df.empty:
            st.info("No products match your current filters. Try adjusting the year range or search term.")
        else:
            # Journey progression overview
            st.markdown("### 🗺️ Journey Overview")
            
            # Group by journey stage
            journey_stages = filtered_df.groupby('journey_stage').size().reset_index(name='count')
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Define the 4 journey stages in order
            stages = [
                "🏗️ Foundation (2022)",
                "💪 Building Strength (2023)", 
                "🛠️ Equipment & Recovery (2024)",
                "🥤 Nutrition & Training (2025)"
            ]
            
            for i, stage in enumerate(stages):
                with [col1, col2, col3, col4][i]:
                    # Get count for this stage from the data
                    count = journey_stages[journey_stages['journey_stage'] == stage]['count'].iloc[0] if stage in journey_stages['journey_stage'].values else 0
                    stage_color = get_journey_stage_color(stage)
                    st.markdown(f"""
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid {stage_color}; margin-bottom: 1rem;">
                        <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{stage}</h4>
                        <p style="margin: 0.5rem 0 0 0; font-weight: 600; color: {stage_color};">{count} items</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            # Initialize Rainforest API if available
            rainforest_api = None
            image_cache = {}
            if RainforestAPI:
                try:
                    rainforest_api = RainforestAPI()
                    # Pre-load all images in batch for better performance
                    asins = [row.get('asin') for _, row in filtered_df.iterrows() if not pd.isna(row.get('asin'))]
                    if asins:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("🖼️ Loading product images...")
                        image_cache = rainforest_api.get_multiple_product_images(asins)
                        
                        progress_bar.progress(1.0)
                        status_text.text("✅ Images loaded!")
                        
                        # Clear the progress indicators after a short delay
                        import time
                        time.sleep(0.5)
                        progress_bar.empty()
                        status_text.empty()
                except:
                    st.warning("⚠️ Rainforest API not configured. Using placeholder images.")
            
            # Load product notes
            product_notes = load_product_notes()
            
            # Note editing is always available
            
            # Create product cards
            st.markdown('<div class="product-grid">', unsafe_allow_html=True)
            
            for idx, product in filtered_df.iterrows():
                card_html = create_product_card(product, image_cache, product_notes)
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Notes are managed via product_notes.json file
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        create_analytics_charts(filtered_df)
    
    

if __name__ == "__main__":
    main()
