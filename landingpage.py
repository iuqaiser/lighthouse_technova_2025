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
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        st.title("⚓️💡🌊🚢") 
    col1, col2, col3, col4, col5 = st.columns([1,1,2,1,1])
    with col3:
        st.title("Lighthouse")
    col1, col2, col3 = st.columns([6,7,6])
    with col2:
        st.write("Where hope is only one click away.")

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
    st.title("📄 About Us Page")
    st.write("Welcome to the About Us page!")

    # Small top-left button
    if st.button("Go Back Home"):
        st.query_params = {"page": ["home"]}
        
        

    st.markdown("</div>", unsafe_allow_html=True)

    # Example unique content
    st.subheader("Our Mission")
    st.write("We aim to build beautiful Streamlit apps that are easy to navigate.")
    
    st.subheader("Team")
    st.write("- Alice: Frontend Developer\n- Bob: Backend Developer\n- Charlie: UX Designer")
