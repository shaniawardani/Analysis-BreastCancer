import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model # type: ignore
from sklearn.preprocessing import LabelEncoder
import json
from supabase import create_client, Client
from datetime import datetime, timezone
from fpdf import FPDF
import io
from pytz import timezone

# Translations dictionary
translations = {
    'en': {
        'welcome': 'Welcome, ',
        'choose_method': 'Choose Prediction Method:',
        'machine_learning': '30 Features',
        'deep_learning': '6 Features',
        'prediction_title': 'Prediction Cancer Type Using - ',
        'patient_name': 'Patient Name',
        'submit': 'Submit',
        'data_inserted': 'Data Inserted!',
        'download_pdf': 'Download PDF Report',
        'patient_warning': 'Patient name must be provided before continuing.',
        'logout': 'Logout',
        'language': 'Language/Bahasa',
        'login_first': 'Please login first!',
    },
    'id': {
        'welcome': 'Selamat datang, ',
        'choose_method': 'Pilih Metode Prediksi:',
        'machine_learning': 'Machine Learning',
        'deep_learning': 'Deep Learning',
        'prediction_title': 'Prediksi Jenis Kanker Menggunakan - ',
        'patient_name': 'Nama Pasien',
        'submit': 'Kirim',
        'data_inserted': 'Data Berhasil Dimasukkan!',
        'download_pdf': 'Unduh Laporan PDF',
        'patient_warning': 'Nama pasien harus diisi sebelum melanjutkan.',
        'logout': 'Keluar',
        'language': 'Bahasa',
        'login_first': 'Silakan login terlebih dahulu!',
    }
}

# Define the folder paths
folderML = 'hasil/ML'
folderDL = 'hasil/DL'


# # Configure Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
JWT_SECRET = st.secrets["JWT_SECRET"] 

if not SUPABASE_URL or not SUPABASE_KEY or not JWT_SECRET:
     raise EnvironmentError("SUPABASE_URL or SUPABASE_KEY is not set in .env file or environment variables.")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load categories from JSON file
ohe_json_path = 'hasil/ML/ann.json'  # Sesuaikan path jika perlu

try:
    with open(ohe_json_path, 'r') as json_file:
        ohe_categories = json.load(json_file)
except FileNotFoundError:
    st.error(f"File JSON '{ohe_json_path}' tidak ditemukan.")
    ohe_categories = {}


# Load Machine Learning model and preprocessing components

# Memuat kembali model dan preprocessing tools
ml_model_path = os.path.join(folderML, 'model_ann10064.h5')

# Pastikan file dan folder ada sebelum memuat
if not os.path.exists(ml_model_path):
    st.error(f"Model file '{ml_model_path}' tidak ditemukan.")

# Memuat model, label encoder, scaler, dan OneHotEncoder
ml_model = tf.keras.models.load_model(ml_model_path)  # Memuat model

# Load Deep Learning model
dl_model = load_model(os.path.join(folderDL, 'model_dnn7032.h5'))
dl_model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
ahnak2_mutenc = ohe_categories.get("AHNAK2 Mutation", [])
mutation_encoder = LabelEncoder()
mutation_encoder.fit(ahnak2_mutenc)

# categorical_cols = [ohe_encoder.categories_[0]]
categorical_cols = ['oncotree_code', 'chemotherapy', 'tumor_other_histologic_subtype', 
                        'ahnak2_mut', 'kmt2d_mut', 'stab2_mut', 'pde4dip_mut', 'map3k1_mut', 
                        'muc16_mut', 'cdh1_mut', 'atr_mut']


