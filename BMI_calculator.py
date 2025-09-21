import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BMI Calculator - Health & Fitness Tracker",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f7fafc, #edf2f7);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 0.5rem 0;
    }
    .bmi-result {
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .recommendation-box {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4169e1;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💪 BMI Calculator</h1>
    <p>Professional Health & Fitness Assessment Tool</p>
</div>
""", unsafe_allow_html=True)

# BMI Calculation Functions
def calculate_bmi(weight, height, unit):
    """Calculate BMI based on weight and height"""
    if unit == 'Imperial':
        # Convert pounds to kg and inches to meters
        weight_kg = weight * 0.453592
        height_m = height * 0.0254
    else:
        # Convert cm to meters
        weight_kg = weight
        height_m = height / 100
    
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Get BMI category based on value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_bmi_color(bmi):
    """Get color for BMI category"""
    if bmi < 18.5:
        return "#3182ce"  # Blue
    elif bmi < 25:
        return "#38a169"  # Green
    elif bmi < 30:
        return "#d69e2e"  # Orange
    else:
        return "#e53e3e"  # Red

def calculate_ideal_weight(height, gender, unit):
    """Calculate ideal weight using Devine formula"""
    height_cm = height * 2.54 if unit == 'Imperial' else height
    
    if gender == 'Male':
        ideal_weight = 50 + (2.3 * ((height_cm - 152.4) / 2.54))
    else:
        ideal_weight = 45.5 + (2.3 * ((height_cm - 152.4) / 2.54))
    
    if unit == 'Imperial':
        return round(ideal_weight * 2.20462)
    return round(ideal_weight)

def calculate_bmr(weight, height, age, gender, unit):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    weight_kg = weight * 0.453592 if unit == 'Imperial' else weight
    height_cm = height * 2.54 if unit == 'Imperial' else height
    
    if gender == 'Male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    return round(bmr)

def get_recommendations(bmi_category, age, gender):
    """Get personalized recommendations based on BMI category"""
    recommendations = []
    
    if bmi_category == "Underweight":
        recommendations = [
            "🍽️ Focus on nutrient-dense, calorie-rich foods like nuts, seeds, avocados, and lean proteins",
            "💪 Include strength training exercises to build muscle mass along with cardiovascular fitness",
            "👨‍⚕️ Consider consulting with a nutritionist to develop a healthy weight gain plan"
        ]
    elif bmi_category == "Normal Weight":
        recommendations = [
            "⚖️ Maintain your current healthy lifestyle with balanced nutrition and regular exercise",
            "🏃‍♂️ Continue with 150 minutes of moderate aerobic activity or 75 minutes vigorous activity weekly",
            "🍎 Focus on whole foods, fruits, vegetables, lean proteins, and whole grains"
        ]
    elif bmi_category == "Overweight":
        recommendations = [
            "📈 Aim for gradual weight loss of 1-2 pounds per week through caloric deficit",
            "🚴‍♂️ Increase physical activity to 300+ minutes of moderate exercise per week",
            "🥕 Focus on portion control and include more vegetables, lean proteins, and whole grains"
        ]
    else:  # Obese
        recommendations = [
            "👨‍⚕️ Consult with a healthcare provider to develop a comprehensive weight management plan",
            "❤️ Start with low-impact exercises and gradually increase intensity as fitness improves",
            "📅 Consider working with a registered dietitian for personalized meal planning"
        ]
    
    return recommendations

# Sidebar for input
with st.sidebar:
    st.header("📋 Enter Your Details")
    
    # Unit selection
    unit = st.selectbox("Select Unit System", ["Metric", "Imperial"])
    
    # Input fields based on unit
    if unit == "Metric":
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
    else:
        height = st.number_input("Height (inches)", min_value=48.0, max_value=96.0, value=67.0, step=0.1)
        weight = st.number_input("Weight (lbs)", min_value=66.0, max_value=660.0, value=154.0, step=0.1)
    
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    calculate_button = st.button("🧮 Calculate BMI", type="primary")

# Main content
if calculate_button:
    # Calculate BMI and related metrics
    bmi = calculate_bmi(weight, height, unit)
    category = get_bmi_category(bmi)
    color = get_bmi_color(bmi)
    ideal_weight = calculate_ideal_weight(height, gender, unit)
    bmr = calculate_bmr(weight, height, age, gender, unit)
    recommendations = get_recommendations(category, age, gender)
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # BMI Result Display
        st.markdown(f"""
        <div class="bmi-result" style="background-color: {color}15; border: 2px solid {color};">
            <h2 style="color: {color}; font-size: 3rem; margin: 0;">{bmi}</h2>
            <h3 style="color: {color}; margin: 0.5rem 0;">{category}</h3>
            <p style="margin: 0;">Body Mass Index</p>
        </div>
        """, unsafe_allow_html=True)
        
        # BMI Categories Chart
        st.subheader("📊 BMI Categories")
        
        # Create BMI scale visualization
        fig = go.Figure()
        
        # Add BMI ranges
        categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
        ranges = [18.5, 25, 30, 40]
        colors = ['#3182ce', '#38a169', '#d69e2e', '#e53e3e']
        
        for i, (cat, range_val, color_val) in enumerate(zip(categories, ranges, colors)):
            start = 0 if i == 0 else ranges[i-1]
            fig.add_trace(go.Bar(
                y=[cat],
                x=[range_val - start],
                orientation='h',
                name=cat,
                marker_color=color_val,
                base=start if i > 0 else 0
            ))
        
        # Add user's BMI marker
        fig.add_vline(x=bmi, line_dash="dash", line_color="black", line_width=3,
                     annotation_text=f"Your BMI: {bmi}", annotation_position="top")
        
        fig.update_layout(
            barmode='stack',
            xaxis_title="BMI Value",
            yaxis_title="Categories",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Health Metrics
        st.subheader("📈 Health Metrics")
        
        weight_unit = "kg" if unit == "Metric" else "lbs"
        
        metrics_data = [
            {"metric": "Current BMI", "value": bmi, "unit": ""},
            {"metric": "BMI Category", "value": category, "unit": ""},
            {"metric": "Ideal Weight", "value": ideal_weight, "unit": weight_unit},
            {"metric": "Daily Calories (BMR)", "value": bmr, "unit": "cal"},
        ]
        
        for metric in metrics_data:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #4a5568;">{metric['metric']}</h4>
                <h2 style="margin: 0.5rem 0; color: #667eea;">{metric['value']} {metric['unit']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Weight Goal Calculation
        if category == "Underweight":
            min_normal_bmi = 18.5
            if unit == "Metric":
                target_weight = min_normal_bmi * (height/100)**2
            else:
                target_weight = min_normal_bmi * (height*0.0254)**2 * 2.20462
            weight_goal = f"+{abs(target_weight - weight):.1f} {weight_unit}"
        elif category in ["Overweight", "Obese"]:
            max_normal_bmi = 24.9
            if unit == "Metric":
                target_weight = max_normal_bmi * (height/100)**2
            else:
                target_weight = max_normal_bmi * (height*0.0254)**2 * 2.20462
            weight_goal = f"-{abs(weight - target_weight):.1f} {weight_unit}"
        else:
            weight_goal = "Maintain current weight"
        
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: #4a5568;">Weight Goal</h4>
            <h2 style="margin: 0.5rem 0; color: #667eea;">{weight_goal}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations Section
    st.subheader("💡 Personalized Recommendations")
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"""
        <div class="recommendation-box">
            <p style="margin: 0; font-weight: 500;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # BMI History Tracker (simulated data for demo)
    st.subheader("📈 BMI Trend Analysis")
    
    # Create sample BMI history
    dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
    sample_bmis = [bmi + np.random.normal(0, 0.5) for _ in range(12)]
    sample_bmis[-1] = bmi  # Current BMI
    
    bmi_df = pd.DataFrame({
        'Date': dates,
        'BMI': sample_bmis
    })
    
    fig_trend = px.line(bmi_df, x='Date', y='BMI', 
                       title='BMI Trend Over Time',
                       line_shape='spline')
    
    # Add BMI category zones
    fig_trend.add_hline(y=18.5, line_dash="dash", line_color="blue", 
                       annotation_text="Underweight threshold")
    fig_trend.add_hline(y=25, line_dash="dash", line_color="green", 
                       annotation_text="Normal weight threshold")
    fig_trend.add_hline(y=30, line_dash="dash", line_color="red", 
                       annotation_text="Obese threshold")
    
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Health Tips based on BMI
    st.subheader("🏥 Health Information")
    
    health_info = {
        "Underweight": {
            "risks": ["Weakened immune system", "Osteoporosis risk", "Delayed wound healing"],
            "benefits": ["Lower risk of heart disease", "Reduced joint stress"]
        },
        "Normal Weight": {
            "risks": ["Generally low health risks"],
            "benefits": ["Optimal health status", "Lower disease risk", "Better energy levels"]
        },
        "Overweight": {
            "risks": ["Increased diabetes risk", "High blood pressure", "Sleep apnea"],
            "benefits": ["Can be reversed with lifestyle changes"]
        },
        "Obese": {
            "risks": ["Heart disease", "Type 2 diabetes", "Stroke risk", "Certain cancers"],
            "benefits": ["Significant health improvements possible with weight loss"]
        }
    }
    
    current_info = health_info[category]
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### ⚠️ Health Considerations")
        for risk in current_info["risks"]:
            st.markdown(f"• {risk}")
    
    with col4:
        st.markdown("### ✅ Positive Aspects")
        for benefit in current_info["benefits"]:
            st.markdown(f"• {benefit}")

else:
    # Welcome message when no calculation has been performed
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f7fafc, #edf2f7); border-radius: 15px;">
        <h2>Welcome to Your Personal BMI Calculator! 👋</h2>
        <p style="font-size: 1.2rem; color: #718096;">
            Enter your details in the sidebar to get started with your health assessment.
        </p>
        <br>
        <p><strong>Features included:</strong></p>
        <p>📊 Detailed BMI Analysis • 💪 Health Metrics • 🎯 Personalized Recommendations • 📈 Trend Visualization</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; padding: 1rem;">
    <p><strong>Disclaimer:</strong> This calculator provides estimates for informational purposes only. 
    Consult healthcare professionals for medical advice.</p>
    <p>Built with ❤️ using Python & Streamlit</p>
</div>
""", unsafe_allow_html=True)