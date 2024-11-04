import streamlit as st
import numpy as np
import cv2
from PIL import Image, UnidentifiedImageError
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Set page configuration as the very first Streamlit command
st.set_page_config(
    page_title='Ship Detection App',
    page_icon=":ship:",
    layout='wide',
    initial_sidebar_state='auto',
    menu_items={
        'About': "Ship Detection Web App by Bharadwaj Kamepalli"
    }
)

# Load your pre-trained model

def load_model():
    model = tf.keras.models.load_model('ship-model.h5')
    return model

model = load_model()

class_names = ["no-ship", "ship"]
class_name_labels = {0: "no-ship", 1: "ship"}

def predict(image):
    image = cv2.resize(image, (64, 64))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    class_id = np.argmax(prediction)
    class_label = class_name_labels[class_id]
    confidence = np.max(prediction) * 100  # Multiply by 100 to convert to percentage
    return class_label, confidence

def main():
    st.title('Ship Detection in Satellite Images')

    # Sidebar About section with better formatting and collapsible content
    with st.sidebar:
        st.header('About')
        with st.expander("Learn more"):
            st.markdown("""
                **Ship Detection Model**

                This model predicts the presence of ships in satellite images using a trained convolutional neural network (CNN). It is designed to assist in monitoring and managing maritime activities, which are crucial for:

                - Maritime safety
                - Fishing regulation
                - Traffic monitoring

                **Author: Bharadwaj Kamepalli**
            """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert('RGB')
            image_array = np.array(image)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            if st.button('Predict'):
                prediction, confidence = predict(image_array)
                st.write(f'Prediction: {prediction}')
                st.write(f'Confidence: {confidence:.2f}%')

                # Display a bar chart of confidence with adjusted size
                fig, ax = plt.subplots(figsize=(3, 1.5))  # Reduced size
                ax.bar(class_names, [100-confidence, confidence], color=['#d3d3d3', '#76b947'])  # Changed colors and modified range for clarity
                ax.set_ylabel('Confidence (%)')
                ax.set_ylim([0, 100])
                st.pyplot(fig)
        except UnidentifiedImageError:
            st.error("The uploaded file is not a valid image. Please check the file and try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