# Preprocess and adjust input data to match model input
def ml_prediction(input_data):
    # Daftar fitur yang digunakan selama pelatihan
    expected_features = [
        "neoplasm_histologic_grade", "aurka", "chek1", "ccne1", "ahnak",
        "e2f2", "cdc25a", "aph1b", "cdh1", "gsk3b", "lama2", "src", 
        "tgfb3", "slc19a1", "lfng", "mapt", "cdk1", "hsd17b10", "bcl2",
        "chemotherapy", "oncotree_code", "tumor_other_histologic_subtype",
        "ahnak2_mut", "kmt2d_mut", "stab2_mut", "pde4dip_mut", 
        "map3k1_mut", "muc16_mut", "cdh1_mut", "atr_mut"
    ]

    # buat validasi di data nya apabila ada data yang NaN, maka diisi 0 apabila numerical dan unknown apabila kategorikal
    for feature in expected_features:
        if feature not in input_data.columns:
            input_data[feature] = 0 if feature not in ohe_categories else 'Unknown'

    # Pastikan urutan kolom sesuai dengan yang diharapkan model
    input_data = input_data[expected_features]

    # Encode kategori menjadi numerik
    encoders = {
        "oncotree_code": ohe_categories.get("Oncotree Code", []),
        "tumor_other_histologic_subtype": ohe_categories.get("Tumor Other Histologic Subtype", []),
        "chemotherapy": ohe_categories.get("Chemotherapy", []),
        "ahnak2_mut": ohe_categories.get("AHNAK2 Mutation", []),
        "kmt2d_mut" : ohe_categories.get("KMT2D Mutation", []),
        "stab2_mut" : ohe_categories.get("STAB2 Mutation", []),
        "pde4dip_mut" : ohe_categories.get("PDE4DIP Mutation", []),
        "map3k1_mut" : ohe_categories.get("MAP3K1 Mutation", []),
        "muc16_mut" : ohe_categories.get("MUC16 Mutation", []),
        "cdh1_mut" : ohe_categories.get("CDH1 Mutation", []),
        "atr_mut" : ohe_categories.get("ATR Mutation", [])
    }

    for feature, categories in encoders.items():
        if feature in input_data.columns:
            input_data[feature] = input_data[feature].apply(lambda x: categories.index(x) if x in categories else -1)  # Fallback ke -1 jika tidak ditemukan

    # Pilih hanya kolom numerik untuk prediksi
    numerical_cols = input_data.select_dtypes(include=[np.number]).columns
    X_new_processed = input_data[numerical_cols].to_numpy(dtype=np.float32)

    # buat validasi apabila jml inptan dengan feature dataset itu sama 
    if len(X_new_processed.shape) == 1:
        X_new_processed = X_new_processed.reshape(1, -1)

    # Predict using ANN model
    predictions = ml_model.predict(X_new_processed)
    predicted_classes = np.argmax(predictions, axis=1)

    # Ambil label tipe kanker dari JSON
    cancer_types = ohe_categories.get("cancers_types", [])
    predicted_label = [cancer_types[class_idx] for class_idx in predicted_classes]

    # Add prediction to input data for later insertion into Supabase
    input_data['prediction'] = predicted_label[0]
    
    return predicted_label[0]

