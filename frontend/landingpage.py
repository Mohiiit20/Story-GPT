import streamlit as st

def showLandingPage():
    # Set up the Streamlit page configuration
    st.set_page_config(page_title="StoryGPT", page_icon="📚")

    # PAGE SETUP
    customized_story_gen_page = st.Page(
        "frontend/custom.py",
        title="custom",
        icon=":material/home:",
    )
    home_page = st.Page(
        "frontend/homepage.py",
        title="Home",
        icon=":material/home:",
        default=True,
    )
    about_page = st.Page(
        "frontend/aboutpage.py",
        title="About",
        icon=":material/info:",
    )
    contact_page = st.Page(
        "frontend/contactpage.py",
        title="Contact",
        icon=":material/contact_page:",
    )
    profile_page = st.Page(
        "frontend/profilepage.py",
        title="Profile",
        icon=":material/account_circle:",
    )

    # NAVIGATION SETUP [WITHOUT SECTIONS]
    pg = st.navigation(pages=[customized_story_gen_page,home_page, profile_page, about_page, contact_page])

    # NAVIGATION SETUP [WITH SECTIONS]
    # pg = st.navigation(
    #     {
    #         "Info": [about_page],
    #         "Projects": [project_1_page, project_2_page],
    #     }
    # )

    st.sidebar.markdown("Create Stories. Inspire Imagination!")

    # RUN NAVIGATION
    pg.run()
