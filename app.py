import streamlit as st

import textwrap

from datetime import date

from agents.agent_manager import TravelAgentManager

from services.database_service import TravelDatabaseService

from agents.budget_analyst_agent import BudgetAnalystAgent

from agents.itinerary_planner_agent import ItineraryPlannerAgent

from services.auth_service import AuthService





# --------------------------------------------------

# PAGE CONFIGURATION

# --------------------------------------------------

st.set_page_config(

    page_title="GoRove | Smart Travel Companion",

    page_icon="🌍",

    layout="wide",

    initial_sidebar_state="expanded"

)





# --------------------------------------------------

# SESSION INITIALIZATION AND AUTHENTICATION

# --------------------------------------------------

DEFAULT_SESSION_VALUES = {

    "is_authenticated": False,

    "current_user": None,

    "chat_history": [],

    "trip_destination": "",

    "trip_travellers": 2,

    "trip_budget": 30000,

    "trip_start_date": date.today(),

    "trip_end_date": None,

    "trip_travel_type": "Relaxation",

    "trip_research_result": None,

}



for key, value in DEFAULT_SESSION_VALUES.items():

    if key not in st.session_state:

        st.session_state[key] = value





auth_service = AuthService()



# Re-check the account on every authenticated rerun.

if st.session_state.is_authenticated and st.session_state.current_user:

    latest_user = auth_service.get_user_by_id(

        st.session_state.current_user["user_id"]

    )



    if not latest_user or latest_user["is_active"] != 1:

        st.session_state.is_authenticated = False

        st.session_state.current_user = None

        st.session_state.pop("agent_manager", None)

        st.session_state.pop("chat_history", None)

        st.warning(

            "Your account is inactive or unavailable. "

            "Please contact the administrator."

        )

        st.stop()



    st.session_state.current_user = {

        "user_id": latest_user["user_id"],

        "full_name": latest_user["full_name"],

        "email": latest_user["email"],

        "role": latest_user["role"],

    }





# --------------------------------------------------

# GLOBAL STYLING

# --------------------------------------------------

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');



html, body, [class*="css"] {

    font-family: 'DM Sans', sans-serif;

}

.stApp {

    background: #f5f7fa;

}

.block-container {

    max-width: 1380px;

    padding-top: 1.8rem;

    padding-bottom: 3rem;

}

h1, h2, h3 {

    color: #172b45;

    letter-spacing: -0.35px;

}

p {

    line-height: 1.65;

}

section[data-testid="stSidebar"] {

    background: #14263f;

}

section[data-testid="stSidebar"] > div {

    padding: 1.2rem 1rem;

}

section[data-testid="stSidebar"] * {

    color: #f8fafc;

}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {

    padding: 9px 11px;

    border-radius: 9px;

    margin-bottom: 4px;

    font-size: 14px;

}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {

    background: rgba(255,255,255,0.10);

}

.stButton > button {

    background: #245b78;

    color: white;

    border: 1px solid #245b78;

    border-radius: 9px;

    min-height: 42px;

    padding: 8px 20px;

    font-weight: 700;

}

.stButton > button:hover {

    background: #19445c;

    border-color: #19445c;

    color: white;

}

.stTextInput input, .stNumberInput input, .stDateInput input {

    border-radius: 9px;

}

.info-card {

    background: #ffffff;

    padding: 23px;

    border-radius: 13px;

    border: 1px solid #e7ebef;

    min-height: 166px;

}

.info-card h3 {

    font-size: 18px;

    margin-top: 12px;

    margin-bottom: 7px;

}

.info-card p {

    color: #64748b;

    font-size: 13px;

    margin-bottom: 0;

}

.hero {

    background:

        linear-gradient(90deg, rgba(12,31,52,0.86), rgba(12,31,52,0.25)),

        url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1800&q=85");

    background-size: cover;

    background-position: center;

    min-height: 330px;

    padding: 62px 46px;

    border-radius: 16px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    margin-bottom: 32px;

}

.hero-kicker {

    color: #d8e6ef;

    font-size: 11px;

    letter-spacing: 2px;

    font-weight: 800;

    text-transform: uppercase;

}

.hero h1 {

    color: #ffffff;

    font-family: 'Playfair Display', serif;

    font-size: 43px;

    line-height: 1.2;

    max-width: 700px;

    margin-top: 14px;

    margin-bottom: 14px;

}

.hero p {

    color: #f1f5f9;

    font-size: 16px;

    max-width: 650px;

    margin-bottom: 0;

}

.destination-card {

    height: 205px;

    border-radius: 12px;

    overflow: hidden;

    background-size: cover;

    background-position: center;

    display: flex;

    align-items: end;

    padding: 17px;

    box-shadow: inset 0 -95px 85px rgba(0,0,0,0.52);

}

.destination-card h3 {

    color: #ffffff;

    font-size: 20px;

    margin: 0;

}

.section-subtitle {

    color: #718096;

    font-size: 14px;

    margin-top: -9px;

    margin-bottom: 22px;

}

.footer {

    text-align: center;

    color: #82909d;

    padding: 24px 0 10px 0;

    font-size: 12px;

    border-top: 1px solid #e8edf1;

    margin-top: 30px;

}



.gorove-footer-heading {

    color: #245b78;

    font-size: 15px;

    font-weight: 700;

    margin: 8px 0 10px 0;

}

.gorove-footer-note {

    color: #34465a;

    font-size: 13px;

    line-height: 1.8;

}

.gorove-footer-brand {

    background: #101d2d;

    color: #ffffff;

    padding: 18px 20px;

    margin-top: 32px;

    border-radius: 4px 4px 0 0;

}

.gorove-footer-brand strong {

    color: #ffffff;

    font-size: 19px;

}

.gorove-footer-brand div {

    color: #e2e8f0;

    font-size: 12px;

    margin-top: 4px;

}

.gorove-footer-copyright {

    background: #101d2d;

    color: #e2e8f0;

    text-align: center;

    padding: 13px 8px;

    margin-top: 16px;

    font-size: 12px;

}

