import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import base64

# Load the trained model
@st.cache_resource
def load_trained_model():
    model = load_model('plastic_sign.h5')  # Ensure this path is correct
    return model

model = load_trained_model()

# Image preprocessing function
IMG_SIZE = (224, 224)  # Same size used during training

def preprocess_image(image):
    img = image.resize(IMG_SIZE)  # Resize image
    img_array = img_to_array(img)  # Convert image to array
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Function to add a background image
def add_background_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
        }}
        .center {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Add a background image
add_background_image("back2.jpg")  # Provide the correct path to your background image

# Plastic type descriptions and recyclability info
plastic_info = {
    "PEHD_highdensitypolyethylene(2)": {
        "description": "High-density polyethylene (HDPE) is commonly used for milk jugs, detergent bottles, and piping. It is durable and resistant to impact.Plastic Type 2 (HDPE) is a durable, strong, and lightweight thermoplastic known for its excellent chemical resistance and low moisture absorption. It is widely used for milk jugs, detergent bottles, piping, and grocery bags. Identified by the recycling code 2 HDPE is easily recyclable and highly versatile for various applications.",
        "recyclable": "Recyclable",
    },
    "PELD_lowdensitypolyethylene(4)": {
        "description": "Low-Density Polyethylene (LDPE) is a lightweight, flexible, and durable thermoplastic commonly used in everyday products. It is widely used in manufacturing plastic bags, shrink wraps, squeeze bottles, container lids, and packaging films due to its moisture resistance and ease of molding. LDPE is recyclable and is typically categorized under recycling code #4, though the availability of recycling facilities varies by region. Its recyclability helps reduce plastic waste, making it an eco-friendlier choice when properly disposed of. However, LDPE is not biodegradable and can contribute to pollution if not recycled or reused effectively.",
        "recyclable": "Recyclable",
    },
    "Noplastic(8)": {
        "description": "The 'No Plastic' category, often labeled as recycling code #8, includes materials that are not plastic, such as glass, metal, paper, or biodegradable materials. These materials are commonly used in items like glass jars, aluminum cans, paper packaging, and compostable containers. They are typically more eco-friendly and easier to recycle or dispose of compared to plastics. Recycling or repurposing these materials significantly reduces environmental impact, as they often have dedicated recycling systems and can be reused multiple times. Proper segregation ensures these non-plastic materials are effectively processed and contribute to sustainable waste management.",
        "recyclable": "Non-recyclable",
    },
    "OherResins(7)": {
        "description": "Other Resins, categorized under recycling code #7, include a variety of plastics such as polycarbonate (PC), polylactic acid (PLA), and acrylic. These plastics are used in a wide range of products, including water cooler bottles, certain food containers, baby bottles, medical devices, and automotive parts, due to their strength and versatility. While some types of #7 plastics, like PLA, are biodegradable under specific industrial conditions, most are not. Recycling options for code #7 plastics are limited and vary by region, making proper disposal a challenge. When possible, reusing or recycling these materials can help reduce environmental impact.",
        "recyclable": "Depends on local facilities",
    },
    "PET_polyethylene(1)": {
        "description": "Polyethylene terephthalate (PET) is commonly used in water and soda bottles. It is lightweight and clear.Plastic Type 1 (PET or PETE)** is a lightweight, strong, transparent, and recyclable thermoplastic. It offers excellent barrier properties, chemical resistance, and is widely used for beverage bottles, food packaging, and textiles. It’s identified by the recycling code 1 and is one of the most commonly recycled plastics.",
        "recyclable": "Recyclable",
    },
    "PP_polypropylene(5)": {
        "description": "Polypropylene (PP), marked with recycling code #5, is a durable and versatile plastic widely used in everyday items like food containers, bottle caps, straws, medicine bottles, and reusable food storage containers. Its high resistance to heat and chemicals makes it suitable for applications such as microwavable containers and automotive parts. PP is recyclable and is often repurposed into items like bins, battery cases, or outdoor furniture. However, its recycling availability depends on local facilities. Due to its reusability and strength, polypropylene is considered an eco-friendlier plastic when disposed of or recycled responsibly.",
        "recyclable": "Recyclable",
    },
    "PS_polystyrene(6)": {
        "description": "Polystyrene (PS), labeled under recycling code #6, is a lightweight and rigid plastic commonly used in products like disposable cups, food containers, utensils, packing peanuts, and insulation materials. Its versatility and low cost make it popular for both consumer and industrial applications. Polystyrene is technically recyclable, but recycling facilities for it are limited, as the material is bulky and challenging to process efficiently. If not properly managed, PS can persist in the environment, contributing to pollution and harming wildlife. Reducing single-use polystyrene products or switching to reusable alternatives can minimize its environmental impact.",
        "recyclable": "Non-recyclable",
    },
    "PVC__polyvinylchloride(3)": {
        "description": "Polyvinyl chloride (PVC) is used in pipes, credit cards, and some packaging. It is tough but not widely recyclable.Plastic Type 3 (PVC) is a strong, durable, and versatile thermoplastic. It is resistant to chemicals, weather, and fire due to its chlorine content. Common uses include pipes, window frames, flooring, and medical equipment. Identified by the recycling code 3 PVC is less commonly recycled and can release harmful chemicals if not properly managed.",
        "recyclable": "Non-recyclable",
    },
}

# Function to display recyclability box
def display_recyclability_box(recyclability):
    # Define box color based on recyclability
    if recyclability == "Recyclable":
        color = "#4CAF50"  # Green for recyclable
    elif recyclability == "Non-recyclable":
        color = "#F44336"  # Red for non-recyclable
    else:
        color = "#FFC107"  # Yellow for 'Depends on local facilities'

    # HTML for the highlighted box
    st.markdown(
        f"""
        <div style="
            border: 2px solid {color};
            background-color: {color}20;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            color: {color};
            margin-top: 10px;
        ">
            {recyclability}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Center-align content
st.markdown(
    """
    <style>
    .center {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit App UI
st.markdown('<div class="center">', unsafe_allow_html=True)
st.title("♻️ Plastic Recycle Sign Detector")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="center">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Display uploaded image with reduced size
    st.markdown('<div class="center">', unsafe_allow_html=True)
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=False, width=300)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Predict button
    st.markdown('<div class="center">', unsafe_allow_html=True)
    if st.button("Predict"):
        with st.spinner("Predicting..."):
            # Preprocess and predict
            image = load_img(uploaded_file)
            processed_image = preprocess_image(image)
            prediction = model.predict(processed_image)
            
            # Class labels
            class_labels = ['Noplastic(8)', 'OherResins(7)', 'PEHD_highdensitypolyethylene(2)','PELD_lowdensitypolyethylene(4)','PET_polyethylene(1)','PP_polypropylene(5)','PS_polystyrene(6)','PVC__polyvinylchloride(3)']
            
            # Get predicted class
            predicted_class_index = np.argmax(prediction, axis=1)[0]
            predicted_label = class_labels[predicted_class_index]
            
            # Fetch description and recyclability
            info = plastic_info[predicted_label]
            description = info["description"]
            recyclability = info["recyclable"]
            
            # Display prediction
            st.success(f"♻️ Predicted type: **{predicted_label}**")
            st.markdown(f"**Description:** {description}")
            
            # Highlight recyclability
            display_recyclability_box(recyclability)
    st.markdown('</div>', unsafe_allow_html=True)
