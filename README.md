# 💪 My Gym Journey — Through Amazon Orders

A beautiful Streamlit web application that visualizes your personal fitness evolution through Amazon purchase data. Track your gym-related purchases, add personal reflections, and analyze your spending patterns over time.

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## ✨ Features

- 🛍️ **Product Gallery**: Beautiful card-based display of gym purchases with product images
- 📊 **Analytics Dashboard**: Interactive charts showing spending patterns and trends
- 🔍 **Smart Filtering**: Filter by year range and search product names
- 💭 **Personal Notes**: Add reflections and notes for each purchase
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 🚀 **Fast Loading**: Optimized with Streamlit caching for smooth performance
- 📤 **Export Data**: Download filtered data as CSV for further analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Amazon Product Advertising API credentials (optional, for product images)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fitness-journey.git
   cd fitness-journey
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional, for Amazon API)
   ```bash
   cp env.example .env
   # Edit .env with your Amazon API credentials
   ```

4. **Add your Amazon order data**
   - Place your `Retail.OrderHistory.1.csv` file in the project root
   - The app will automatically detect and process gym-related products

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔧 Configuration

### Amazon Product Advertising API (Optional)

To enable product images, you'll need Amazon Product Advertising API credentials:

1. **Get Amazon Associates Account**
   - Sign up at [Amazon Associates](https://affiliate-program.amazon.com/)
   - Apply for Product Advertising API access

2. **Configure Environment Variables**
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env with your credentials
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AMAZON_ASSOCIATE_TAG=your_associate_tag_here
   AWS_REGION=us-east-1
   ```

3. **Without API**: The app works perfectly with placeholder images if you don't have API access.

## 📊 Data Format

The app expects a CSV file with the following columns:
- `Order Date`: Purchase date
- `Product Name`: Name of the product
- `Unit Price` or `Total Owed`: Product price
- `Quantity`: Number of items
- `Order Status`: Order status (filters for "Closed" orders)
- `ASIN`: Amazon Standard Identification Number (optional, for images)

## 🎨 Customization

### Adding New Gym Keywords

Edit the `is_gym_related()` function in `app.py` to add more keywords:

```python
gym_keywords = [
    'protein', 'creatine', 'gym', 'fitness', 'wrap', 'sleeve', 'shorts',
    'supplement', 'band', 'mat', 'weight', 'dumbbell', 'barbell',
    # Add your custom keywords here
    'your_keyword_here'
]
```

### Styling

The app uses custom CSS for a portfolio-ready design. Modify the CSS in the `st.markdown()` section of `app.py` to customize colors, fonts, and layout.

## 🚀 Deployment

### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set environment variables in the Streamlit Cloud dashboard
   - Deploy!

### Other Platforms

The app can be deployed on any platform that supports Python:
- **Heroku**: Use the included `Procfile`
- **Railway**: Deploy directly from GitHub
- **Vercel**: Use the Python runtime
- **Docker**: Use the included `Dockerfile`

## 📁 Project Structure

```
fitness-journey/
├── app.py                 # Main Streamlit application
├── amazon_api.py          # Amazon Product Advertising API helper
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
├── Retail.OrderHistory.1.csv  # Your Amazon order data
└── .gitignore            # Git ignore file
```

## 🛠️ Development

### Running in Development Mode

```bash
# Install in development mode
pip install -e .

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

### Adding New Features

1. **New Chart Types**: Add functions to `create_analytics_charts()`
2. **Additional Filters**: Extend the sidebar filter section
3. **Export Formats**: Add new export options in the sidebar
4. **Data Sources**: Modify `load_and_process_data()` for different CSV formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [Amazon Product Advertising API](https://webservices.amazon.com/paapi5/documentation/) for product data
- [Plotly](https://plotly.com/) for interactive charts
- [Pandas](https://pandas.pydata.org/) for data manipulation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/fitness-journey/issues) page
2. Create a new issue with detailed information
3. Contact: [your-email@example.com](mailto:your-email@example.com)

---

**Built with ❤️ by Pratham Pradhan**

*Showcasing skills in data visualization, web development, and API integration*