.st-key-gorove_footer .stButton > button {

    background: transparent !important;

    color: #34465a !important;

    border: 0 !important;

    border-radius: 0 !important;

    min-height: 0 !important;

    height: auto !important;

    padding: 3px 0 !important;

    margin: 0 !important;

    font-size: 13px !important;

    font-weight: 400 !important;

    text-align: left !important;

    justify-content: flex-start !important;

    box-shadow: none !important;

}

.st-key-gorove_footer .stButton > button:hover {

    background: transparent !important;

    color: #245b78 !important;

    text-decoration: underline !important;

}

.auth-shell {

    max-width: 980px;

    margin: 22px auto 0 auto;

    background: #ffffff;

    border: 1px solid #e6edf3;

    border-radius: 24px;

    overflow: hidden;

    box-shadow: 0 22px 65px rgba(24, 54, 78, 0.12);

}

.auth-brand-panel {

    min-height: 590px;

    padding: 55px 42px;

    color: white;

    background:

      linear-gradient(145deg, rgba(12,35,58,.94), rgba(31,91,120,.82)),

      url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1100&q=85");

    background-size: cover;

    background-position: center;

    display: flex;

    flex-direction: column;

    justify-content: center;

}

.auth-brand-panel h1 {

    color: white;

    font-family: 'Playfair Display', serif;

    font-size: 42px;

    margin: 16px 0 8px 0;

}

.auth-brand-panel p {

    color: #e4edf4;

    font-size: 15px;

}

.auth-brand-tag {

    color: #c6e3ef;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 2px;

}

.auth-form-panel {

    padding: 38px 34px 30px 34px;

}

.auth-footnote {

    color: #8a98a8;

    text-align: center;

    font-size: 11px;

    margin-top: 22px;

}

@media (max-width: 768px) {

    .hero {

        padding: 38px 24px;

        min-height: 290px;

    }

    .hero h1 {

        font-size: 31px;

    }

    .auth-brand-panel {

        min-height: 240px;

        padding: 30px 25px;

    }

    .auth-brand-panel h1 {

        font-size: 34px;

    }

    .auth-form-panel {

        padding: 25px 20px;

    }

}

</style>

""", unsafe_allow_html=True)





# --------------------------------------------------

# LOGIN AND SIGNUP

# --------------------------------------------------

if not st.session_state.is_authenticated:



    spacer1, auth_area, spacer2 = st.columns([0.35, 2.3, 0.35])



    with auth_area:

        brand_col, form_col = st.columns([0.95, 1.05], gap="large")



        with brand_col:

            st.html("""
<div class="auth-brand-panel">

    <div style="font-size:48px;">🌍</div>

    <div class="auth-brand-tag">YOUR JOURNEY STARTS HERE</div>

    <h1>GoRove</h1>

    <p style="font-size:18px;font-weight:600;">
        Explore More. Worry Less.
    </p>

    <p>
        Discover destinations, shape memorable journeys
        and keep your travel plans together in one place.
    </p>

    <div style="margin-top:28px;color:#d8e8f1;font-size:13px;">
        ✦ Smart travel planning<br><br>
        ✦ Personal trip workspace<br><br>
        ✦ AI-powered travel assistance
    </div>

</div>
""")



        with form_col:

            st.markdown("<div class='auth-form-panel'>", unsafe_allow_html=True)

            st.markdown("### Welcome to GoRove")

            st.caption("Sign in or create an account to continue.")



            login_tab, signup_tab = st.tabs(["Login", "Create Account"])



            with login_tab:

                with st.form("gorove_login_form", clear_on_submit=False):

                    email = st.text_input(

                        "Email address",

                        placeholder="name@example.com",

                        key="login_email"

                    )

                    password = st.text_input(

                        "Password",

                        type="password",

                        placeholder="Enter your password",

                        key="login_password"

                    )

                    login_button = st.form_submit_button(

                        "Sign in to GoRove",

                        use_container_width=True

                    )



                if login_button:

                    if not email.strip() or not password:

                        st.warning("Please enter your email address and password.")

                    else:

                        success, message, user = auth_service.login_user(

                            email, password

                        )

                        if success:

                            st.session_state.is_authenticated = True

                            st.session_state.current_user = user

                            st.session_state.chat_history = []

                            st.rerun()

                        else:

                            st.error(message)



                st.caption("Forgot password?")



            with signup_tab:

                with st.form("gorove_signup_form", clear_on_submit=False):

                    full_name = st.text_input(

                        "Full name",

                        placeholder="Enter your full name",

                        key="signup_full_name"

                    )

                    signup_email = st.text_input(

                        "Email address",

                        placeholder="name@example.com",

                        key="signup_email"

                    )

                    signup_password = st.text_input(

                        "Create password",

                        type="password",

                        placeholder="At least 8 characters",

                        key="signup_password"

                    )

                    confirm_password = st.text_input(

                        "Confirm password",

                        type="password",

                        placeholder="Re-enter your password",

                        key="signup_confirm_password"

                    )

                    signup_button = st.form_submit_button(

                        "Create my account",

                        use_container_width=True

                    )



                if signup_button:

                    if not full_name.strip():

                        st.warning("Please enter your full name.")

                    elif not signup_email.strip():

                        st.warning("Please enter your email address.")

                    elif not signup_password:

                        st.warning("Please enter a password.")

                    elif signup_password != confirm_password:

                        st.error("Passwords do not match.")

                    else:

                        success, message = auth_service.register_user(

                            full_name,

                            signup_email,

                            signup_password

                        )

                        if success:

                            st.success(

                                "Your account has been created. "

                                "Please open the Login tab to sign in."

                            )

                        else:

                            st.error(message)



            st.markdown(

                "<div class='auth-footnote'>SECURE ACCOUNT ACCESS&nbsp; • &nbsp;GOROVE</div>",

                unsafe_allow_html=True

            )

            st.markdown("</div>", unsafe_allow_html=True)



    st.stop()





# --------------------------------------------------

# CURRENT USER AND ROLE

# --------------------------------------------------

current_user = st.session_state.current_user

user_role = current_user["role"]





# --------------------------------------------------

# ROLE-BASED SIDEBAR NAVIGATION

# --------------------------------------------------

with st.sidebar:

    st.html("""
