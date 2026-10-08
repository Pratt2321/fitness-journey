# ⚡ From Calisthenics to Heavy Lifts: My 4-Year Fitness Progression (2022–2026)

A personal portfolio project by [Pratham Pradhan](https://prathampradhan.dev) visualizing a 4-year fitness evolution using real Amazon order history as a proxy for progression and discipline.

![Streamlit](https://img.shields.io/badge/Streamlit-1.63.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.3+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-7.1+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## 📖 The Narrative Thesis

When lifts, daily macros, and step counts weren't consistently tracked in a dedicated workout app, physical equipment and nutritional purchases became the authentic proxy for my journey.

Between 2022 and 2026, 16 key purchases on a student budget traced the shift from home calisthenics and habit building to weighted overload, injury management, and sports nutrition:

```
Amazon Order Data (Retail.OrderHistory.1.csv)
       ↓
Curated Fitness Milestones (16 items spanning 2022–2026)
       ↓
Local Product Metadata & Reflections (data/curated_products.json)
       ↓
Local Image Asset Pipeline (assets/products/*.jpg, *.png)
       ↓
Story-First Streamlit Web App (app.py)
```

---

## 🗺️ The Four Chapters

1. **Chapter 1: 2022 — Foundation**  
   *Calisthenics, Home Workouts, and Building the Habit.*  
   Push-up parallettes and noise-canceling AirPods Pro to lock in and establish daily discipline before ever setting foot in a commercial gym.

2. **Chapter 2: 2023 — Building Strength**  
   *Grip Endurance, Activity Tracking, and Navigating Setbacks.*  
   Casio G-Shock step tracking, grip trainers, and separating gym novelty from functional training.

3. **Chapter 3: 2024 — Equipment & Recovery**  
   *Campus Gym vs. Break Gyms, Weighted Overload, and Managing Joint Health.*  
   Moving between Michigan State University and Planet Fitness, bringing a dedicated dip belt for weighted dips and pull-ups, high-calorie smoothie blending, and elbow compression support.

4. **Chapter 4: 2025 — Nutrition & Training**  
   *Supplementation, Protein Precision, and Form-First Discipline.*  
   Daily protein targets with Orgain and RXBARs, micronized creatine, wrist support for heavy pressing, and knee sleeves after hack squat lessons.

---

## ✨ Architecture & Features

- **Story First → Data Second**: Chronological narrative chapters paired with personal retrospective reflections on *why* each purchase mattered.
- **Local Image Asset Pipeline**: High-resolution, authentic product images stored locally in `assets/products/`. Zero external API calls at runtime.
- **Graceful Fallback**: Inline dark SVG placeholders render seamlessly if any image asset is ever missing.
- **Curated Dataset Schema**: Clean, structured metadata in `data/curated_products.json` (`id`, `product_name`, `purchase_date`, `year`, `category`, `price`, `asin`, `image_path`, `reflection`).
- **Interactive Gear Lenses**: Filter by timeline chapter, full story vs. core lifting gear vs. nutrition, or live search.
- **Secondary Analytics**: Clean Plotly visualizations breaking down financial trajectory and category distribution.
- **Automated Test Suite**: Comprehensive test pipeline in `test_app.py` (6/6 tests covering data loading, filtering, schema validation, local image resolution, and fallback resilience).

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/pratt2321/fitness-journey.git
cd fitness-journey
pip install -r requirements.txt
```

### 2. Verify Local Images (One-Time Fetcher)
```bash
python3 scripts/image_fetcher.py
```
*(All 16 product images are already pre-downloaded and stored in `assets/products/`.)*

### 3. Run Tests
```bash
python3 test_app.py
```

### 4. Launch Streamlit Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Repository Structure

```
fitness-journey/
├── assets/
│   └── products/                  # Local authentic product photography (16 items)
├── data/
│   └── curated_products.json      # Structured curated metadata & reflections
├── scripts/
│   └── image_fetcher.py           # Offline utility to populate local product images
├── Retail.OrderHistory.1.csv      # Raw Amazon order history export
├── product_notes.json             # Personal purchase reflections keyed by ASIN & timestamp
├── app.py                         # Story-first Streamlit web application
├── test_app.py                    # Complete test suite
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

---

## 👤 Author

**Pratham Pradhan**  
Portfolio: [prathampradhan.dev](https://prathampradhan.dev)