# Function to get user input for Machine Learning model
def get_user_input_ml():
    st.title(f"{text('prediction_title')}{text('machine_learning')}")

     # patient = st.text_input("Patient Name")
    patient = st.text_input(text('patient_name'))

    if not patient.strip():
        st.warning(text('patient_warning'))
        return None
    # Slider for each kolom with min value and max value from Dataset training
    neoplasm_histologic_grade = st.slider('Neoplasm Histologic Grade', 1.0000, 3.0000, 1.0000)
    aurka = st.slider('AURKA', -2.27, 4.82, 0.0)
    ccne1 = st.slider('CCNE1', -1.55, 5.64, 0.0)
    chek1 = st.slider('CHEK1', -1.9498, 4.0154, 0.0)
    ahnak = st.slider('AHNAK', -5.1982, 3.3290, 0.0)
    e2f2 = st.slider('E2F2', -2.3664, 4.6230, 0.0)
    cdc25a = st.slider('CDC25A', -1.9507, 4.4992, 0.0)
    aph1b = st.slider('APH1B', -2.9178, 3.8819, 0.0)
    cdh1 = st.slider('CDH1', -3.3237, 2.8209, 0.0)
    gsk3b = st.slider('GSK3B', -2.9365, 3.4707, 0.0)
    lama2 = st.slider('LAMA2', -2.2392, 3.6904, 0.0)
    src = st.slider('SRC', -3.2506, 3.8812, 0.0)
    tgfb3 = st.slider('TGFB3', -2.9964, 2.4067, 0.0)
    slc19a1 = st.slider('SLC19A1', -2.6814, 5.3590, 0.0)
    lfng = st.slider('LFNG', -2.9711, 3.1072, 0.0)
    mapt = st.slider('MAPT', -2.0151, 2.3416, 0.0)
    cdk1 = st.slider('CDK1', -2.4035, 4.6134, 0.0)
    hsd17b10 = st.slider('HSD17B10', -3.7902, 5.0452, 0.0)
    bcl2 = st.slider('BCL2', -2.7919, 2.6561, 0.0)                  

    # Menampilkan input dengan opsi dari JSON
    if ohe_categories:
        # Kategori tanpa opsi input manual (hanya selectbox)
        oncotree_code = st.selectbox('Oncotree Code', ohe_categories.get("Oncotree Code", []))
        tumor_other_histologic_subtype = st.selectbox('Tumor Other Histologic Subtype', ohe_categories.get("Tumor Other Histologic Subtype", []))
        chemotherapy = st.selectbox('Chemotherapy', ohe_categories.get("Chemotherapy", []))
        
        # Kategori 
        ahnak2_mut = st.selectbox('AHNAK2 Mutation', ohe_categories.get("AHNAK2 Mutation", []))
        kmt2d_mut = st.selectbox('KMT2D Mutation', ohe_categories.get("KMT2D Mutation", []))
        stab2_mut = st.selectbox('STAB2 Mutation', ohe_categories.get("STAB2 Mutation", []))
        pde4dip_mut = st.selectbox('PDE4DIP Mutation', ohe_categories.get("PDE4DIP Mutation", []))
        map3k1_mut = st.selectbox('MAP3K1 Mutation', ohe_categories.get("MAP3K1 Mutation", []))
        muc16_mut = st.selectbox('MUC16 Mutation', ohe_categories.get("MUC16 Mutation", []))
        cdh1_mut =st.selectbox('CDH1 Mutation', ohe_categories.get("CDH1 Mutation", []))
        atr_mut = st.selectbox('ATR Mutation', ohe_categories.get("ATR Mutation", []))
    else:
        st.warning("Kategori tidak tersedia. Pastikan file JSON telah dimuat dengan benar.")

    # Create DataFrame from user input
    return pd.DataFrame({
        "patient": patient,
        "neoplasm_histologic_grade": [neoplasm_histologic_grade],
        "aurka": [aurka],
        "chek1": [chek1],
        "ccne1": [ccne1],
        "ahnak": [ahnak],
        "e2f2": [e2f2],
        "cdc25a": [cdc25a],
        "aph1b": [aph1b],
        "cdh1": [cdh1],
        "gsk3b": [gsk3b],
        "lama2": [lama2],
        "src": [src],
        "tgfb3": [tgfb3],
        "slc19a1": [slc19a1],
        "chemotherapy": [chemotherapy], 
        "lfng": [lfng],
        "mapt": [mapt],
        "cdk1": [cdk1],
        "hsd17b10": [hsd17b10],
        "bcl2": [bcl2],
        "oncotree_code": [oncotree_code],
        "tumor_other_histologic_subtype": [tumor_other_histologic_subtype],
        "ahnak2_mut": [ahnak2_mut],
        "kmt2d_mut": [kmt2d_mut],
        "stab2_mut": [stab2_mut],
        "pde4dip_mut": [pde4dip_mut],
        "map3k1_mut": [map3k1_mut],
        "muc16_mut": [muc16_mut],
        "cdh1_mut": [cdh1_mut],
        "atr_mut": [atr_mut],
    })

