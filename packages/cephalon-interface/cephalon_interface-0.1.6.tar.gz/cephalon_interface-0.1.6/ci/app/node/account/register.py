import time
import pycountry
import streamlit as st
from ci.core import cephalon

country_names = [country.name for country in pycountry.countries]
country_name_to_code: dict = {
    country.name: country.alpha_2 for country in pycountry.countries
}


def render_already_logged_in():
    st.error(
        "You are already logged in to an account. Please log out first to submit a new registration request."
    )


def render_registration_form():
    first_name = st.text_input("First Name", placeholder="John")
    last_name = st.text_input("Last Name", placeholder="Doe")
    email = st.text_input("Email", placeholder="example@domain.com")
    # citcol, affcol = st.columns([1, 1])
    # with citcol:
    #     country_name = st.selectbox(
    #         "Citizenship",
    #         options=country_names,
    #         index=None,
    #         help="Your primary citizenship.",
    #     )
    #     if country_name:
    #         citizenship = country_name_to_code[country_name]

    # with affcol:
    #     entity_affiliation = st.selectbox(
    #         "Entity Affiliation",
    #         options=[
    #             "Individual",
    #             "Organization",
    #             "Academic",
    #             "Government",
    #             "Company",
    #             "Other",
    #         ],
    #         index=None,
    #         help="Whether this application is for an individual or an organization.",
    #     )
    # organization = st.text_input("Organization")
    # organization_type = st.selectbox(
    #     "Organization Type",
    #     options=["Academic", "Government", "Private", "Other"],
    #     index=None,
    # )
    # organization_country = st.selectbox(
    #     "Organization Country", options=["US", "Non-US"], index=None
    # )
    # position = st.text_input("Your Position at Organization")
    # referral_info = st.text_area("How did you hear about us?")
    # interest_info = st.text_area(
    #     "What research tools, resources, or data are you interested in?"
    # )
    # # todo: add - would you be willing to pay for any of the services?
    # # default: I need to test the services first
    # # - if so, which ones?
    # # - if so, how much?
    # # - what is your preferred payment method?
    if st.button("Submit"):
        # todo: add params
        result = cephalon.account.register(
            email=email, first_name=first_name, last_name=last_name
        )
        if result.is_ok():
            st.success("Your registration request has been submitted.")
            st.info("Please check your email for a temporary password.")

        else:
            st.error(result.message)


def render():
    st.markdown("# Register for an account.")
    if cephalon.account.authenticated:
        render_already_logged_in()
    else:
        render_registration_form()
