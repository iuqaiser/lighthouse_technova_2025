#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 12:51:10 2025

@author: angelinachen
"""
import streamlit as st
import pandas as pd 

# -------------------------------
# Sidebar Navigation
# -------------------------------

st.set_page_config(layout="wide") 


st.markdown(
    """
    <style>
    /* Sidebar width */
    [data-testid="stSidebar"] {
        background-color: #dbcaab !important;
        border-right: 3px solid #912a04;
    }

    /* Selected radio button item */
    div[role="radiogroup"] label[data-baseweb="radio"] > div[data-testid="stMarkdownContainer"] {
        transition: background-color 0.2s;
        border-radius: 8px;
        padding: 5px 10px;
    }

    /* Active page (checked input) */
    div[role="radiogroup"] label[data-baseweb="radio"] > input:checked + div[data-testid="stMarkdownContainer"] {
        background-color: #912a04 !important;
        color: white !important;
        font-weight: bold;
    }

    /* Hover effect for unselected items */
    div[role="radiogroup"] label[data-baseweb="radio"]:not(:has(input:checked)) > div[data-testid="stMarkdownContainer"]:hover {
        background-color: #c78b72;
        color: white;
    }

    /* Center main page content regardless of sidebar */
    .appview-container .main .block-container {
        max-width: 900px;   /* adjust width as needed */
        padding-left: 3rem; /* space from sidebar */
        padding-right: 3rem;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.title("🧭 Navigation")

menu_items = [("Homepage", "home"), ("Finder", "about")]

# Get current page from query params
current_page = st.query_params.get("page", ["home"])[0]

page_names = [page_name for _, page_name in menu_items]
current_index = page_names.index(current_page)

# Sidebar radio menu
selected_index = st.sidebar.radio(
    "Menu",
    range(len(menu_items)),
    index=current_index,
    format_func=lambda i: menu_items[i][0]
)

# Update query params if sidebar selection changes
if selected_index != current_index:
    st.query_params = {"page": [menu_items[selected_index][1]]}

page = menu_items[selected_index][1]

# -------------------------------
# Home Page
# -------------------------------


if page == "home":
    # Background just for Home page
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #c2d3ed;  /* Light lavender */
        }
        header[data-testid="stHeader"] {
            background-color: #c2d3ed;  /* Lavender top bar */
        }
        header[data-testid="stHeader"]::before {
            box-shadow: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        st.title("⚓️💡🌊🚢")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Lighthouse</h1>", unsafe_allow_html=True)
        st.write("<p style='text-align:center; font-size:20px; font-weight:400; color:#333;'>Where hope is only one click away.</p>", unsafe_allow_html=True)
        

    # CSS specifically for homepage button
    st.markdown(
    """
    <style>
    /* Only affect the first stButton on the page */
    div.stButton > button:first-child {
        background-color: #b8b8f5;   /* Lavender background */
        color: black;                /* Text color */
        font-size: 20px;
        font-weight: bold;
        padding: 15px 40px;
        border-radius: 12px;
        border: 3px solid #9370DB;   /* Lavender border */
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:first-child:hover {
        background-color: #5a5a9e;   /* Darker lavender */
        color: white;
        border: 3px solid #4B0082;   /* Darker border on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("Start your healing journey here"):
            st.query_params = {"page": ["about"]}

# -------------------------------
# About Us Page
# -------------------------------
elif page == "about":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fad99b;  
        }
        header[data-testid="stHeader"] {
            background-color: #fad99b;  
        }
        header[data-testid="stHeader"]::before {
            box-shadow: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page title in rounded box
    st.markdown("""
        <div style="
            background-color:#f5eada;
            border-radius:20px;
            padding:20px;
            text-align:center;
            font-size:48px;
            font-weight:bold;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            margin-bottom:20px;
        ">
            💭 How are you feeling today?
        </div>
    """, unsafe_allow_html=True)
    # Search bar in rounded box
    search_query = st.text_input("🖊️ Type into the search bar and I’ll help match you with a mental health provider, or use the navigation filters to explore options that fit your needs.", "")
    if search_query:
        st.write(f"You searched for: **{search_query}**")

    #BUTTON 
    # Small top-left button in a rounded box
    st.markdown('<div class="home-btn">', unsafe_allow_html=True)
    if st.button("Go back to Homepage", key="about_home_btn"):
        st.query_params = {"page": ["home"]}
    st.markdown('</div>', unsafe_allow_html=True)
 
    

    st.markdown("</div>", unsafe_allow_html=True)

  


    # Columns for content and map
    #col1, col2 = st.columns([2,4])

   # with col1:
    st.markdown("""
            <div style="
                background-color:#f5eada;
            border-radius:15px;
            padding:15px;
            text-align:center;
            font-size:28px;
            font-weight:semibold;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            margin-bottom:10px;
            ">
            Best Matches
        </div>
    """, unsafe_allow_html=True)


    # Placeholder for the table
table_placeholder = st.empty()

# Example: no results yet
if "results" not in st.session_state:
    st.markdown("""
        <div style="
            background-color:#fff8ef;
            border: 2px dashed #c78b72;
            border-radius:12px;
            padding:20px;
            text-align:center;
            color:#555;
            font-size:18px;
            margin-top:15px;
        ">
        ℹ️ Use the search bar or filters to see results.
        </div>
    """, unsafe_allow_html=True)
else:
    # Show query results
        table_placeholder.dataframe(st.session_state["results"], use_container_width=True)

# --- Search header box ---
st.markdown("""
    <div style="
        background-color:#f5eada;
        border-radius:15px;
        padding:15px;
        text-align:center;
        font-size:28px;
        font-weight:600;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        margin-bottom:20px;
    ">
    🔎 Find a provider near you:
    </div> 
""", unsafe_allow_html=True)

# --- Search bar + button ---
st.text_input("Search by location", key="search_query")
if st.button("Run Search"):
    # TODO: Replace with Snowflake query
    df = pd.DataFrame({
        "Provider": ["Alice", "Bob"],
        "Specialty": ["CBT", "DBT"],
        "Location": ["Toronto", "Vancouver"]
    })
    st.session_state["results"] = df

# --- Results section (scoped only to this area) ---
table_placeholder = st.empty()
with table_placeholder.container():
    if "results" in st.session_state:
        st.dataframe(st.session_state["results"], use_container_width=True)
    else:
        st.markdown("""
            <div style="
                background-color:#fff8ef;
                border: 2px dashed #c78b72;
                border-radius:12px;
                padding:20px;
                text-align:center;
                color:#555;
                font-size:18px;
                margin-top:15px;
            ">
            ℹ️ Use the search bar or filters to see results.
            </div>
        """, unsafe_allow_html=True)
        
        # Map without pandas
    uw_map_data = [{"lat": 43.4723, "lon": -80.5449}]
    st.map(uw_map_data)

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer in rounded box
    col1, col2, col3 = st.columns([2,1,2])
    with col2: 
        st.write("Team - Angie and Iman")

# -------------------------------
# Sidebar Filters (only for About Us page)
# -------------------------------
if page == "about":
    st.sidebar.markdown("---")  # Separator line
    st.sidebar.subheader("Filter Providers 🩺")

    # 1️⃣ Specialization in specific mental health conditions
    mh_conditions = st.sidebar.multiselect(
        "Common specialization in mental health conditions",
        options=[
            "Depression", "Anxiety", "PTSD", "Bipolar", "ADHD", "Eating Disorders", "OCD"
        ]
    )

    # 2️⃣ Type of therapy
    therapy_type = st.sidebar.multiselect(
        "Type of therapy",
        options=[
            "CBT", "DBT", "Group therapy (including AA)", "One-on-one"
        ]
    )

    # 3️⃣ Specialization in traumas / life situations
    trauma_support = st.sidebar.multiselect(
        "Common specialization in trauma / life situations",
        options=[
            "LGBTQ+ support", "Religious support", "Domestic/sexual violence trauma",
            "Addiction support", "Grief counseling", "Career / life coaching"
        ]
    )

    # 4️⃣ Provider gender
    provider_gender = st.sidebar.radio(
        "Healthcare provider gender",
        options=["Any", "Male", "Female", "Non-binary", "Other"]
    )

    # 5️⃣ Insurance and hourly rate
    insurance_options = st.sidebar.multiselect(
        "Common insurance accepted",
        options=["OHIP", "Greenshield", "Manulife", "Blue Cross", "Canada Life", "Sun Life", "Desjardins", "Other"]
    )
    hourly_rate = st.sidebar.slider(
        "Hourly rate ($)", 0, 500, (0, 200)
    )
    
    search_clicked = st.sidebar.button("🔍 Search Providers")

    # -------------------------------
    # Display selected filters in styled boxes
    # -------------------------------
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Selected Filters")

  
    def render_filter_box(label, value):
        """Render a filter selection in a rounded box"""
        if value:
            st.sidebar.markdown(f"""
                <div style="
                    background-color:#ffffff;
                    border-radius:12px;
                    padding:10px;
                    margin-bottom:8px;
                    box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
                    font-size:14px;
                ">
                    <strong>{label}:</strong> {value}
                </div>
            """, unsafe_allow_html=True) 
            
    render_filter_box("Mental Health Conditions", ", ".join(mh_conditions))
    render_filter_box("Therapy Type", ", ".join(therapy_type))
    render_filter_box("Traumas / Life Situations", ", ".join(trauma_support))
    render_filter_box("Provider Gender", provider_gender)
    render_filter_box("Insurance", ", ".join(insurance_options))
    render_filter_box("Hourly Rate", f"${hourly_rate[0]} - ${hourly_rate[1]}")

    # -------------------------------
    # Apply filters (example)
    # -------------------------------
    if search_clicked:
        st.success("Filters applied! Showing matching providers...")
        # Here you can integrate your provider search logic
        # e.g., update map points or a table based on selected filters

    # with col2: FOR GOOGLE MAPS
    #     st.subheader("Our Location")
    #     # Embed Google Map iframe
    #     st.markdown(
    #         """
    #         <iframe 
    #             src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2886.6719059078693!2d-79.3856906845003!3d43.65322697912162!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882b34d1f2fa3b91%3A0x2e60b13b1df6a055!2sToronto%2C%20ON%2C%20Canada!5e0!3m2!1sen!2sus!4v1695800000000!5m2!1sen!2sus" 
    #             width="100%" 
    #             height="400" 
    #             style="border:0;" 
    #             allowfullscreen="" 
    #             loading="lazy" 
    #             referrerpolicy="no-referrer-when-downgrade">
    #         </iframe>
    #         """,
    #         unsafe_allow_html=True
    #     )


    # Example unique content