<div style="text-align:center;padding:12px 5px 25px 5px;">
    <div style="
        font-size:38px;
        background:rgba(255,255,255,.10);
        width:68px;
        height:68px;
        border-radius:18px;
        margin:auto;
        display:flex;
        align-items:center;
        justify-content:center;
    ">🌍</div>

    <div style="font-size:25px;font-weight:800;color:#fff;
        margin-top:13px;letter-spacing:1px;">GOROVE</div>

    <div style="font-size:10px;letter-spacing:1.8px;
        color:#bdcbd8;margin-top:6px;">
        EXPLORE MORE. WORRY LESS.
    </div>
</div>
""")

    st.write(f"Welcome, {current_user['full_name']}!")




    



    if st.button("Logout", use_container_width=True, key="logout_button"):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()



    st.divider()



    if user_role == "admin":

        page = st.radio(

            "Admin navigation",

            [

                "📊 Admin Dashboard",

                "👥 Manage Users",

                "🧳 Manage Trips",

                "📄 Cancellation & Refund Policy",

                "🔒 Privacy Policy",

                "📜 Terms & Conditions",

                "❓ FAQs",

            ],

            label_visibility="collapsed",

            key="admin_navigation"

        )

    else:

        page = st.radio(

            "Customer navigation",

            [

                "🏠 Home",

                "💬 Travel Assistant",

                "🧭 Trip Planner",

                "✈️ Flight Search",

                "🏨 Hotel Search",

                "💰 Budget Planner",

                "📅 Itinerary Generator",

                "🧳 My Trips",

            ],

            label_visibility="collapsed",

            key="customer_navigation"

        )



        st.html("""
<div style="background:rgba(255,255,255,.07);
    border:1px solid rgba(255,255,255,.10);border-radius:11px;
    padding:16px 13px;text-align:left;margin-top:25px;">

    <div style="font-size:11px;color:#cbd5e1;letter-spacing:1px;">
        PLAN WITH CONFIDENCE
    </div>

    <p style="color:#fff;font-size:13px;line-height:1.6;margin:9px 0 0 0;">
        Thoughtful trip planning, from the first idea to the journey home.
    </p>

</div>
""")



page = st.session_state.pop("footer_target_page", page)







# --------------------------------------------------

# AUTO SCROLL TO TOP AFTER FOOTER NAVIGATION

# --------------------------------------------------





if st.session_state.pop("scroll_to_top", False):



    st.components.v1.html(

        """

        <script>

            const doc = window.parent.document;



            function scrollPageTop() {

                const selectors = [

                    'section.main',

                    '[data-testid="stAppViewContainer"]',

                    '[data-testid="stMain"]'

                ];



                selectors.forEach(selector => {

                    const element = doc.querySelector(selector);



                    if (element) {

                        element.scrollTo({

                            top: 0,

                            behavior: 'smooth'

                        });

                    }

                });



                window.parent.scrollTo({

                    top: 0,

                    behavior: 'smooth'

                });

            }



            scrollPageTop();

            setTimeout(scrollPageTop, 300);

            setTimeout(scrollPageTop, 700);

        </script>

        """,

        height=0

    )





# --------------------------------------------------

# ADMIN DASHBOARD

# --------------------------------------------------

if page == "📊 Admin Dashboard":

    st.title("GoRove Admin Dashboard")

    st.markdown(

        '<p class="section-subtitle">A quick overview of customer accounts and travel activity.</p>',

        unsafe_allow_html=True

    )



    db = TravelDatabaseService()

    summary = db.get_admin_summary()



    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Users", summary.get("total_users", 0))

    col2.metric("Active Users", summary.get("active_users", 0))

    col3.metric("Total Trips", summary.get("total_trips", 0))

    col4.metric("Planned Trips", summary.get("planned_trips", 0))



    st.divider()

    st.subheader("Recent Trips")

    trips = db.get_all_trips()



    if trips:

        st.dataframe(trips[:5], use_container_width=True, hide_index=True)

    else:

        st.info("No trips have been created yet.")





# --------------------------------------------------

# ADMIN - MANAGE USERS

# --------------------------------------------------

elif page == "👥 Manage Users":

    st.title("Manage Users")

    st.markdown(

        '<p class="section-subtitle">Review registered accounts and manage customer access.</p>',

        unsafe_allow_html=True

    )



    db = TravelDatabaseService()

    users = db.get_all_users()



    if users:

        st.dataframe(users, use_container_width=True, hide_index=True)



        customers = [u for u in users if u["role"] == "customer"]

        if customers:

            st.divider()

            st.subheader("Update Customer Account")



            selected_id = st.selectbox(

                "Select customer",

                options=[u["user_id"] for u in customers],

                format_func=lambda uid: next(

                    f"{u['full_name']} — {u['email']}"

                    for u in customers if u["user_id"] == uid

                ),

                key="admin_selected_customer"

            )

            selected_user = next(

                u for u in customers if u["user_id"] == selected_id

            )



            selected_status = st.selectbox(

                "Account status",

                ["Active", "Inactive"],

                index=0 if selected_user["is_active"] == 1 else 1,

                key=f"customer_status_{selected_id}"

            )



            if st.button("Update customer status", key="update_customer_status"):

                success = db.update_user_status(

                    selected_id,

                    1 if selected_status == "Active" else 0

                )

                if success:

                    st.success("Customer status updated.")

                    st.rerun()

                else:

                    st.error("Unable to update customer status.")

        else:

            st.info("No customer accounts are registered yet.")

    else:

        st.info("No registered users found.")





# --------------------------------------------------

# ADMIN - MANAGE TRIPS

# --------------------------------------------------

elif page == "🧳 Manage Trips":

    st.title("Manage Trips")

    st.markdown(

        '<p class="section-subtitle">Review customer trip records and update their status.</p>',

        unsafe_allow_html=True

    )



    db = TravelDatabaseService()

    trips = db.get_all_trips()



    if trips:

        st.dataframe(trips, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Update Trip Status")



        selected_trip_id = st.selectbox(

            "Select trip",

            options=[t["trip_id"] for t in trips],

            format_func=lambda tid: next(

                f"Trip #{t['trip_id']} — {t.get('destination_name', 'Destination')}"

                for t in trips if t["trip_id"] == tid

            ),

            key="admin_selected_trip"

        )

        selected_trip = next(

            t for t in trips if t["trip_id"] == selected_trip_id

        )



        statuses = ["Planned", "Confirmed", "Completed", "Cancelled"]

        old_status = selected_trip.get("status", "Planned")

        new_status = st.selectbox(

            "New status",

            statuses,

            index=statuses.index(old_status) if old_status in statuses else 0,

            key=f"trip_status_{selected_trip_id}"

        )



        if st.button("Update trip status", key="update_trip_status"):

            success = db.update_trip_status(selected_trip_id, new_status)

            if success:

                st.success("Trip status updated.")

                st.rerun()

            else:

                st.error("Unable to update trip status.")

    else:

        st.info("No customer trips are available yet.")





# --------------------------------------------------

# CUSTOMER - HOME

# --------------------------------------------------

elif page == "🏠 Home":

    st.html("""
