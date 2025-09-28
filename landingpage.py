#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 12:51:10 2025

@author: angelinachen
"""
import streamlit as st
import pandas as pd 
import requests
from geopy.geocoders import Nominatim 


backend_url = "http://127.0.0.1:8000"  

if "filtered_providers" not in st.session_state:
    st.session_state["filtered_providers"] = []

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
    col1, col2, col3 = st.columns([1.5,1,1.5])
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
    # search_query = st.text_input("🖊️ Type into the search bar and I’ll help match you with a mental health provider, or use the navigation filters to explore options that fit your needs.", "")
    # if search_query:
    #     st.write(f"You searched for: **{search_query}**")
        #pass to backend

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
    if "filtered_providers" in st.session_state:
        table_placeholder.dataframe(
            pd.DataFrame(st.session_state["filtered_providers"]), 
            use_container_width=True
        )
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
        <div style='margin-top:30px;'></div>
    """, unsafe_allow_html=True)

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
    search_query2 = []
    #st.text_input("Search by location", key="search_query")
    # if search_query2: 
    # # TODO: Replace with Snowflake query
    #     df = pd.DataFrame({
    #     "Provider": ["Alice", "Bob"],
    #     "Specialty": ["CBT", "DBT"],
    #     "Location": ["Toronto", "Vancouver"]
    # })
    #     st.session_state["results"] = df

# # --- Results section (scoped only to this area) ---
#     table_placeholder = st.empty()
#     with table_placeholder.container():
#         if "results" in st.session_state:
#             st.dataframe(st.session_state["results"], use_container_width=True)
#         else:
#             st.markdown("""
#                         <div style="
#                         background-color:#fff8ef;
#                 border: 2px dashed #c78b72;
#                 border-radius:12px;
#                 padding:20px;
#                 text-align:center;
#                 color:#555;
#                 font-size:18px;
#                 margin-top:15px;
#             ">
#             ℹ️ Use the search bar or filters to see results.
            
#             </div>
#             <div style='margin-top:30px;'></div>
#         """, unsafe_allow_html=True)
        
        # Map without pandas
    # Map points for filtered providers
    try:
        response = requests.get(f"{backend_url}/search/providers", params={"limit": 100})
        response.raise_for_status()
        providers = response.json()  # List of dicts with provider info
    except Exception as e:
        st.error(f"Could not fetch providers: {e}")
        providers = []

    # Geocode addresses
    geolocator = Nominatim(user_agent="lighthouse_app")
    map_points = []

    for provider in providers:
        address = provider.get("address")
        if address:
            try:
                location = geolocator.geocode(address)
                if location:
                    map_points.append({"lat": location.latitude, "lon": location.longitude})
            except Exception as e:
                st.warning(f"Could not geocode address '{address}': {e}")

    # If no valid points, fallback
    if not map_points:
        map_points = [{"lat": 43.4723, "lon": -80.5449}]

    # Show map
    st.map(map_points)

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer in rounded box
    col1, col2, col3 = st.columns([2,1,2])
    with col2: 
        st.write("Team - Angie and Iman")

# -------------------------------
# Sidebar Filters (only for About Us page)
# -------------------------------

# Backend URL
# Replace with deployed backend

# Define allowed columns as in your backend
allowed_columns = {
    "provider_role": "Provider Occupation",
    "gender_identity": "Provider Gender",
    "insurance": "Insurance Accepted",
    "session_options": "Session Options",
    "specialized_support": "Specialized Support",
    "services_offered": "Services Offered"
}
# Dictionary to store fetched values
column_values = {}
# Fetch values from backend
for col_key, col_label in allowed_columns.items():
    try:
        response = requests.get(f"{backend_url}/unique_split/{col_key}")
        column_values[col_key] = response.json()  # list of strings
    except Exception as e:
        st.error(f"Could not load {col_label}: {e}")
        column_values[col_key] = []

