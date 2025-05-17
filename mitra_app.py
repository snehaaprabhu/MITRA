import streamlit as st
import sqlite3
import hashlib
import matplotlib.pyplot as plt

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="Mitra - GRE Buddy", layout="wide")

# ---------------------- Database Connection ----------------------
def get_db_connection():
    conn = sqlite3.connect('init_db.db')
    return conn

# ---------------------- Initialize Tables ----------------------
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            gre_score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

# ---------------------- Hash Password ----------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------- Check if User Exists ----------------------
def user_exists(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# ---------------------- Add User ----------------------
def add_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

# ---------------------- Check Login ----------------------
def check_login(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

# ---------------------- Log GRE Score ----------------------
def log_gre_attempt(username, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_attempts (username, gre_score) VALUES (?, ?)', (username, score))
    conn.commit()
    conn.close()

# ---------------------- Fetch Past Scores ----------------------
def get_user_attempts(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT gre_score, timestamp FROM user_attempts WHERE username = ? ORDER BY timestamp DESC', (username,))
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------------- Session Init ----------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# ---------------------- Sidebar ----------------------
with st.sidebar:
    st.image("mitra.png", width=150)
    st.title("🎓 Mitra")
    st.markdown("Your GRE and US Admissions Assistant")

# ---------------------- Header ----------------------
st.markdown("<h1 style='text-align: center; color: #6c63ff;'>Welcome to<u> Mitra </u></h1>", unsafe_allow_html=True)
st.markdown("### Helping 3rd & 4th Year Engineering Students Plan Their Future")

# ---------------------- Auth Section ----------------------
if not st.session_state['logged_in']:
    menu = st.selectbox("Select an option", ["Login", "Sign Up"])

    if menu == "Sign Up":
        st.subheader("Create an Account")
        with st.form("signup_form"):
            username = st.text_input("Username", key="signup_username")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            submit_button = st.form_submit_button("Sign Up")

            if submit_button:
                if not username or not password:
                    st.warning("Please fill in all the fields.")
                elif password != confirm_password:
                    st.warning("Passwords do not match.")
                elif user_exists(username):
                    st.warning("Username already exists!")
                else:
                    add_user(username, password)
                    st.success("Account created successfully! You can now log in.")

    if menu == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if username and password:
                if check_login(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.warning("Incorrect username or password.")
            else:
                st.warning("Please enter both fields.")

# ---------------------- Main App ----------------------
if st.session_state['logged_in']:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📘 GRE Info", "🏛️ US Universities", "📈 Profile Eval", "💸 Funding", "📋 Dashboard"])

    with tab1:
        st.subheader("About the GRE")
        st.markdown("""
        The **Graduate Record Examination (GRE)** is a globally recognized standardized test that plays a key role in admissions to graduate and business programs, particularly in the United States.

        ### 🧪 Why is the GRE Important?
        - Required by most US universities for MS, MBA, and some PhD programs
        - Helps universities compare applicants from diverse academic backgrounds
        - A strong GRE score can **compensate for a lower GPA** or limited project experience

        ### 🧮 GRE Structure:
        | Section                  | Questions | Time     | Score Range |
        |--------------------------|-----------|----------|-------------|
        | Verbal Reasoning          | 40        | 60 mins  | 130–170     |
        | Quantitative Reasoning    | 40        | 70 mins  | 130–170     |
        | Analytical Writing        | 2 Essays  | 60 mins  | 0–6         |
        | Experimental Section      | Varies    | ~30 mins | Not Scored  |

        ⚠️ **Total Duration**: ~3 hours 45 minutes

        ### 📌 Scoring:
        - Total GRE score = Verbal + Quant (out of 340)
        - AWA (Analytical Writing) scored separately on a 6-point scale

        ### 📝 Preparation Tips:
        - **Verbal**: Learn 10 new GRE words every day. Use apps like Magoosh Vocabulary Builder.
        - **Quant**: Practice data interpretation, probability, geometry, and algebra.
        - **AWA**: Write practice essays and get them reviewed by mentors or tools like ETS’s ScoreItNow.
        - **Mock Tests**: Simulate real test conditions. ETS and Manhattan Prep offer great test series.

        👉 Register for the GRE at the official [ETS Website](https://www.ets.org/gre)
        """)
        st.info("🧠 Tip: Start preparing 3–4 months before your intended exam date for best results.")

    with tab2:
        st.subheader("Top US Universities Accepting GRE")
        # Keep your university tiers code here
        with st.expander("🎓 Tier 1: Highly Competitive (GRE 325+)", expanded=False):
            st.markdown("""
            - [Stanford University](https://www.stanford.edu)  
            - [MIT (Massachusetts Institute of Technology)](https://www.mit.edu)  
            - [Caltech (California Institute of Technology)](https://www.caltech.edu)
            """)
        with st.expander("🎯 Tier 2: Competitive (GRE 310–325)"):
            st.markdown("""
            - [University of Texas at Austin](https://www.utexas.edu)  
            - [University of Michigan, Ann Arbor](https://umich.edu)  
            - [Purdue University](https://www.purdue.edu)
            """)
        with st.expander("📚 Tier 3: Safe Options (GRE 295–310)"):
            st.markdown("""
            - [Arizona State University](https://www.asu.edu)  
            - [University at Buffalo (SUNY)](https://www.buffalo.edu)  
            - [University of Central Florida](https://www.ucf.edu)
            """)

    with tab3:
        st.subheader("Evaluate Your GRE Score 🎯")
        gre_score = st.slider("Enter your GRE score", 260, 340, 300)

        if gre_score >= 330:
            st.success("🌟 Excellent! Apply to MIT, Stanford, or Columbia.")
        elif 320 <= gre_score < 330:
            st.success("✅ Strong Profile! Consider UT Austin or Georgia Tech.")
        elif 310 <= gre_score < 320:
            st.info("👍 Good Profile! Look at Purdue, USC, NCSU.")
        elif 300 <= gre_score < 310:
            st.warning("⚠️ Decent. Consider ASU, SUNY, UCF.")
        else:
            st.error("❌ Improve score. Aim for 305+ to increase chances.")

        st.markdown("### 🎯 Your Score vs Averages")
        fig, ax = plt.subplots()
        universities = ['Top Tier', 'Mid Tier', 'Your Score']
        scores = [330, 315, gre_score]
        ax.bar(universities, scores, color=['green', 'orange', 'blue'])
        ax.set_ylim([260, 340])
        st.pyplot(fig)

    with tab4:
        st.subheader("Funding & Scholarships 💰")
        st.markdown("""
        Here are popular options to help fund your education:

        - 🏅 **Fulbright-Nehru Fellowship** – Covers tuition and living
        - 📖 **Inlaks Scholarship** – For top US institutions
        - 🎓 **Tata Trusts** – Need-based aid for Indian students
        - 🧑‍🔬 **University TA/RA** – Assistantships that offer stipends

        👉 Explore more at: [scholarships.com](https://www.scholarships.com)
        """)
        st.success("Tip: Apply early! Most funding deadlines are 6-9 months before intake.")


    # ------------- Tab 5: Dashboard -------------
    with tab5:
        st.subheader("📋 Your Dashboard")
        st.markdown(f"**👤 Username:** `{st.session_state['current_user']}`")

        st.markdown("### ➕ Log New GRE Score")
        with st.form("log_score_form"):
            new_score = st.slider("Enter new GRE score", 260, 340, 300, key="dashboard_slider")
            log_button = st.form_submit_button("Save Score")

            if log_button:
                log_gre_attempt(st.session_state['current_user'], new_score)
                st.success("✅ Score saved successfully!")
                st.rerun()

        st.markdown("### 📜 Your Past GRE Attempts")
        attempts = get_user_attempts(st.session_state['current_user'])
        if attempts:
            for score, timestamp in attempts:
                st.write(f"📌 **Score:** {score} | 🕒 {timestamp}")
            
            # ----- Score Trend Visualization -----
            st.markdown("### 📊 GRE Score Progress Over Time")
            scores = [score for score, _ in attempts][::-1]  # reverse to show oldest first
            timestamps = [timestamp for _, timestamp in attempts][::-1]

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(timestamps, scores, marker='o', color='blue', linewidth=2)
            ax.set_title("GRE Score Trend", fontsize=14)
            ax.set_xlabel("Attempt Date", fontsize=12)
            ax.set_ylabel("Score", fontsize=12)
            ax.set_ylim([260, 360])
            ax.grid(True)

            st.pyplot(fig)

        else:
            st.info("No attempts logged yet.")


    # ---------------------- Footer ----------------------
    st.markdown("---")
    st.markdown("<center>Made with ❤️ for aspiring grads by Mitra</center>", unsafe_allow_html=True)