<div class="hero">
    <div class="hero-kicker">A better way to plan your next getaway</div>
    <h1>Find your next favourite place.</h1>
    <p>
        From choosing a destination to organising the details,
        GoRove brings your travel planning together in one place.
    </p>
</div>
""")



    st.title("Welcome to GoRove")

    st.markdown(

        '<p class="section-subtitle">A little inspiration for wherever you want to go next.</p>',

        unsafe_allow_html=True

    )



    col1, col2, col3 = st.columns(3)

    with col1:

        st.html("""

        <div class="info-card"><div style="font-size:27px;">🗺️</div>

        <h3>Explore destinations</h3>

        <p>Discover places to visit, local highlights and useful travel information.</p></div>

        """)

    with col2:

        st.html("""

        <div class="info-card"><div style="font-size:27px;">🧭</div>

        <h3>Plan your journey</h3>

        <p>Put together a trip that suits your dates, interests and travel style.</p></div>

        """)

    with col3:

        st.html("""

        <div class="info-card"><div style="font-size:27px;">₹</div>

        <h3>Keep track of costs</h3>

        <p>Estimate your travel expenses and make decisions that fit your budget.</p></div>

        """)



    st.write("")

    st.subheader("Start planning")

    with st.container(border=True):

        st.markdown("Tell us a little about the trip you have in mind.")

        c1, c2 = st.columns(2)



        with c1:

            home_destination = st.text_input(

                "Where would you like to go?",

                placeholder="For example, Goa, Dubai or Bali",

                key="home_destination"

            )

            home_start = st.date_input(

                "Departure date",

                value=date.today(),

                key="home_departure_date"

            )



        with c2:

            home_travellers = st.number_input(

                "Number of travellers", min_value=1, max_value=20,

                value=2, key="home_travellers"

            )

            home_budget = st.number_input(

                "Estimated total budget (₹)", min_value=1000,

                value=30000, step=1000, key="home_budget"

            )



        if st.button("Continue to Trip Planner", key="home_plan"):

            if home_destination.strip():

                st.session_state["trip_destination"] = home_destination.strip()

                st.session_state["trip_travellers"] = int(home_travellers)

                st.session_state["trip_budget"] = int(home_budget)

                st.session_state["trip_start_date"] = home_start

                st.session_state["trip_end_date"] = None

                st.session_state["trip_research_result"] = None

                st.success("Trip details added. Open Trip Planner to complete your dates.")

            else:

                st.warning("Please enter a destination.")



    st.write("")

    st.subheader("Places worth discovering")

    destinations = [

        ("Goa", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=700&q=80"),

        ("Kerala", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=700&q=80"),

        ("Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=700&q=80"),

        ("Bali", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=700&q=80"),

    ]

    cols = st.columns(4)

    for col, (name, image_url) in zip(cols, destinations):

        with col:

            st.html(f"""

            <div class="destination-card" style="background-image:url('{image_url}');">

                <h3>{name}</h3>

            </div>

            """)





    # --------------------------------------------------

    # GOROVE FLOATING HOME CHATBOT

    # --------------------------------------------------



    st.markdown("""

    <style>

    /* Floating Chat Icon Position */

    .st-key-gorove_home_chat {

        position: fixed !important;

        bottom: 25px !important;

        right: 25px !important;

        z-index: 99999 !important;

    }



    /* Chat Icon Design */

    .st-key-gorove_home_chat button {

        width: 65px !important;

        height: 65px !important;

        min-width: 65px !important;

        border-radius: 50% !important;

        background-color: #087EAD !important;

        color: white !important;

        border: 3px solid white !important;

        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.30) !important;

        font-size: 32px !important;

        font-weight: bold !important;

    }



    /* Hide Enter-to-submit helper text */

    .st-key-gorove_home_chat [data-testid="InputInstructions"] {

        display: none !important;

    }

    </style>

    """, unsafe_allow_html=True)



    if "home_chat_history" not in st.session_state:

        st.session_state.home_chat_history = []



    with st.popover("💬", help="Chat with GoRove", key="gorove_home_chat"):



        st.markdown("### 🌍 GoRove AI Assistant")

        st.caption("Your personal travel companion!")



        # Display Chat History

        for message in st.session_state.home_chat_history:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])



        # Chat Input Form

        with st.form("gorove_home_chat_form", clear_on_submit=True):



            home_chat_input = st.text_input(

                "Your travel question",

                placeholder="Ask me about your next trip..."

            )



            home_chat_send = st.form_submit_button("Send")



        # Process User Question

        if home_chat_send and home_chat_input.strip():



            st.session_state.home_chat_history.append({

                "role": "user",

                "content": home_chat_input

            })



            if "agent_manager" not in st.session_state:

                st.session_state.agent_manager = TravelAgentManager()



            try:

                with st.spinner("GoRove is thinking..."):



                    reply = st.session_state.agent_manager.process_request(
                        home_chat_input,
                        conversation_history=st.session_state.home_chat_history[:-1]
                    )



                reply = str(reply) if reply else (

                    "Sorry, I couldn't prepare an answer. Please try again."

                )



                # Remove Internal Agent Labels

                for label in [

                    "TravelAssistantAgent:",

                    "Travel Assistant Agent:",

                    "Agent Manager:",

                    "Multi-Agent Response",

                ]:

                    reply = reply.replace(label, "")



                st.session_state.home_chat_history.append({

                    "role": "assistant",

                    "content": reply

                })



            except Exception:

                st.session_state.home_chat_history.append({

                    "role": "assistant",

                    "content": "Sorry, I couldn't process your request. Please try again."

                })



            st.rerun()









# --------------------------------------------------
# CUSTOMER - TRAVEL ASSISTANT
# --------------------------------------------------

elif page == "💬 Travel Assistant":

    import re

    st.title("Travel Assistant")

    st.markdown(
        '<p class="section-subtitle">Have a travel question? Let’s work it out together.</p>',
        unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "agent_manager" not in st.session_state:
        st.session_state.agent_manager = TravelAgentManager()

    st.caption(
        "Ask about destinations, attractions, travel budgets, itineraries, flights or hotels."
    )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Where are you thinking of travelling?"
    )

    if user_input and user_input.strip():

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner(
                "Putting together helpful travel suggestions..."
            ):

                try:

                    assistant_reply = (
                        st.session_state.agent_manager.process_request(
                            user_input,
                            conversation_history=st.session_state.chat_history[:-1]
                        )
                    )

                    if assistant_reply is None:
                        assistant_reply = (
                            "I’m sorry, I couldn’t prepare an answer just now. "
                            "Please try again."
                        )
                    else:
                        assistant_reply = str(assistant_reply)

                    # Remove internal agent labels
                    internal_labels = [
                        "Destination Research Agent",
                        "Itinerary Planner Agent",
                        "Travel Assistant Agent",
                        "Agent Manager:",
                        "Agents Activated:",
                        "Multi-Agent Response",
                        "Database activities are scheduled sequentially without repeating them.",
                        "Activity timings, availability and travel distances are not live or confirmed."
                    ]

                    cleaned_lines = []

                    for line in assistant_reply.splitlines():

                        if not any(
                            label in line for label in internal_labels
                        ):
                            cleaned_lines.append(line)

                    assistant_reply = "\n".join(cleaned_lines)

                    # Remove Information Source section
                    assistant_reply = re.sub(
                        r"(?ims)^#{1,6}\s*Information Source\s*\n.*?(?=^#{1,6}\s|\Z)",
                        "",
                        assistant_reply
                    )

                    # Remove unwanted database note
                    assistant_reply = re.sub(
                        r"(?is)\*{0,2}Note:\*{0,2}\s*\*{0,2}Database activities are scheduled sequentially without repeating them\.?\*{0,2}",
                        "",
                        assistant_reply
                    )

                    # Remove activity availability disclaimer
                    assistant_reply = re.sub(
                        r"(?is)Activity timings,\s*availability,?\s*and travel distances are not live or confirmed\.?",
                        "",
                        assistant_reply
                    )

                    # Remove excessive blank lines
                    assistant_reply = re.sub(
                        r"\n{3,}",
                        "\n\n",
                        assistant_reply
                    )

                    # Apply GoRove branding
                    assistant_reply = assistant_reply.replace(
                        "AI Travel Planner",
                        "GoRove"
                    )

                    # Display response
                    st.markdown(assistant_reply)

                    # Save assistant response
                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": assistant_reply
                        }
                    )

                except Exception as e:

                    st.error(
                        "Sorry, I couldn't process that request at the moment. "
                        "Please try again in a little while."
                    )

                    print("Travel Assistant Error:", repr(e))

    if st.button("Clear conversation", key="clear_chat"):

        st.session_state.chat_history = []

        st.rerun()



# --------------------------------------------------

# CUSTOMER - TRIP PLANNER

# --------------------------------------------------

elif page == "🧭 Trip Planner":

    st.title("Trip Planner")

    st.markdown(

        '<p class="section-subtitle">Shape your trip around the places and experiences you enjoy.</p>',

        unsafe_allow_html=True

    )



    with st.container(border=True):

        destination = st.text_input(

            "Destination",

            value=st.session_state.get("trip_destination", ""),

            key="planner_destination"

        )



        c1, c2 = st.columns(2)

        with c1:

            start_date = st.date_input(

                "Start date",

                value=st.session_state.get("trip_start_date") or date.today(),

                key="planner_start"

            )

        with c2:

            end_date = st.date_input(

                "End date",

                value=st.session_state.get("trip_end_date") or date.today(),

                key="planner_end"

            )



        c3, c4 = st.columns(2)

        with c3:

            travellers = st.number_input(

                "Number of travellers", min_value=1, max_value=20,

                value=int(st.session_state.get("trip_travellers", 2)),

                key="planner_travellers"

            )

        with c4:

            budget = st.number_input(

                "Total budget (₹)", min_value=1000,

                value=int(st.session_state.get("trip_budget", 30000)),

                step=1000, key="planner_budget"

            )



        travel_options = [

            "Adventure", "Relaxation", "Family Vacation",

            "Honeymoon", "Cultural Exploration", "Business Travel"

        ]

        saved_travel_type = st.session_state.get("trip_travel_type", "Relaxation")

        travel_index = (

            travel_options.index(saved_travel_type)

            if saved_travel_type in travel_options else 1

        )

        travel_type = st.selectbox(

            "What kind of trip are you planning?",

            travel_options,

            index=travel_index,

            key="planner_travel_type"

        )



        if st.button("Create my trip plan", key="create_trip_plan"):

            if not destination.strip():

                st.warning("Please enter a destination.")

            elif end_date < start_date:

                st.error("End date cannot be earlier than start date.")

            else:

                st.session_state["trip_destination"] = destination.strip()

                st.session_state["trip_travellers"] = int(travellers)

                st.session_state["trip_budget"] = int(budget)

                st.session_state["trip_start_date"] = start_date

                st.session_state["trip_end_date"] = end_date

                st.session_state["trip_travel_type"] = travel_type

                st.session_state["trip_research_result"] = None



                research_prompt = f"""

                Find information about {destination.strip()}.

                User preference: {travel_type}.

                Return a destination overview, popular attractions,

                and useful visitor tips using the local database.

                """

                try:

                    with st.spinner("Finding useful information for your trip..."):

                        agent_manager = TravelAgentManager()

                        result = agent_manager.process_request(research_prompt)

                        st.session_state["trip_research_result"] = result

                    st.success("Your destination recommendations are ready.")

                except Exception:

                    st.error(

                        "We couldn't prepare destination recommendations right now. "

                        "Please try again."

                    )



        if st.session_state.get("trip_research_result"):

            st.divider()

            st.subheader("Your trip details")

            st.write("**Destination:**", st.session_state["trip_destination"])

            st.write("**Travel preference:**", st.session_state.get("trip_travel_type", ""))

            st.write("**Travellers:**", st.session_state["trip_travellers"])

            st.write("**Budget:**", f"₹{st.session_state['trip_budget']:,}")

            st.subheader("Destination recommendations")

            st.markdown(str(st.session_state["trip_research_result"]))





# --------------------------------------------------

# CUSTOMER - FLIGHT SEARCH

# --------------------------------------------------

elif page == "✈️ Flight Search":

    st.title("Flight Search")





    with st.container(border=True):

        c1, c2 = st.columns(2)

        with c1:

            from_city = st.text_input("From", placeholder="Chennai")

        with c2:

            to_city = st.text_input("To", placeholder="Goa")



        c3, c4 = st.columns(2)

        with c3:

            flight_date = st.date_input("Departure date", key="flight_date")

        with c4:

            passengers = st.number_input(

                "Passengers", min_value=1, max_value=9, value=1

            )



        flight_class = st.selectbox(

            "Travel class",

            ["Economy", "Premium Economy", "Business", "First Class"]

        )



        if st.button("Search flights"):

            if not from_city.strip() or not to_city.strip():

                st.warning("Please enter both departure and destination cities.")

            else:

                try:

                    db = TravelDatabaseService()

                    flights = db.search_flights(from_city.strip(), to_city.strip())

                    if flights:

                        st.success(

                            f"Found {len(flights)} flight option(s) from "

                            f"{from_city} to {to_city}."

                        )

                        st.dataframe(

                            flights, use_container_width=True, hide_index=True

                        )



                    else:

                        st.warning(

                            f"No flight options were found for {from_city} to "

                            f"{to_city} in the sample database."

                        )

                except Exception:

                    st.error("Flight search is unavailable. Please try again.")





# --------------------------------------------------

# CUSTOMER - HOTEL SEARCH

# --------------------------------------------------

elif page == "🏨 Hotel Search":

    st.title("Hotel Search")

    st.markdown(

        '<p class="section-subtitle">Explore accommodation details available for your destination.</p>',

        unsafe_allow_html=True

    )



    with st.container(border=True):

        hotel_city = st.text_input(

            "Destination / City", placeholder="For example, Goa"

        )

        c1, c2 = st.columns(2)

        with c1:

            checkin = st.date_input("Check-in date", key="hotel_checkin")

        with c2:

            checkout = st.date_input("Check-out date", key="hotel_checkout")



        c3, c4 = st.columns(2)

        with c3:

            guests = st.number_input("Guests", min_value=1, max_value=20, value=2)

        with c4:

            rooms = st.number_input("Rooms", min_value=1, max_value=10, value=1)



        hotel_type = st.selectbox(

            "Accommodation type", ["Any", "Hotel", "Resort", "Villa", "Budget Stay"]

        )



        if st.button("Search hotels"):

            if not hotel_city.strip():

                st.warning("Please enter a destination.")

            elif checkout <= checkin:

                st.error("Check-out date must be after check-in date.")

            else:

                try:

                    db = TravelDatabaseService()

                    hotels = db.get_hotels(hotel_city.strip())

                    if hotels:

                        st.success(

                            f"Found {len(hotels)} accommodation option(s) in {hotel_city}."

                        )

                        for hotel in hotels:

                            with st.container(border=True):

                                st.markdown(f"### {hotel['hotel_name']}")

                                st.write("**Location:**", hotel["address"])

                                st.write(

                                    f"**Price per night:** ₹{hotel['price_per_night']}"

                                )

                                st.write(f"**Rating:** {hotel['rating']}/5")



                    else:

                        st.warning(

                            f"No accommodation options were found for {hotel_city} "

                            "in the sample database."

                        )

                except Exception:

                    st.error("Hotel search is unavailable. Please try again.")





# --------------------------------------------------

# CUSTOMER - BUDGET PLANNER

# --------------------------------------------------

elif page == "💰 Budget Planner":

    st.title("Travel Budget Planner")

    st.markdown(

        '<p class="section-subtitle">Build an estimated budget for the journey you have in mind.</p>',

        unsafe_allow_html=True

    )



    with st.container(border=True):

        st.subheader("Your trip details")

        destination = st.text_input(

            "Destination", placeholder="For example, Goa", key="budget_destination"

        )

        c1, c2 = st.columns(2)

        with c1:

            days = st.number_input(

                "Trip duration (days)", min_value=1, max_value=30, value=3

            )

        with c2:

            travellers = st.number_input(

                "Number of travellers", min_value=1, max_value=20, value=2

            )

        budget = st.number_input(

            "Your total budget (₹)", min_value=1000, value=30000, step=1000

        )



        if st.button("Estimate trip expenses"):

            if not destination.strip():

                st.warning("Please enter a destination.")

            else:

                try:

                    agent = BudgetAnalystAgent()

                    prompt = (

                        f"Estimate budget for a {days}-day "

                        f"{destination.strip()} trip for {travellers} people "

                        f"with a budget of ₹{budget}"

                    )

                    result = agent.get_response(prompt)

                    st.divider()

                    st.subheader("Estimated trip expenses")

                    st.markdown(result)

                except Exception:

                    st.error(

                        "We couldn't prepare the budget estimate right now. "

                        "Please try again."

                    )





# --------------------------------------------------

# CUSTOMER - ITINERARY GENERATOR

# --------------------------------------------------

elif page == "📅 Itinerary Generator":

    st.title("Itinerary Generator")

    st.markdown(

        '<p class="section-subtitle">Create a day-by-day outline for your destination.</p>',

        unsafe_allow_html=True

    )



    destination = st.text_input(

        "Destination",

        value=st.session_state.get("trip_destination", ""),

        key="itinerary_destination"

    )

    days = st.number_input(

        "Number of days", min_value=1, max_value=14, value=3

    )

    travel_style = st.selectbox(

        "Travel style", ["Relaxed", "Adventure", "Family", "Cultural", "Luxury"]

    )



    if st.button("Create my itinerary"):

        if not destination.strip():

            st.warning("Please enter a destination.")

        else:

            try:

                agent = ItineraryPlannerAgent()

                prompt = (

                    f"Create a {int(days)}-day {travel_style} itinerary "

                    f"for {destination.strip()}."

                )

                result = agent.get_response(prompt)

                st.divider()

                st.subheader(f"{days}-day plan for {destination.strip()}")

                st.markdown(result)

            except Exception:

                st.error(

                    "We couldn't create the itinerary right now. Please try again."

                )





# --------------------------------------------------

# CUSTOMER - MY TRIPS

# --------------------------------------------------

elif page == "🧳 My Trips":

    st.title("My Trips")

    st.markdown(

        '<p class="section-subtitle">Keep the details of your planned journeys together.</p>',

        unsafe_allow_html=True

    )



    db = TravelDatabaseService()

    user_id = current_user["user_id"]



    destination = st.session_state.get("trip_destination")

    budget = st.session_state.get("trip_budget")

    start_date = st.session_state.get("trip_start_date")

    end_date = st.session_state.get("trip_end_date")



    if destination and start_date and end_date and budget is not None:

        st.subheader("Current Trip")

        st.write("**Destination:**", destination)

        st.write("**Start Date:**", start_date)

        st.write("**End Date:**", end_date)

        st.write("**Travel Preference:**", st.session_state.get("trip_travel_type", ""))

        st.write("**Travellers:**", st.session_state.get("trip_travellers", 1))

        st.write("**Budget:**", f"₹{budget:,}")



        if st.button("Save this trip", key="save_trip_database"):

            success, message = db.save_trip(

                user_id,

                current_user["full_name"],

                destination,

                str(start_date),

                str(end_date),

                budget

            )

            if success:

                st.success(message)

                st.rerun()

            else:

                st.error(message)

    else:

        st.info(

            "You haven't completed a trip plan yet. "

            "Open Trip Planner, enter your dates and create your plan."

        )



    st.divider()

    st.subheader("My Saved Trips")

    saved_trips = db.get_user_trips(user_id)



    if saved_trips:

        st.dataframe(saved_trips, use_container_width=True, hide_index=True)

    else:

        st.info("You haven't saved any trips yet.")





# --------------------------------------------------

# CUSTOMER - MY PROFILE

# --------------------------------------------------

elif page == "👤 My Profile":

    st.title("My Profile")

    st.markdown(

        '<p class="section-subtitle">Your GoRove account information.</p>',

        unsafe_allow_html=True

    )



    profile = auth_service.get_user_by_id(current_user["user_id"])

    if profile:

        with st.container(border=True):

            st.subheader("Account Information")

            st.write("**Full Name:**", profile["full_name"])

            st.write("**Email Address:**", profile["email"])

            st.write("**Account Role:**", profile["role"].title())

            st.write(

                "**Account Status:**",

                "Active" if profile["is_active"] == 1 else "Inactive"

            )

            st.write("**Joined On:**", profile["created_at"])

    else:

        st.error("Profile information could not be found.")







# --------------------------------------------------

# CUSTOMER / ADMIN - POLICY AND HELP PAGES

# --------------------------------------------------

elif page == "📄 Cancellation & Refund Policy":

    st.title("Cancellation & Refund Policy")



    st.subheader("1. General cancellation rules")

    st.markdown("""

    - Cancellation conditions depend on the airline, hotel, activity provider or other travel supplier.

    - Always check the cancellation deadline and charges shown by the supplier before confirming a reservation.

    - A booking may offer free cancellation, partial refund or no refund, depending on its fare or rate conditions.

    - Cancellation requests should be submitted through the platform or supplier that accepted the booking.

    """)



    st.subheader("2. Flight cancellations")

    st.markdown("""

    - Airline tickets are subject to the airline's fare rules and applicable regulations.

    - Cancellation charges, airline service fees and eligible refund amounts can vary by ticket type and time of cancellation.

    - If an airline cancels or significantly changes a flight, available options are determined by the airline and applicable passenger-rights rules.

    """)



    st.subheader("3. Hotel cancellations")

    st.markdown("""

    - Hotel reservations follow the individual property's cancellation policy.

    - Free cancellation is available only when the reservation terms explicitly provide it and the request is made before the stated deadline.

    - Non-refundable rates may not qualify for a refund. No-show and late-cancellation charges may also apply.

    """)



    st.subheader("4. Refunds")

    st.markdown("""

    - Refund eligibility and the amount payable are decided under the applicable supplier's booking terms and relevant law.

    - Where a refund is approved, it is generally returned through the original payment method or the supplier's stated process.

    - The time taken for a refund to appear can vary by supplier, bank and payment provider.

    - Any cancellation fees, non-refundable amounts or other permitted deductions may be applied by the supplier.

    """)



    st.subheader("5. Changes, cancellations by suppliers and no-shows")

    st.markdown("""

    - Changes to travel dates, passenger details or accommodation dates depend on supplier rules and availability.

    - If a supplier cancels a service, contact that supplier for the available alternatives or refund process.

    - If a traveller does not arrive or misses a service, the supplier's no-show conditions may apply.

    """)



    st.subheader("6. Before you confirm a booking")

    st.markdown("""

    Please read the final price, cancellation deadline, refund conditions, baggage or stay rules, and any additional fees shown by the booking provider. Keep your booking confirmation and cancellation reference for future communication.

    """)





elif page == "🔒 Privacy Policy":

    st.title("Privacy Policy")



    st.markdown("""

    **1. Information used**



    GoRove may use account details such as your name and email address, the trip details you enter, and information you provide while using travel-planning features.



    **2. How information is used**



    Information is used to provide account access, display your profile, save and show your trips, and generate travel-planning suggestions.



    **3. Storage and access**



    Account and saved-trip information is stored in the application's database. Access to administrative features is restricted by the account role. Chat messages are maintained in the active app session in this project.



    **4. Sharing**



    GoRove does not intentionally publish your account or trip details. If external services are connected in a future version, their role and data handling must be explained here before use.



    **5. Security**



    The project uses password hashing for account passwords. No internet-connected service can guarantee absolute security, so users should choose a unique password and keep their login details private.



    **6. Your choices and contact**



    For account or data-related questions, contact the GoRove project administrator through the support details provided by the project owner.

    """)





elif page == "📜 Terms & Conditions":

    st.title("Terms & Conditions")



    st.markdown("""

    **1. Use of the service**



    GoRove is currently a travel-planning project that helps users organise trip ideas, view sample travel information and generate suggested plans.



    **2. Accuracy of information**



    Destination information, sample flight and hotel records, estimated budgets and generated itineraries may be incomplete or out of date. Confirm prices, opening hours, availability, travel requirements and supplier conditions independently before making travel decisions.



    **3. No booking or payment service at present**



    The current project does not issue flight tickets, confirm hotel reservations, collect travel payments or process refunds. Any booking made through a separate provider is governed by that provider's terms.



    **4. User accounts**



    Users are responsible for keeping their login credentials confidential and for providing accurate account information. Administrators may restrict accounts in accordance with the project's account-management rules.



    **5. Appropriate use**



    Users must not misuse the application, attempt unauthorised access, or submit unlawful or harmful content.



    **6. Updates**



    These terms may be revised as the project gains features or connects to external travel providers. The published version should be reviewed before public or commercial launch.

    """)





elif page == "❓ FAQs":

    st.title("Frequently Asked Questions")



    st.markdown(

        '<p class="section-subtitle">Quick answers to common questions about GoRove.</p>',

        unsafe_allow_html=True

    )



    with st.expander("Can I book flights or hotels directly through GoRove?"):

        st.write("Not currently. The project displays sample information; live booking and payment integrations are not connected.")



    with st.expander("Are flight and hotel prices live?"):

        st.write("No. Results currently come from the local sample database and should not be treated as live prices or availability.")



    with st.expander("Can I save my trip?"):

        st.write("Yes. Complete your trip details in Trip Planner, then open My Trips and choose Save this trip.")



    with st.expander("How do I cancel a booking?"):

        st.write("If you booked through another provider, use that provider's website or support channel and follow the cancellation terms in your confirmation.")



    with st.expander("Does GoRove process refunds?"):

        st.write("No. GoRove does not currently collect booking payments or process refunds. Refunds for external bookings are handled by the relevant provider.")



    with st.expander("I cannot access my account. What should I do?"):

        st.write("Use the account credentials you registered with. Password recovery is planned for a later update; contact the project administrator if you need assistance.")





# --------------------------------------------------

# SIMPLE FOOTER - PLAIN TEXT LINKS (NO CARDS)

# --------------------------------------------------

def _go_to_footer_page(target_page):

    st.session_state["footer_target_page"] = target_page

    st.session_state["scroll_to_top"] = True





if user_role == "customer" and st.session_state.get("customer_navigation") == "🏠 Home":



    st.markdown("""

    <style>

    .st-key-gorove_footer div[data-testid="stButton"] button {

        background: transparent !important;

        border: none !important;

        box-shadow: none !important;

        color: #285f78 !important;

        padding: 4px 0 !important;

        justify-content: flex-start !important;

        font-weight: 500 !important;

    }



    .st-key-gorove_footer div[data-testid="stButton"] button:hover {

        color: #173e55 !important;

        text-decoration: underline !important;

    }

    </style>

    """, unsafe_allow_html=True)



    with st.container(key="gorove_footer"):

        st.html("""