if page == "about":
    st.sidebar.markdown("---")  # Separator line
    st.sidebar.subheader("Filter Providers 🩺")

    occupation = st.sidebar.multiselect(
    allowed_columns["provider_role"],
    options=column_values["provider_role"]
    )

    gender = st.sidebar.multiselect(
        allowed_columns["gender_identity"],
        options=column_values["gender_identity"]
    )

    insurance = st.sidebar.multiselect(
        allowed_columns["insurance"],
        options=column_values["insurance"]
    )

    session_options = st.sidebar.multiselect(
        allowed_columns["session_options"],
        options=column_values["session_options"]
    )

    specialized_support = st.sidebar.multiselect(
        allowed_columns["specialized_support"],
        options=column_values["specialized_support"]
    )

    services_offered = st.sidebar.multiselect(
        allowed_columns["services_offered"],
        options=column_values["services_offered"]
    )
    
    # specialty = st.sidebar.text_input("Specialty")
    # insurance = st.sidebar.text_input("Insurance")
    # gender = st.sidebar.text_input("Gender Identity")
    # services = st.sidebar.text_input("Services Offered")
    # session = st.sidebar.text_input("Session Offering Options")
    #rate = st.sidebar.slider("Hourly Rate", 0, 500, 10)
    city_input = st.sidebar.text_input("City")  # Allow free-text input
    limit = st.sidebar.slider("Max providers to fetch", 1, 100, 50)
    # 1️⃣ Specialization in specific mental health conditions
    # mh_conditions = st.sidebar.multiselect(
    #     "Common specialization in mental health conditions",
    #     options=[
    #         "Depression", "Anxiety", "PTSD", "Bipolar", "ADHD", "Eating Disorders", "OCD", "Other"
    #     ]
    # )

    # # 2️⃣ Type of therapy
    # therapy_type = st.sidebar.multiselect(
    #     "Type of therapy",
    #     options=[
    #         "CBT", "DBT", "Group therapy (including AA)", "One-on-one", "Other"
    #     ]
    # )

    # # 3️⃣ Specialization in traumas / life situations
    # trauma_support = st.sidebar.multiselect(
    #     "Common specialization in trauma / life situations",
    #     options=[
    #         "LGBTQ+ support", "Religious support", "Domestic/sexual violence trauma",
    #         "Addiction support", "Grief counseling", "Career / life coaching", "Other"
    #     ]
    # )

    # # 4️⃣ Provider gender
    # provider_gender = st.sidebar.radio(
    #     "Healthcare provider gender",
    #     options=["Any", "Male", "Female", "Non-binary", "Other"]
    # )

    # # 5️⃣ Insurance and hourly rate
    # insurance_options = st.sidebar.multiselect(
    #     "Common insurance accepted",
    #     options=["OHIP", "Greenshield", "Manulife", "Blue Cross", "Canada Life", "Sun Life", "Desjardins", "Other"]
    # )
    rate = st.sidebar.slider(
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
                    color:#32a852;
                ">
                    <strong>{label}:</strong> {value}
                </div>
            """, unsafe_allow_html=True) 
            
    render_filter_box("Occupation", ", ".join(occupation or []))
    render_filter_box("Therapy Type", ", ".join(services_offered or []))
    render_filter_box("Traumas / Life Situations", ", ".join(specialized_support or []))
    render_filter_box("Provider Gender", gender)
    render_filter_box("Insurance", ", ".join(insurance or []))
    render_filter_box("Hourly Rate", f"${rate[0]} - ${rate[1]}")

    params = {
        "provider_role": occupation if occupation else None,
        "services_offered": services_offered if services_offered else None,
        "specialized_support": specialized_support if specialized_support else None,
        "gender_identity": gender if gender else None,
        "insurance": insurance if insurance else None,
        "hourly_rate_min": rate[0] if rate else None,
        "hourly_rate_max": rate[1] if rate else None,
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    # --- Fetch providers ---
    providers = []
    if search_clicked:
        st.session_state["filtered_providers"] = []
        st.success("Filters applied! Fetching matching providers...")
        try:
            # Fetch providers from backend
            params_query = {k: ','.join(v) if isinstance(v, list) else v for k, v in params.items()}
            response = requests.get(f"{backend_url}/search/providers", params=params_query)
            response.raise_for_status()
            providers = response.json()
        except Exception as e:
            st.error(f"Could not fetch providers: {e}")
            providers = []

        #Filter providers further based on search term
        search_term_lower = search_query2.lower() if search_query2 else None
        for p in providers:
            if search_term_lower:
                found = False
                for key, value in p.items():
                    if isinstance(value, list):
                        if any(search_term_lower in str(v).lower() for v in value):
                            found = True
                            break
                    elif value is not None:
                        if search_term_lower in str(value).lower():
                            found = True
                            break
                if not found:
                    continue
            st.session_state["filtered_providers"].append(p)

    # Display results
    # table_placeholder = st.empty()
    # if st.session_state["filtered_providers"]:
    #     table_placeholder.dataframe(
    #         pd.DataFrame(st.session_state["filtered_providers"]),
    #         use_container_width=True
    #     )
    # else:
    #     table_placeholder.markdown("ℹ️ Use the search bar or filters to see results.")

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

