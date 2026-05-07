import streamlit as st
import base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def header_home():
    b64 = get_base64_image("src/img/logo.png")
    st.markdown(f"""
            <div style = "display:flex; flex-direction:column; align-items:center; justify-content:center;margin-bottom:30px;margin-top:30px">
                <img src='data:image/png;base64,{b64}' style = 'height:150px; width:150px' />
                <h1 style = 'text-align:center; color: #A9D2E7'>SNAP<br/>ROLL</h1>
            </div>


                """, unsafe_allow_html=True)
    
def header_dashboard():
    b64 = get_base64_image("src/img/logo.png")
    st.markdown(f"""
            <div style = "display:flex; align-items:center; justify-content:center;gap:10px">
                <img src='data:image/png;base64,{b64}' style = 'height:200px; width:85px' />
                <h2 style = 'text-align:left; color: #A9D2E7'>SNAP<br/>ROLL</h2>
            </div>


                """, unsafe_allow_html=True)