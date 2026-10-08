"""
From AirPods Pro to Creatine: 4 Years of Transformation (2022–2025)
An Editorial Fitness Journey Case Study

Author: Pratham Pradhan (prathampradhan.dev)
Tech Stack: Streamlit, Pandas, Local Image Pipeline
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import base64
import urllib.parse
from typing import List, Dict, Optional

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="From Calisthenics to Heavy Lifts: My 4-Year Fitness Progression",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# Editorial Design System & Styling
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap');

    /* Global Dark Canvas */
    .stApp {
        background-color: #080b11;
        color: #e2e8f0;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Completely hide Streamlit sidebar and extra margins */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    header[data-testid="stHeader"] {
        background: transparent;
    }

    .main .block-container {
        max-width: 1040px;
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin: 0 auto;
    }

    /* Editorial Hero Section */
    .editorial-hero {
        padding: 3.5rem 0 3rem 0;
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 3.5rem;
    }

    .hero-kicker {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #38bdf8;
        margin-bottom: 1.25rem;
    }

    .editorial-hero h1 {
        font-size: clamp(2.4rem, 5vw, 3.8rem);
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.035em;
        line-height: 1.15;
        margin: 0 0 1.25rem 0;
    }

    .editorial-hero p.narrative-lead {
        font-size: clamp(1.05rem, 1.8vw, 1.25rem);
        color: #94a3b8;
        max-width: 760px;
        margin: 0 auto 1.75rem auto;
        line-height: 1.7;
        font-weight: 400;
    }

    .hero-byline {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        font-size: 0.9rem;
        color: #64748b;
    }

    .hero-byline a {
        color: #cbd5e1;
        text-decoration: none;
        font-weight: 500;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 1px;
        transition: all 0.15s ease;
    }

    .hero-byline a:hover {
        color: #38bdf8;
        border-bottom-color: #38bdf8;
    }

    /* Chapter Section Styling */
    .chapter-container {
        margin: 4.5rem 0 2rem 0;
    }

    .chapter-meta {
        display: flex;
        align-items: baseline;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }

    .chapter-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        color: #38bdf8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .chapter-heading {
        font-size: 2rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.025em;
        margin: 0 0 0.5rem 0;
    }

    .chapter-theme {
        font-size: 1.05rem;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    .chapter-essay {
        font-size: 1.02rem;
        color: #cbd5e1;
        line-height: 1.75;
        max-width: 860px;
        margin-bottom: 2.25rem;
    }

    /* Product Card Editorial Grid */
    .product-grid-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.75rem;
        margin-bottom: 2.5rem;
    }

    .editorial-card {
        background: #0e131f;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }

    .editorial-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 255, 255, 0.18);
        box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.6);
    }

    .editorial-card a.img-link {
        display: block;
        text-decoration: none;
        width: 100%;
        margin-bottom: 1.25rem;
    }

    .editorial-card .img-frame {
        width: 100%;
        height: 210px;
        background: #07090f;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.25rem;
        overflow: hidden;
    }

    .editorial-card .img-frame img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.5));
        transition: transform 0.3s ease;
    }

    .editorial-card:hover .img-frame img {
        transform: scale(1.04);
    }

    .editorial-card a.title-link {
        font-size: 1.12rem;
        font-weight: 700;
        color: #f8fafc;
        text-decoration: none;
        line-height: 1.4;
        margin: 0 0 0.4rem 0;
        display: inline-block;
        transition: color 0.15s ease;
    }

    .editorial-card a.title-link:hover {
        color: #38bdf8;
    }

    .card-date {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #64748b;
        margin-bottom: 1.1rem;
    }

    .card-reflection-block {
        margin-top: auto;
        background: rgba(15, 23, 42, 0.6);
        border-left: 2px solid #38bdf8;
        padding: 0.9rem 1rem;
        border-radius: 0 8px 8px 0;
        font-family: 'Newsreader', Georgia, serif;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #cbd5e1;
        font-style: italic;
    }

    /* Chapter Accents */
    .c-2022 .chapter-number, .c-2022 a.title-link:hover { color: #38bdf8; }
    .c-2022 .card-reflection-block { border-left-color: #38bdf8; }

    .c-2023 .chapter-number, .c-2023 a.title-link:hover { color: #34d399; }
    .c-2023 .card-reflection-block { border-left-color: #34d399; }

    .c-2024 .chapter-number, .c-2024 a.title-link:hover { color: #fbbf24; }
    .c-2024 .card-reflection-block { border-left-color: #fbbf24; }

    .c-2025 .chapter-number, .c-2025 a.title-link:hover { color: #fb7185; }
    .c-2025 .card-reflection-block { border-left-color: #fb7185; }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# Backward-Compatible Data Processing Functions
# (Kept intact for test_app.py and raw CSV compatibility)
# ==============================================================================
@st.cache_data
def load_and_process_data(file_path: str) -> pd.DataFrame:
    """Load and process the Amazon order history CSV file."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['year'] = df['order_date'].dt.year
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['total_owed'] = pd.to_numeric(df['total_owed'], errors='coerce')
        df = df[df['order_status'] == 'Closed']
        return df
    except Exception as e:
        st.error(f"Error loading CSV data: {str(e)}")
        return pd.DataFrame()


