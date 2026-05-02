import streamlit as st
import requests
import datetime

FIREBASE_API_KEY = "AIzaSyB_aAQxtij0yQ1m2JKjIWPcShnDUjvHPBc"
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Trạm Ghi Chú", page_icon="🌿", layout="wide")

custom_css = """
<style>
    [data-testid="stForm"] { border-radius: 16px; padding: 2rem; border: 1px solid #444; }
    .stButton>button { border-radius: 8px; font-weight: 600; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.uid = None
    st.session_state.email = None
if "current_note" not in st.session_state:
    st.session_state.current_note = None

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    res = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    if res.status_code == 200:
        data = res.json()
        st.session_state.token = data["idToken"]
        st.session_state.uid = data["localId"]
        st.session_state.email = data["email"]
        st.rerun()
    else: st.error("❌ Sai email hoặc mật khẩu!")

def register(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    res = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    if res.status_code == 200:
        st.success("🎉 Đăng ký thành công! Hãy chuyển sang Đăng nhập.")
    else:
        try:
            err = res.json()["error"]["message"]
            if err == "EMAIL_EXISTS": st.error("❌ Email đã tồn tại!")
            else: st.error(f"❌ Lỗi: {err}")
        except: st.error("❌ Có lỗi xảy ra khi đăng ký.")

if st.session_state.token is None:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🌿 Trạm Ghi Chú</h2>", unsafe_allow_html=True)
        auth_mode = st.radio("Thao tác:", ["Đăng nhập", "Đăng ký tài khoản"], horizontal=True, label_visibility="collapsed")
        
        if auth_mode == "Đăng nhập":
            with st.form("login_form"):
                login_email = st.text_input("📧 Email (@gmail.com)")
                login_password = st.text_input("🔑 Mật khẩu", type="password")
                submit_login = st.form_submit_button("Đăng Nhập Ngay 🚀", use_container_width=True)
                if submit_login: 
                    if not login_email.endswith("@gmail.com"): st.warning("Hệ thống chỉ nhận @gmail.com")
                    else: login(login_email, login_password)
        else:
            with st.form("register_form"):
                reg_email = st.text_input("📧 Email (@gmail.com)")
                reg_pass = st.text_input("🔑 Mật khẩu (ít nhất 6 ký tự)", type="password")
                reg_pass_conf = st.text_input("🔑 Xác nhận mật khẩu", type="password")
                submit_reg = st.form_submit_button("Tạo Tài Khoản ✨", use_container_width=True)
                if submit_reg:
                    if not reg_email.endswith("@gmail.com"): st.warning("Hệ thống chỉ nhận @gmail.com")
                    elif reg_pass != reg_pass_conf: st.warning("Mật khẩu không khớp!")
                    elif len(reg_pass) < 6: st.warning("Mật khẩu phải từ 6 ký tự trở lên")
                    else: register(reg_email, reg_pass)

else:
    # --- SIDEBAR ---
    st.sidebar.markdown(f"Xin chào,<br> **{st.session_state.email}** 👋", unsafe_allow_html=True)
    if st.sidebar.button("Đăng xuất", use_container_width=True):
        st.session_state.token = None
        st.rerun()
        
    st.sidebar.divider()

    if st.sidebar.button("➕ Ghi chú mới", type="primary", use_container_width=True):
        st.session_state.current_note = None
        st.rerun()

    st.sidebar.subheader("🕒 Lịch sử của bạn")
    res = requests.get(f"{BACKEND_URL}/notes/{st.session_state.uid}")
    if res.status_code == 200:
        notes = res.json().get("notes", [])
        for note in reversed(notes):
            with st.sidebar.container(border=True):
                st.markdown(f"**{note['title']}**")
                if note.get("deadline"):
                    st.caption(f"📅 Hạn: {note['deadline']}")
                
               
                if st.button("✏️ Chỉnh sửa", key=f"edit_{note['id']}", use_container_width=True):
                    st.session_state.current_note = note
                    st.rerun()
                    
    # --- MAIN AREA ---
    if st.session_state.current_note is None:
        st.title("📝 Viết ghi chú mới")
        def_title = ""
        def_content = ""
        def_deadline = datetime.date.today()
        note_id = None
    else:
       
        st.title("✏️ Chỉnh sửa ghi chú")
        note = st.session_state.current_note
        def_title = note.get("title", "")
        def_content = note.get("content", "")
        note_id = note.get("id")
        try:
            def_deadline = datetime.datetime.strptime(note.get("deadline", ""), "%d/%m/%Y").date()
        except:
            def_deadline = datetime.date.today()

    with st.form("note_form"):
        note_title = st.text_input("Tiêu đề:", value=def_title)
        note_deadline = st.date_input("Mốc thời gian (Deadline):", value=def_deadline, format="DD/MM/YYYY")
        note_content = st.text_area("Chi tiết:", value=def_content, height=200)
        
        btn_name = "Lưu Ghi Chú Mới" if note_id is None else "Cập Nhật Ghi Chú"
        submit_note = st.form_submit_button(btn_name)
        
        if submit_note: 
            if not note_title.strip() or not note_content.strip():
                st.warning("⚠️ Vui lòng nhập đủ tiêu đề và nội dung!")
            else:
                payload = {
                    "uid": st.session_state.uid, 
                    "title": note_title, 
                    "content": note_content,
                    "deadline": note_deadline.strftime("%d/%m/%Y")
                }
                if note_id: payload["note_id"] = note_id 
                
                post_res = requests.post(f"{BACKEND_URL}/notes", json=payload)
                if post_res.status_code == 200:
                    st.success(post_res.json()["message"])
                    st.session_state.current_note = None
                    st.rerun() 
                else:
                    st.error("❌ Lỗi Backend!")

   
    if note_id is not None:
        if st.button("🗑️ Xóa Ghi Chú Này", type="primary", use_container_width=True):
            del_res = requests.delete(f"{BACKEND_URL}/notes/{note_id}")
            if del_res.status_code == 200:
                st.success("Đã xóa thành công!")
                st.session_state.current_note = None
                st.rerun()
            else:
                st.error("❌ Lỗi Backend khi xóa!")