def generate_pdf(input_data, result, model_type):
    # Function to generate a PDF report and provide a download link
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title Section
    pdf.set_font("Times", "B", 18)
    pdf.set_text_color(138, 44, 82)  # Adjusted color
    pdf.cell(0, 10, f"Medical Prediction Report ({model_type})", 0, 1, 'C')
    pdf.ln(10)

    # Header Section: Patient Information
    pdf.set_font("Times", "B", 14)
    pdf.set_text_color(0, 0, 0)  # Reset text color to black
    pdf.cell(0, 10, "Patient Information", 0, 1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Line separator
    pdf.ln(5)

    # Patient Name
    patient_name = input_data.get("patient", "")
    pdf.set_font("Times", "", 12)
    pdf.cell(50, 10, "Patient Name:", 0, 0)
    pdf.cell(0, 10, f"{patient_name if patient_name else '[Not Provided]'}", 0, 1)

    # Clinical Data Section
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Clinical Data", 0, 1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Line separator
    pdf.ln(5)

    # Table Header
    pdf.set_font("Times", "B", 12)
    pdf.set_fill_color(230, 230, 230)  # Light grey background for header
    pdf.cell(90, 10, "Parameter", 1, 0, 'C', fill=True)
    pdf.cell(0, 10, "Value", 1, 1, 'C', fill=True)

    # Clinical Data Table
    pdf.set_font("Times", "", 12)
    for key, value in input_data.items():
        if key != "patient":  # Skip the patient key
            pdf.cell(90, 10, f"{key.replace('_', ' ').capitalize()}:", 1, 0, 'L')
            
            # Format value safely
            formatted_value = (
                f"{value[0]:.2f}" if isinstance(value, list) and isinstance(value[0], (int, float)) else
                f"{value:.2f}" if isinstance(value, (int, float)) else
                f"{value}" if value else "[Not Provided]"
            )
            
            pdf.cell(0, 10, formatted_value, 1, 1, 'L')

    pdf.ln(10)

    # Prediction Result Section
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Prediction Result", 0, 1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Line separator
    pdf.ln(5)
    pdf.set_font("Times", "", 12)
    pdf.set_text_color(138, 44, 82)  # Adjusted color
    pdf.cell(50, 10, "Predicted Cancer Type:", 0, 0)
    pdf.cell(0, 10, f"{result}", 0, 1)

    # Reset text color to black
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # Create a BytesIO object to hold the PDF
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S'))  # Write the bytearray directly
    pdf_output.seek(0)

    # Display download link in Streamlit
    st.download_button(
        label="Download PDF Report",
        data=pdf_output,
        file_name="medical_prediction_report.pdf",
        mime="application/pdf"
    )
   
def text(key):
    language = st.session_state.get('language', 'en')  # Default ke 'en'
    return translations[language].get(key, key)
    
def set_page_config():
    """Set the initial page configuration."""
    st.set_page_config(
        page_icon="",
        page_title="Breast Cancer Analysis",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

def inject_custom_css():
    """Inject custom CSS for styling."""
    st.markdown(
        """
        <style>
        /* Background for the main content */
        .stApp {
            background-color: #FFE0EC;
            padding: 20px;
            background-image:url(https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/bcimage.png?raw=true);
        }
        /* Change the background color of the sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFB3D9;
            position: relative;
        }

        /* Styling for form header */
        .form-header-container {
            background-color: #8A2C52;
            border-radius: 15px;
            padding: 20px 0;
            width: 90%;
            margin: auto;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Styling for form header text */
        .form-header {
            color: #FFFFFF;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #FFF5F7;
            border-radius: 10px;
            height: 40px;
            padding-left: 10px;
            border: none;
            margin-bottom: 10px;
        }

        /* Button styling */
        .stButton > button {
            background-color: #FFFFFF;
            color: #A65277;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #F0D0E1;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    """Render the sidebar with navigation."""
    with st.sidebar:
        if st.button("Logout"):
            # Hapus semua data di session_state (opsional)
            for key in st.session_state.keys():
                del st.session_state[key]
            # Beri konfirmasi logout (opsional)
            st.switch_page("Dashboard.py")  # Redirect ke halaman login (jika ada sistem multi-halaman)
            st.success("You have successfully logged out.")
        st.markdown(
           """
            <div style="text-align: center;">
                <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/logo.png?raw=true' class='sidebar-logo'/>
            </div>
            """, unsafe_allow_html=True
        )
        # Language selection in the sidebar
        language = st.selectbox('Language/Bahasa', ['en', 'id'])
        st.session_state['language'] = language


# Function to handle Deep Learning prediction
def dl_prediction(input_data):
    # Transform and normalize features for Deep Learning
    le_tumor_subtype = LabelEncoder()
    # le_tumor_subtype.fit(['Ductal/NST', 'Mixed', 'Lobular', 'Tubular/ cribriform', 'Mucinous', 'Medullary', 'Other', 'Unknown', 'Metaplastic'])
    le_tumor_subtype.fit(ohe_categories.get("Tumor Other Histologic Subtype", []))
    

    le_oncotree_code = LabelEncoder()
    # le_oncotree_code.fit(['IDC', 'MDLC', 'ILC', 'IMMC', 'BREAST', 'Unknown', 'MBC'])
    le_oncotree_code.fit(ohe_categories.get("Oncotree Code",[]))


    # Normalization and encoding
    input_data['tumor_other_histologic_subtype'] = le_tumor_subtype.transform([input_data['tumor_other_histologic_subtype']])[0]
    input_data['oncotree_code'] = le_oncotree_code.transform([input_data['oncotree_code']])[0]

    # Encode mutation
    try:
        input_data['ahnak2_mut'] = mutation_encoder.transform([input_data['ahnak2_mut']])[0]
    except ValueError:
        st.error(f"Invalid mutation value: {input_data['ahnak2_mut']}")
        return None
    
    processed_data = np.array([input_data['tumor_other_histologic_subtype'],
                               input_data['oncotree_code'],
                               input_data['ahnak2_mut'],
                               input_data['aurka'],
                               input_data['ccne1'],
                               input_data['src']]).reshape(1, -1)  # Reshape to (1, 6) as needed for the model

    # Predict using the DL model
    predictions = dl_model.predict(processed_data)
    predicted_class = predictions.argmax(axis=1)

    
    cancer_types = ohe_categories.get("cancers_types", [])



    le_cancer_type_detailed = LabelEncoder()
    le_cancer_type_detailed.fit(cancer_types)
    predicted_cancer_type = le_cancer_type_detailed.inverse_transform(predicted_class)

    # Add prediction to input data for later insertion into Supabase
    input_data['prediction'] = predicted_cancer_type[0]

    return predicted_cancer_type[0]
    
# Function to get user input for DL model
def get_user_input_dl():

    st.title(f"{text('prediction_title')}{text('deep_learning')}")

     # patient = st.text_input("Patient Name")
    patient = st.text_input(text('patient_name'))

    if not patient.strip():
        st.warning(text('patient_warning'))
        return None

    # Menampilkan input dengan opsi dari JSON
    if ohe_categories:
        # Kategori tanpa opsi input manual (hanya selectbox)
        tumor_other_histologic_subtype = st.selectbox('Tumor Other Histologic Subtype', ohe_categories.get("Tumor Other Histologic Subtype", []))
        oncotree_code = st.selectbox('Oncotree Code', ohe_categories.get("Oncotree Code", []))
        
        # Kategori dengan opsi input manual
        ahnak2_mut = st.selectbox('AHNAK2 Mutation', ohe_categories.get("AHNAK2 Mutation", []))
    else:
        st.warning("Kategori tidak tersedia. Pastikan file JSON telah dimuat dengan benar.")

    aurka = st.slider('AURKA', -2.27, 4.82, 0.0)
    ccne1 = st.slider('CCNE1', -1.55, 5.64, 0.0)
    src = st.slider('SRC', -3.2506, 3.8812, 0.0)

    # Return input as dictionary
    return {
        "patient": patient,
        'tumor_other_histologic_subtype': tumor_other_histologic_subtype,
        'oncotree_code': oncotree_code,
        'ahnak2_mut': ahnak2_mut,
        'aurka': aurka,
        'ccne1': ccne1,
        'src': src
    }


# Function to insert data into Supabase, convert data dari dataframe ke dict untuk masuk ke supabase nya
def insert_to_supabase(input_data, model_type):    
    # Convert pandas Series to dictionary if input_data is a pandas Series
    if isinstance(input_data, pd.DataFrame):
        input_data = input_data.to_dict(orient="records")[0]  # Ambil baris pertama jika hanya satu

    local_tz = timezone('Asia/Jakarta')
    timestamp = datetime.now(local_tz).isoformat()
    patient = input_data.get("patient", "unknown_patient")
    input_data['prediction'] = input_data.get('prediction', 'Unknown')  # Default to 'Unknown' if not present
   
    # Prepare data to insert into the Supabase table
    if model_type == 'ML':
        data = {
            "patient": patient,  # Add patient_id
            "neoplasm_histologic_grade": input_data["neoplasm_histologic_grade"],
            "aurka": input_data["aurka"],
            "chek1": input_data["chek1"],
            "ccne1": input_data["ccne1"],
            "ahnak": input_data["ahnak"],
            "e2f2": input_data["e2f2"],
            "cdc25a": input_data["cdc25a"],
            "aph1b": input_data["aph1b"],
            "cdh1": input_data["cdh1"],
            "gsk3b": input_data["gsk3b"],
            "lama2": input_data["lama2"],
            "src": input_data["src"],
            "tgfb3": input_data["tgfb3"],
            "slc19a1": input_data["slc19a1"],
            "chemotherapy": input_data["chemotherapy"],
            "lfng": input_data["lfng"],
            "mapt": input_data["mapt"],
            "cdk1": input_data["cdk1"],
            "hsd17b10": input_data["hsd17b10"],
            "bcl2": input_data["bcl2"],
            "oncotree_code": input_data["oncotree_code"],
            "tumor_other_histologic_subtype": input_data["tumor_other_histologic_subtype"],          
            "ahnak2_mut": input_data["ahnak2_mut"],
            "kmt2d_mut": input_data["kmt2d_mut"],
            "stab2_mut": input_data["stab2_mut"],
            "pde4dip_mut": input_data["pde4dip_mut"],
            "map3k1_mut": input_data["map3k1_mut"],
            "muc16_mut": input_data["muc16_mut"],
            "cdh1_mut": input_data["cdh1_mut"],
            "atr_mut": input_data["atr_mut"],
            "timestamp": timestamp,  # Add the timestamp
            "prediction": input_data["prediction"]  # Assuming you have predicted cancer type in the input data
        }
         # Masukkan data ke tabel Supabase
        try:
            supabase.table("ML").insert(data).execute()
            # st.write(f"Data berhasil dimasukkan")
        except Exception as e:
            st.write(f"Error saat memasukkan data ke Supabase: {e}")

    elif model_type == 'DL':
        # Convert numpy Series to dictionary if input_data is a numpy Series
        if isinstance(input_data, pd.Series):
            input_data = input_data.to_dict()
        input_data = {key: (value.item() if isinstance(value, np.generic) else value) for key, value in input_data.items()}
        data_dl = {
            "patient": patient,  # Add patient_id
            "tumor_other_histologic_subtype": input_data["tumor_other_histologic_subtype"],
            "oncotree_code": input_data["oncotree_code"],
            "ahnak2_mut": input_data["ahnak2_mut"],
            "aurka": input_data["aurka"],
            "ccne1": input_data["ccne1"],
            "src": input_data["src"],
            "timestamp": timestamp,  # Add the timestamp
            "prediction": input_data["prediction"],  # Assuming you have predicted cancer type in the input data
        }
        # Insert data into Supabase DL table
        try:
            supabase.table("DL").insert(data_dl).execute()
        except Exception as e:
            st.write(f"Error saat memasukkan data ke Supabase: {e}")


def logout():
    """Log out the user by clearing session state."""
    del st.session_state['logged_in']
    del st.session_state['username']
    del st.session_state['email']
    st.success("You have been logged out!")


# Main function to run Streamlit app
def main():
    set_page_config()
    inject_custom_css()
    render_sidebar()

    if not st.session_state.get('logged_in', False):
        st.write("Please login first!")
        return

    if st.session_state['logged_in']:
        st.write(f"{text('welcome')}{st.session_state.get('username', '')}!")
        
        
        # Radio button for selecting model
        model_choice = st.radio(text('choose_method'), (text('machine_learning'), text('deep_learning')))

        # Get user input
        if model_choice == '30 Features':
            input_data = get_user_input_ml()
            
            if st.button('Submit'):
                result = ml_prediction(input_data)
                # st.write(f"Predicted Cancer Type : {result}")
                st.write(f"Predicted Cancer Type : {result}")
                input_data["prediction"] = result
                # Insert data into Supabase
                insert_to_supabase(input_data, model_type='ML')
                st.write(text('data_inserted'))
                # Generate PDF report
                generate_pdf(input_data.iloc[0].to_dict(), result, model_type='Machine Learning')


        elif model_choice == '6 Features':
            input_data = get_user_input_dl()

            # Add submit button
            if st.button('Submit'):
                result = dl_prediction(input_data)
                st.write(f"Predicted Cancer Type : {result}")
             
                # Insert data into Supabase
                insert_to_supabase(input_data, model_type='DL')
                st.write(text('data_inserted'))
                # Generate PDF report
                generate_pdf(input_data, result, model_type='Machine Learning')



if __name__ == "__main__":
    main()