def is_gym_related(product_name: str) -> bool:
    """Check if a product is part of Pratham's specific fitness journey."""
    if pd.isna(product_name):
        return False
    
    journey_items = [
        # 2022 - Foundation
        'airpods pro', 'teclor push up bar',
        # 2023 - Building Strength
        'grip strength', 'headband', 'gshock', 'g-shock',
        # 2024 - Equipment & Recovery
        'replacement ear tips', 'polislime', 'anti slip soft ear tips', 
        'noise reduction hole', 'silicone eartips', 'elbow brace', 
        'dip belt', 'ninja fit compact personal blender', 'body fat scale', 'scale',
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
    
    year = order_date.year if hasattr(order_date, 'year') else pd.to_datetime(order_date).year
    if year == 2022:
        return "🏗️ Foundation (2022)"
    elif year == 2023:
        return "💪 Building Strength (2023)"
    elif year == 2024:
        return "🛠️ Equipment & Recovery (2024)"
    elif year == 2025:
        return "🥤 Nutrition & Training (2025)"
    return f"Fitness Journey ({year})"


def get_journey_stage_color(stage: str) -> str:
    """Get color for each journey stage."""
    if "2022" in str(stage):
        return "#38bdf8"
    elif "2023" in str(stage):
        return "#34d399"
    elif "2024" in str(stage):
        return "#fbbf24"
    elif "2025" in str(stage):
        return "#fb7185"
    return "#64748b"


@st.cache_data
def filter_gym_products(df: pd.DataFrame, cache_version: str = "v2") -> pd.DataFrame:
    """Filter raw dataframe to only include Pratham's fitness journey products."""
    if df.empty:
        return df
    
    journey_mask = df['product_name'].apply(is_gym_related)
    journey_df = df[journey_mask].copy()
    
    journey_df = journey_df[
        (journey_df['total_owed'] > 0) & 
        (journey_df['order_status'] == 'Closed')
    ].copy()
    
    journey_df['journey_stage'] = journey_df.apply(
        lambda row: get_journey_stage(row['product_name'], row['order_date']), axis=1
    )
    journey_df = journey_df.sort_values('order_date', ascending=True)
    
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
    
    def get_item_type(product_name):
        product_lower = product_name.lower()
        for keyword, item_type in item_types.items():
            if keyword in product_lower:
                return item_type
        return product_name.lower()
    
    journey_df['item_type'] = journey_df['product_name'].apply(get_item_type)
    journey_df = journey_df.sort_values('order_date', ascending=True)
    journey_df = journey_df.drop_duplicates(subset=['item_type'], keep='first')
    return journey_df.sort_values('order_date', ascending=True)


def load_product_notes() -> Dict[str, str]:
    """Load product notes from JSON file."""
    notes_file = 'product_notes.json'
    try:
        if os.path.exists(notes_file):
            with open(notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_product_note(product_id: str, note: str) -> None:
    """Save a product note to JSON file."""
    notes_file = 'product_notes.json'
    try:
        notes = load_product_notes()
        notes[product_id] = note
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving note: {e}")


# ==============================================================================
# Curated Dataset & Local Image Asset Pipeline
# ==============================================================================
def load_curated_dataset() -> List[Dict]:
    """
    Load the clean curated products dataset, always dynamically syncing the latest reflections from product_notes.json.
    """
    notes = load_product_notes()
    curated_path = os.path.join(os.path.dirname(__file__), "data", "curated_products.json")
    if os.path.exists(curated_path):
        try:
            with open(curated_path, "r", encoding="utf-8") as f:
                items = json.load(f)
                if items and len(items) == 16:
                    for it in items:
                        asin = it.get('asin', '')
                        ts = it.get('order_timestamp', '')
                        key = f"{asin}_{ts}"
                        if key in notes:
                            it['reflection'] = notes[key]
                        else:
                            for k, v in notes.items():
                                if k.startswith(asin):
                                    it['reflection'] = v
                                    break
                    return items
        except Exception:
            pass

    # Fallback to generating directly from CSV + notes
    csv_file = "Retail.OrderHistory.1.csv"
    if os.path.exists(csv_file):
        raw_df = load_and_process_data(csv_file)
        gym_df = filter_gym_products(raw_df)
        
        fallback_items = []
        for _, r in gym_df.iterrows():
            asin = r.get('asin', '')
            od = str(r.get('order_date', ''))
            note_key = f"{asin}_{od}"
            img_path = f"assets/products/{asin}.jpg"
            if os.path.exists(f"assets/products/{asin}.png"):
                img_path = f"assets/products/{asin}.png"
                
            fallback_items.append({
                "id": str(asin),
                "product_name": r.get('product_name', ''),
                "purchase_date": od[:10],
                "order_timestamp": od,
                "year": int(r.get('year', 2022)),
                "category": "Fitness Gear",
                "price": float(r.get('total_owed', 0.0)),
                "asin": asin,
                "image_path": img_path,
                "reflection": notes.get(note_key, "")
            })
        return fallback_items

    return []


@st.cache_data
def get_product_image_src(image_path: str, product_name: str) -> str:
    """
    Return base64 data URI of local product image if present,
    or a clean dark SVG placeholder if the file is missing.
    NEVER makes network requests at runtime.
    """
    if image_path and os.path.exists(image_path) and os.path.getsize(image_path) > 500:
        try:
            mime = "image/jpeg"
            if image_path.lower().endswith(".png"):
                mime = "image/png"
            elif image_path.lower().endswith(".webp"):
                mime = "image/webp"

            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:{mime};base64,{b64}"
        except Exception:
            pass

    # Robust local SVG placeholder fallback
    short_title = (product_name[:24] + "...") if len(product_name) > 24 else product_name
    safe_title = urllib.parse.quote(short_title)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200" fill="none">'
        f'<rect width="300" height="200" fill="#090d16" rx="8"/>'
        f'<circle cx="150" cy="80" r="32" fill="#1e293b"/>'
        f'<path d="M136 80h28M140 73v14M160 73v14" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>'
        f'<text x="150" y="135" fill="#94a3b8" font-family="-apple-system, sans-serif" font-size="12" font-weight="600" text-anchor="middle">{safe_title}</text>'
        f'<text x="150" y="155" fill="#475569" font-family="-apple-system, sans-serif" font-size="10" text-anchor="middle">Milestone Asset</text>'
        f'</svg>'
    )
    return f"data:image/svg+xml;utf8,{svg}"


# Chapter Metadata & Narrative Essays
CHAPTERS = {
    2022: {
        "number": "Chapter 01",
        "title": "Foundation",
        "theme": "Calisthenics, Home Discipline, and Habit Formation",
        "css_class": "c-2022",
        "essay": (
            "Before stepping foot into a commercial gym or touching a barbell, my fitness journey began in my bedroom. "
            "I wasn't tracking macros, logging sets, or following rigid lifting splits. Inspired by bodyweight calisthenics, "
            "I bought push-up parallettes to build baseline upper-body strength and locked in with noise-canceling AirPods Pro. "
            "Putting those earbuds in and shutting out the world was how I built the daily mental habit of showing up."
        )
    },
    2023: {
        "number": "Chapter 02",
        "title": "Building Strength",
        "theme": "Consistency, Activity Tracking, and Trial by Error",
        "css_class": "c-2023",
        "essay": (
            "The second year was defined by cementing consistency and quantifying daily output. I picked up a rugged "
            "Casio G-Shock to track daily step targets with reliable accuracy rather than keeping a phone in my pocket. "
            "While trial purchases like hand grippers and headbands taught me what genuinely contributes to functional "
            "progress versus what is just gym novelty, the foundation was holding strong."
        )
    },
    2024: {
        "number": "Chapter 03",
        "title": "Equipment & Recovery",
        "theme": "Gym Transitions, Progressive Overload, and Joint Management",
        "css_class": "c-2024",
        "essay": (
            "As training intensity accelerated, workout logistics shifted. Alternating between the campus gym at Michigan "
            "State University and home breaks at Planet Fitness meant bringing my own dip belt for progressive overload on "
            "weighted dips and pull-ups. Morning smoothie blending fueled a structured caloric surplus, while elbow compression "
            "sleeves and weekly weight tracking forced me to balance heavy overload with active joint recovery."
        )
    },
    2025: {
        "number": "Chapter 04",
        "title": "Nutrition & Training",
        "theme": "Nutritional Precision, Pure Overload, and Form Discipline",
        "css_class": "c-2025",
        "essay": (
            "The final phase represents full optimization. Nutrition matured from casual smoothies to disciplined daily "
            "protein targets with clean plant protein and RXBARs. Adding micronized creatine marked the transition from casual "
            "training to deliberate sports nutrition. When heavy pressing and hack squats tested joint limits, wrist wraps and "
            "knee sleeves reinforced the ultimate lesson: progressive overload is meaningless without disciplined form."
        )
    }
}


def render_editorial_card(item: Dict, chapter_cls: str) -> str:
    """Render an editorial card with clickable product image/title and clean reflection."""
    image_src = get_product_image_src(item.get("image_path", ""), item.get("product_name", ""))
    
    # Format date nicely
    raw_date = item.get("purchase_date", "")
    try:
        dt = datetime.strptime(raw_date, "%Y-%m-%d")
        formatted_date = dt.strftime("%B %d, %Y")
    except Exception:
        formatted_date = raw_date
        
    name = item.get("product_name", "")
    reflection = item.get("reflection", "Personal milestone on the journey.")
    asin = item.get("asin", "")
    product_link = f"https://www.amazon.com/dp/{asin}" if asin else "#"
    
    return f"""
    <div class="editorial-card {chapter_cls}">
        <a href="{product_link}" target="_blank" rel="noopener noreferrer" class="img-link" title="View product details">
            <div class="img-frame">
                <img src="{image_src}" alt="{name}" loading="lazy"/>
            </div>
        </a>
        <a href="{product_link}" target="_blank" rel="noopener noreferrer" class="title-link">
            {name} ↗
        </a>
        <div class="card-date">Purchased &bull; {formatted_date}</div>
        <div class="card-reflection-block">
            "{reflection}"
        </div>
    </div>
    """


# ==============================================================================
# Main Editorial Streamlit View
# ==============================================================================
def main():
    # --------------------------------------------------------------------------
    # Editorial Hero Section
    # --------------------------------------------------------------------------
    st.markdown("""
    <div class="editorial-hero">
        <div class="hero-kicker">FITNESS TIMELINE &bull; 2022–2026</div>
        <h1>From Calisthenics to Heavy Lifts: My 4-Year Fitness Progression</h1>
        <p class="narrative-lead">
            A four-year fitness journey told through tangible milestones.
            When workout logs and macro spreadsheets weren't kept in a database,
            the physical gear and nutrition I committed my student budget to
            became the authentic record of my progression.
        </p>
        <div class="hero-byline">
            <span>Written & Curated by <strong>Pratham Pradhan</strong></span>
            <span>&bull;</span>
            <a href="https://prathampradhan.dev" target="_blank" rel="noopener noreferrer">prathampradhan.dev ↗</a>
            <span>&bull;</span>
            <span>16 Curated Milestones</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Load Dataset
    # --------------------------------------------------------------------------
    all_products = load_curated_dataset()
    if not all_products:
        st.error("No product dataset found. Please ensure data/curated_products.json or Retail.OrderHistory.1.csv exists.")
        return

    # --------------------------------------------------------------------------
    # Chronological Editorial Chapters (2022 -> 2025)
    # --------------------------------------------------------------------------
    for yr in [2022, 2023, 2024, 2025]:
        ch = CHAPTERS[yr]
        year_items = [x for x in all_products if x.get("year") == yr]
        
        if not year_items:
            continue

        # Chapter Header & Narrative Essay
        st.markdown(f"""
        <div class="chapter-container {ch['css_class']}">
            <div class="chapter-meta">
                <span class="chapter-number">{ch['number']} &bull; {yr}</span>
            </div>
            <h2 class="chapter-heading">{ch['title']}</h2>
            <div class="chapter-theme">{ch['theme']}</div>
            <p class="chapter-essay">{ch['essay']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Product Cards: 2-column balanced grid
        cols = st.columns(2)
        for idx, item in enumerate(year_items):
            col_target = cols[idx % 2]
            with col_target:
                card_html = render_editorial_card(item, ch['css_class'])
                st.markdown(card_html, unsafe_allow_html=True)
                st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