<div class="gorove-footer-brand">
    <strong>🌍 GoRove</strong>
    <div>Explore More. Worry Less.</div>
</div>
""")

        footer_cols = st.columns(4)



        # QUICK LINKS

        with footer_cols[0]:

            st.markdown(

                '<div class="gorove-footer-heading">Quick Links</div>',

                unsafe_allow_html=True

            )



            quick_links = [

                ("Home", "🏠 Home"),

                ("Travel Assistant", "💬 Travel Assistant"),

                ("Trip Planner", "🧭 Trip Planner"),

                ("Flight Search", "✈️ Flight Search"),

                ("Hotel Search", "🏨 Hotel Search"),

                ("Budget Planner", "💰 Budget Planner"),

                ("Itinerary Generator", "📅 Itinerary Generator"),

                ("My Trips", "🧳 My Trips"),

                ("My Profile", "👤 My Profile"),

            ]



            for label, target in quick_links:

                st.button(

                    label,

                    key="footer_link_" + target,

                    on_click=_go_to_footer_page,

                    args=(target,)

                )



        # POLICIES

        with footer_cols[1]:

            st.markdown(

                '<div class="gorove-footer-heading">Policies</div>',

                unsafe_allow_html=True

            )



            policy_links = [

                ("Cancellation & Refund", "📄 Cancellation & Refund Policy"),

                ("Privacy Policy", "🔒 Privacy Policy"),

                ("Terms & Conditions", "📜 Terms & Conditions"),

                ("FAQs", "❓ FAQs"),

            ]



            for label, target in policy_links:

                st.button(

                    label,

                    key="footer_policy_" + target,

                    on_click=_go_to_footer_page,

                    args=(target,)

                )



        # TALK TO US

        with footer_cols[2]:

            st.markdown(

                '<div class="gorove-footer-heading">Talk to Us</div>',

                unsafe_allow_html=True

            )



            st.markdown(

                '<div class="gorove-footer-note">'

                'Customer Support<br>'

                '<a href="mailto:akila97aj@gmail.com">akila97aj@gmail.com</a><br>'

                '+91 12345 00000'

                '</div>',

                unsafe_allow_html=True

            )



        # SOCIAL

        with footer_cols[3]:

            st.markdown(

                '<div class="gorove-footer-heading">Social</div>',

                unsafe_allow_html=True

            )



            st.markdown(

                '<div class="gorove-footer-note">'

                'Facebook<br>Instagram<br>LinkedIn<br>YouTube'

                '</div>',

                unsafe_allow_html=True

            )
