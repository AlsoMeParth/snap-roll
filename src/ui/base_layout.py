import streamlit as st

def style_background_home():

    st.markdown("""
        <style>
               .stApp{
                    background: #2A6593 !important;
                } 
                .stApp div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding: 2.5rem !important;
                    border-radius: 5rem !important;
                }
        </style>

    """, unsafe_allow_html=True)

def style_background_dashboard():

    st.markdown("""
        <style>
               .stApp{
                    background:#2A6593 !important;
                } 
        </style>

    """, unsafe_allow_html=True)

def style_base_layout():

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        /*Hide Top Toolbar in streamlit */
            MainMenu, footer, header {
                visibility: hidden;
            }
            .block-container {
                padding-top:1.5rem !important;
            }
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important; 
                color: #A9D2E7 !important;
                }
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important; 
                color: #092B4E !important;
                }

            h4, p{
                font-family: 'Outfit', sans-serif !important;
                color:  #E8F4FA !important;
                }
            h3{
                font-family: 'Outfit',sans-serif !important;
                color: #E8F4FA !important
                }
            button {
            border-radius: 1.5rem !important;
            background-color: #58A4CB !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out, background-color 0.25s ease-in-out !important;
            }   

            button [kind="secondary"]{
            border-radius: 1.5rem !important;
            background-color: #58A4CB !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out, background-color 0.25s ease-in-out !important;
            }
            button[kind="tertiary"]{
                border-radius : 1.5rem !important;
                background-color : #0F1C2E ! important;
                color : white !important;
                padding : 10px 20px !important;
                border : None !important;
                transition : transform 0.25s ease-in-out !important;
            }
            button:hover{
                transform :scale(1.05) !important;
                background-color: #0F1C2E !important;
                }
            button:hover p {
            color: white !important;
            }
        </style>

    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        div[data-testid="stAlert"] {
            background-color: #0F1C2E !important;
            border: 1px solid #2A6593 !important;
        }
        div[data-testid="stAlert"] p {
            color: #A9D2E7 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        /* toast container */
        div[data-testid="stToast"] {
            background-color: #0F1C2E !important;
            border: 1px solid #58A4CB !important;
        }
        /* toast text */
        div[data-testid="stToast"] p {
            color: #A9D2E7 !important;
        }
        /* toast icon */
        div[data-testid="stToast"] svg {
            fill: #58A4CB !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        div[data-testid="stDialog"] > div > div {
            background-color: #2A6593 !important;
        }
    </style>
    """, unsafe_allow_html=True)