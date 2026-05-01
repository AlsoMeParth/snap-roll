import streamlit as st
from supabase import create_client, Client

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# try:
#     client = create_client(SUPABASE_URL, SUPABASE_KEY)
#     client.table("teachers").select("*").limit(1).execute()
#     print("Connected successfully!")
# except Exception as e:
#     print(f"Failed: {e}")