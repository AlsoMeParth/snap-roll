import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_logs, unenroll_student_from_subject
from src.pipelines.voice_pipeline import get_voice_embedding
from src.components.dialog_student_enroll import enroll_dialog
import numpy as np
from PIL import Image
import time

def student_dashboard():
    student_data = st.session_state.student_data
    col1, col2 = st.columns(2, vertical_alignment='center', gap='large')
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"""Welcome, {student_data["name"]}""")
        if st.button("Log Out", type = "secondary",key = "loginbackbtn", shortcut = "control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1,c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button("Enroll in Subject", type = "primary", width = "stretch"):
            enroll_dialog(student_data)
    st.divider()
    with st.spinner("Loading your enrolled subjects.."):
        subjects = get_student_subjects(student_data['student_id'])
        logs =  get_student_logs(student_data['student_id'])

    stats_map = {}

    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"Total" : 0, "Attended" : 0}

        stats_map[sid]["Total"] += 1
        if log.get("is_present"):
            stats_map[sid]["Attended"] += 1

    cols = st.columns(2) #col1, col2
    
    for i, sub in enumerate(subjects):
        s = sub['subjects']
        sid = s['subject_id']
        stats = stats_map.get(sid, {"Total" : 0, "Attended" : 0})

        with cols[i%2]:
            subject_card(
                name = s['name'],
                code = s['subject_code'],
                section = s['section'],
                stats = [
                    ('🗓️', "Total Classes", stats["Total"]),
                    ('✅', "Attended", stats["Attended"]) 
                ],
                footer_callback = lambda : unenroll_btn(student_data['student_id'], sid, s["subject_code"])
            )
    footer_dashboard()

def unenroll_btn(student_id, subject_id, subject_code):
    if st.button("Unenroll from this subject", type="tertiary", width = "stretch"):
        unenroll_student_from_subject(student_id, subject_id)
        st.toast(f"Unenrolled from {subject_code} successfully!")
        time.sleep(1.5)
        st.rerun()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    col1, col2 = st.columns(2, vertical_alignment='center', gap='large')
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", type = "secondary",key = "loginbackbtn", shortcut = "control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    st.space()    
    st.header("Login using FaceID", text_alignment = "center")
    st.space()
    st.space()

    show_registration = False
    photo_source = st.camera_input("Position your face in the center") 
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning"):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found")
            elif num_faces>1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    # getting all the student information for this student_id from database
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Wecome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not Recognized! You might be a new student')
                    show_registration = True
    if show_registration:
        with st.container(border = True):
            st.header("Register new Profile")
            new_name = st.text_input("Enter your name", placeholder = 'E.g. Abcd Sharma')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll for voice only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase like Hello, I am present today.')
            except Exception:
                st.error("Audio Data Failed!")
            
            if st.button("Create Account", type='primary'):
                if new_name:
                    with st.spinner('Creating Profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data :
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(new_name, face_embedding = face_emb, voice_embedding = voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Welcome {new_name}")
                                time.sleep(1)
                                st.rerun() 
                        else:
                            st.error("'Couldn't capture your facial features for registration")
                else:
                    st.warning("Please enter your name")
    footer_dashboard()