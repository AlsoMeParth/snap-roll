import streamlit as st
import time
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.teacher_subject_dialog import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.database.db import create_teacher, check_teacher_exist, teacher_login, get_teacher_subjects
def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()




def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    col1, col2 = st.columns(2, vertical_alignment='center', gap='large')
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"""Welcome, {teacher_data["name"]}""")
        if st.button("Log Out", type = "secondary",key = "loginbackbtn", shortcut = "control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take attendance", type = type1, width = 'stretch', icon = ':material/ar_on_you:'):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"

        if st.button("Manage subjects",type = type2, width = 'stretch', icon = ':material/book_ribbon:'):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button("Attendance records",type = type3, width = 'stretch', icon = ':material/cards_stack:'):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance():
    st.header("Take AI Attendance")
    teacher_id = st.session_state.teacher_data["teacher_id"]
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("You havn't created any subjects! Please create one to begin.")
        time.sleep(2)
        return
    subject_options = {f"{s['name']} -{s['subject_id']}" : s['subject_code'] for s in subjects}

    col1, col2 = st.columns([3,1])

    with col1:
        selected_subject = st.selectbox("Select Subject", options=list(subject_options.keys()))
        selected_subject_code = subject_options[selected_subject]
    with col2:
        if st.button("Add photos", type="primary", width = "stretch", icon=":material/photo_library:"):
            add_photos_dialog()
        
    st.divider()




def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects", width = "stretch")
    with col2:
        if st.button("Create New Subject", width = "stretch"):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for subject in subjects:
            stats = [
                ("👥", "Students", subject['total_students']),
                ("⏰", "Classes", subject['total_classes'])
            ]
        def share_btn():
            if st.button(f"Share Code: {subject['name']}", key = f"share_{subject['subject_code']}", icon = ":material/share:"):
                share_subject_dialog(subject['name'], subject['subject_code'])
            st.space()
        subject_card(
            name = subject['name'],
            code = subject['subject_code'],
            section = subject['section'],
            stats = stats,
            footer_callback = share_btn
        )
    else:
        st.info("No subjects found! Create one above.")

def teacher_tab_attendance_records():
    st.header("Attendance Records")

def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def teacher_screen_login():
    col1, col2 = st.columns(2, vertical_alignment='center', gap='large')
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", type = "secondary",key = "loginbackbtn", shortcut = "control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    st.space()    
    st.header("Login using password", text_alignment = "center")
    st.space()
    st.space()
    teacher_username = st.text_input(":red[Enter username]", placeholder="Vaibhav")
    teacher_password = st.text_input(":red[Enter password]", type="password", placeholder="Enter your password")

    st.divider()
    btncol1, btncol2 = st.columns(2)
    with btncol1:
        if st.button("Login", icon = ":material/passkey:",type="secondary", shortcut = "control + Enter", width = "stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome Back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password!")
    with btncol2:
        if st.button("Register Instead", type="primary", icon = ":material/passkey:", width = "stretch"):
            st.session_state.teacher_login_type = "register"    

    footer_dashboard()

def register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm):
    if not teacher_username or not teacher_name or not teacher_password:
        return False, "All fields are required!"
    if check_teacher_exist(teacher_username):
        return False, "Username already exists"
    if teacher_password != teacher_password_confirm:
        return False, "Password doesn't match"
    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Successfully Created! Login Now" 
    except Exception as e:
        return False, "Unexpected Error"


def teacher_screen_register():
    col1, col2 = st.columns(2, vertical_alignment='center', gap='large')

    with col1:
        header_dashboard()

    with col2:
        if st.button("Go back to Home", type = "secondary",key = "loginbackbtn", shortcut = "control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register your Teacher profile")
    st.space()
    st.space()
    teacher_username = st.text_input(":red[Enter username]", placeholder="royvishal")
    teacher_name = st.text_input(":red[Enter Name]", placeholder="Vishal Roy")
    teacher_password = st.text_input(":red[Enter password]", type="password", placeholder="Enter your password")
    teacher_password_confirm = st.text_input(":red[Confirm Password]", type="password", placeholder="Re-enter password")
    st.divider()
    btncol1, btncol2 = st.columns(2)
    with btncol1:
        if st.button("Register Now", icon = ":material/passkey:",type="secondary", shortcut = "control + Enter", width = "stretch"):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with btncol2:
        if st.button("Login Instead", type="primary", icon = ":material/passkey:", width = "stretch"):
            st.session_state.teacher_login_type = "login"    

    footer_dashboard()