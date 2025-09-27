#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 12:51:10 2025

@author: angelinachen
"""
import streamlit as st

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #dbcaab !important;
        border-right: 3px solid #8b7355; /* darker accent for contrast */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("🧭 Navigation")

menu_items = [("Home", "home"), ("About Us", "about")]

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
    col1, col2, col3 = st.columns([4,4,4]) 
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

    col1, col2, col3 = st.columns([6,7,6])
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
            background-color:#ffffff;
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
    st.markdown("""
        <div style="
            background-color:#ffffff;
            border-radius:15px;
            padding:15px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
            margin-bottom:20px;
        ">
    """, unsafe_allow_html=True)

    search_query = st.text_input("🖊️ Tell me!", "")
    if search_query:
        st.write(f"You searched for: **{search_query}**")

    st.markdown("</div>", unsafe_allow_html=True)

    # Small top-left button in a rounded box
    st.markdown("""
        <div style="
            display:inline-block;
            background-color:#fae6c0;
            border-radius:12px;
            padding:10px 20px;
            margin-bottom:20px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        ">
    """, unsafe_allow_html=True)

    if st.button("Go back to Homepage"):
        st.query_params = {"page": ["home"]}

    st.markdown("</div>", unsafe_allow_html=True)

    # Columns for content and map
    col1, col2 = st.columns([2,3])

    with col1:
        st.markdown("""
            <div style="
                background-color:#ffffff;
                border-radius:15px;
                padding:15px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            ">
        """, unsafe_allow_html=True)

        st.subheader("The Database")
        st.write("We aim to build beautiful Streamlit apps that are easy to navigate.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="
                background-color:#ffffff;
                border-radius:15px;
                padding:15px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            ">
        """, unsafe_allow_html=True)

        st.subheader("🔎 Find a provider near you:")
        provider_search = st.text_input("🗺️ Input your city or postal code", "")
        
        # Map without pandas
        uw_map_data = [{"lat": 43.4723, "lon": -80.5449}]
        st.map(uw_map_data)

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer in rounded box
    st.markdown("""
        <div style="
            background-color:#ffffff;
            border-radius:15px;
            padding:15px;
            text-align:center;
            font-size:16px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
            margin-top:20px;
        ">
            Team - Angie and Iman
        </div>
    """, unsafe_allow_html=True)

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

