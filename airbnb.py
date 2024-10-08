import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
from concurrent.futures import ThreadPoolExecutor

items_per_page = 50
num_columns = 4
placeholder_image_path = "D:/CAPSTONE/AIRBNB/IMAGES/noimage.png"
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None
if 'show_more' not in st.session_state:
    st.session_state.show_more = False
@st.cache_data(show_spinner=False)
def is_valid_image_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
@st.cache_data(show_spinner=False)
def validate_image_urls(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(is_valid_image_url, urls))
    return results
@st.cache_data(show_spinner=False)
def load_data():
    data = pd.read_json(r"D:\CAPSTONE\AIRBNB\DATA\final_datas.json")
    address = pd.read_json(r"D:\CAPSTONE\AIRBNB\DATA\address.json")
    reviews = pd.read_json(r"D:\CAPSTONE\AIRBNB\DATA\reviews.json")
    host = pd.read_json(r"D:\CAPSTONE\AIRBNB\DATA\host.json")
    data.columns = data.columns.str.capitalize()
    address.columns = address.columns.str.capitalize()
    host.columns = host.columns.str.capitalize()
    reviews.columns = reviews.columns.str.capitalize()
    return data, address, reviews, host
data, address, reviews, host = load_data()
def display_image(image_url, placeholder_image_path):
    if validate_image_urls([image_url])[0]:
        st.markdown(
            f'<div style="height:250px; display: flex; align-items: center; justify-content: center;">'
            f'<img src="{image_url}" style="max-height: 100%; max-width: 100%; object-fit: cover;" />'
            f'</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="height: 200px; display: flex; align-items: center; justify-content: center;">'
            f'<img src="{placeholder_image_path}" style="max-height: 100%; max-width: 100%; object-fit: cover;" alt="No Image Available" />'
            f'</div>', unsafe_allow_html=True)
def display_location(address_row):
    location = address_row.get('Location', {})
    coordinates = location.get('coordinates', 'No coordinates available')
    if coordinates and coordinates != 'No coordinates available':
        lat, lon = coordinates
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        return f"📍 [Click Here For Location]({maps_link}) 📍"
    return "📍 Location coordinates not available 📍"
def display_items():
    items_per_column = 25  # Number of items per column
    total_items = len(data)  # Get total items from the dataset
    
    for i in range(0, total_items, items_per_column * 2):  
        coli, colj = st.columns(2)  # Create two columns for odd and even items
        
        # Display items in the first column (odd-indexed items)
        with coli:
            for idx in range(items_per_column):
                data_idx = i + 2 * idx  # Calculate the odd-indexed item
                if data_idx >= total_items:
                    break  # Exit if we exceed the available items
                row = data.iloc[data_idx]
                address_row = address.iloc[data_idx]
                host_row = filtered_host.iloc[0]  # Assumed to be single host
                col1, col2 = st.columns(2)
                
                # First column content
                with col1:
                    display_image(row['Images'], placeholder_image_path)
                    st.write(display_location(address_row))
                
                # Second column content
                with col2:
                    name = f"**{row['Name'].upper()}**"
                    country = f"**Country:** {address_row['Country']}" if not address_row.empty else "**Country:** Not available"
                    price = f"**Price :** {row['Price']}$"
                    review = f"**{row['Review_scores_value']}** ⭐ Review Score - **{row['Property_type'].upper()}**"
                    host_is_superhost = f"**SUPERHOST✅**\n" if host_row['Host_is_superhost'] else "**NO SUPERHOST❌**"
                    identity_verified = f"**Identity Verified** ✅\n" if host_row['Host_identity_verified'] else "**Identity Not Verified** ❌"
                    host_status_info = f"{host_is_superhost}{identity_verified}"
                    st.info(f"{name} \n\n {country} \n\n {price} \n\n {review} \n\n {host_status_info}")
                    st.button(f"Show More", key=f"show_more_{data_idx}")
                
                # Divider between items
                st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

                # Show more details if the button is clicked
                if st.session_state.get(f"show_more_{data_idx}"):
                    st.session_state.selected_row = row
                    st.session_state.show_more = True
                    detailed_view()
        
        # Display items in the second column (even-indexed items)
        with colj:
            for idx in range(items_per_column):
                data_idx = i + 2 * idx + 1  # Calculate the even-indexed item
                if data_idx >= total_items:
                    break  # Exit if we exceed the available items
                row = data.iloc[data_idx]
                address_row = address.iloc[data_idx]
                host_row = filtered_host.iloc[0]
                col1, col2 = st.columns(2)
                
                # First column content
                with col1:
                    display_image(row['Images'], placeholder_image_path)
                    st.write(display_location(address_row))
                
                # Second column content
                with col2:
                    name = f"**{row['Name'].upper()}**"
                    country = f"**Country:** {address_row['Country']}" if not address_row.empty else "**Country:** Not available"
                    price = f"**Price :** {row['Price']}$"
                    review = f"**{row['Review_scores_value']}** ⭐ Review Score - **{row['Property_type'].upper()}**"
                    host_is_superhost = f"**SUPERHOST✅**\n" if host_row['Host_is_superhost'] else "**NO SUPERHOST❌**"
                    identity_verified = f"**Identity Verified** ✅\n" if host_row['Host_identity_verified'] else "**Identity Not Verified** ❌"
                    host_status_info = f"{host_is_superhost}{identity_verified}"
                    st.info(f"{name} \n\n {country} \n\n {price} \n\n {review} \n\n {host_status_info}")
                    st.button(f"Show More", key=f"show_more_{data_idx}")
                
                # Divider between items
                st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

                # Show more details if the button is clicked
                if st.session_state.get(f"show_more_{data_idx}"):
                    st.session_state.selected_row = row
                    st.session_state.show_more = True
                    detailed_view()

def detailed_view():
    selected_row = st.session_state.selected_row
    st.title("Detailed View")
    colk, coll = st.columns(2)
    with colk:
        image_url = selected_row.get('Images', placeholder_image_path)
        if is_valid_image_url(image_url):
            st.image(image_url, use_column_width=True)
        else:
            st.image(placeholder_image_path, caption="No Image Available", use_column_width=True)
        st.caption(f"**ID :** {selected_row.get('_id')}")
    with coll:
        st.write(f"**Name :** {selected_row.get('Name')}")
        st.write(f"**Property Type :** {selected_row.get('Property_type')}")
        st.write(f"**Room Type :** {selected_row.get('Room_type')}")
        st.write(f"**Bedrooms :** {selected_row.get('Bedrooms')}")
        st.write(f"**Bathrooms :** {selected_row.get('Bathrooms')}")
        st.write('  |   '.join([f"**{label} :** {selected_row.get(key)}" for key, label in {'Beds': 'Beds','Bed_type': 'Bed Type'}.items() if selected_row.get(key) is not None]))
        st.write(f"**Accommodates :** {selected_row.get('Accommodates')}")
        st.success(f"**Price :** {selected_row.get('Price')}$")
    coli,colj = st.columns(2)
    with coli:
        with st.expander("Stay Limits"):
            stay_limits = {
                "Minimum Nights": [selected_row.get('Minimum_nights')],
                "Maximum Nights": [selected_row.get('Maximum_nights')]}
            df_stay_limits = pd.DataFrame(stay_limits)
            df_stay_limits_transposed = df_stay_limits.T
            df_stay_limits_transposed.columns = ["Availability"]
            html_table_1 = df_stay_limits_transposed.to_html(header=True, index=True)
            css_style_1 = """<style>th {background-color:#D0A2E0;}table {width: 100%;}th, td {padding: 10px; text-align: left;}</style>"""
            st.markdown(css_style_1 + html_table_1, unsafe_allow_html=True)
    with colj:
        with st.expander("Availability"):
            st.session_state.show_stay_limits = False
            st.session_state.show_availability = True
            st.session_state.show_review_scores = False
            availability_data = {"30 days": [selected_row.get('Availability_30')],
                                "60 days": [selected_row.get('Availability_60')],
                                "90 days": [selected_row.get('Availability_90')],
                                "365 days": [selected_row.get('Availability_365')]}
            df_availability = pd.DataFrame(availability_data)
            df_transposed = df_availability.T
            df_transposed.columns = ["Availability"]
            html_table_2 = df_transposed.to_html(header=True, index=True)
            css_style_2 = """<style>th {background-color:#D0A2E0;}table {width: 100%;}th, td {padding: 10px; text-align: left;}</style>"""
            st.markdown(css_style_2 + html_table_2, unsafe_allow_html=True)
    with st.expander("Review Scores"):
            st.session_state.show_stay_limits = True
            st.session_state.show_availability = False
            st.session_state.show_review_scores = False
            review_scores_data = {
                "Accuracy": [selected_row.get('Review_scores_accuracy')],
                "CheckIn": [selected_row.get('Review_scores_checkin')],
                "Cleanliness": [selected_row.get('Review_scores_cleanliness')],
                "Communication": [selected_row.get('Review_scores_communication')],
                "Location": [selected_row.get('Review_scores_location')],
                "Overall": [selected_row.get('Review_scores_value')]}
            review_scores_data_1 = {"RATING": [selected_row.get('Review_scores_rating')]}
            df_review_scores = pd.DataFrame(review_scores_data)
            df_review_scores_1 = pd.DataFrame(review_scores_data_1)
            df_review_scores_transposed = df_review_scores.T
            df_review_scores_1_transposed = df_review_scores_1.T
            df_review_scores_transposed.columns = ["Review Scores"]
            def convert_to_stars(rating):
                scaled_rating = rating / 2
                full_stars = int(scaled_rating)
                half_star = 1 if scaled_rating % 1 >= 0.5 else 0
                return '★' * full_stars + '☆' * half_star 
            df_review_scores_transposed["Review Scores"] = df_review_scores_transposed["Review Scores"].apply(convert_to_stars)
            html_table_3 = df_review_scores_transposed.to_html(header=True, index=True)
            html_table_4 = df_review_scores_1_transposed.to_html(header=False, index=True)
            css_style_3 = """<style>th {background-color:#D0A2E0;}table {width: 100%;}th, td {padding: 10px; text-align: left;}</style>"""
            st.markdown(css_style_3 + html_table_3, unsafe_allow_html=True)
            st.markdown(css_style_3 + html_table_4, unsafe_allow_html=True)
    fields = ['Description', 'Neighborhood_overview']
    for key in fields:
        value = selected_row.get(key, 'N/A')
        if value and value != 'N/A':
            st.markdown(f"<h2 style='text-align: center;'>{key.replace('_', ' ').title()}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{value}</p>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Amenities 🏠</h2>", unsafe_allow_html=True)
    amenities = selected_row.get('Amenities', [])
    if amenities:
        amenities_with_emojis = {
            "Wifi": "📶",
            "Air conditioning": "❄️",
            "Kitchen": "🍴",
            "Iron": "🧺",
            "Essentials": "🧳",
            "TV": "📺",
            "Elevator": "🛗",
            "Free street parking": "🅿️",
            "Heating": "🔥",
            "Washer": "🧼",
            "Dryer": "🌀",
            "Smoke detector": "🚨",
            "Fire extinguisher": "🧯",
            "Shampoo": "🧴",
            "Hangers": "🪝",
            "Hair dryer": "💇‍♀️",
            "Laptop friendly workspace": "💻",
            "Self check-in": "🔑",
            "Keypad": "🔢",
            "Private living room": "🛋️",
            "Hot water": "💧",
            "Bed linens": "🛏️",
            "Microwave": "🍲",
            "Coffee maker": "☕",
            "Refrigerator": "🧊",
            "Dishwasher": "🍽️",
            "Dishes and silverware": "🍴",
            "Cooking basics": "🍳",
            "Oven": "🔥",
            "Stove": "🍳",
            "Patio or balcony": "🏖️",
            "Long term stays allowed": "🏡",
            "Pool": "🏊‍♂️",
            "Free parking on premises": "🅿️",
            "Gym": "🏋️‍♂️",
            "Family/kid friendly": "👨‍👩‍👧‍👦",
            "First aid kit": "🩹",
            "Lock on bedroom door": "🔒",
            "24-hour check-in": "⏰",
            "Hot tub": "♨️",
            "Buzzer/wireless intercom": "🔔",
            "Internet": "🌐",
            "translation missing: en.hosting_amenity_50":"None",
            "translation missing: en.hosting_amenity_49":"None",
            }
        filtered_amenities = [item for item in amenities if item and item not in ["translation missing: en.hosting_amenity_50", "translation missing: en.hosting_amenity_49"]]
        col1, col2, col3, col4,col5 = st.columns(5)
        with col2:
            first_5_amenities = filtered_amenities[:5]
            amenities_text = "\n\n".join([f"{amenities_with_emojis.get(item, '')} {item}" for item in first_5_amenities if item])
            st.write(amenities_text)
        with col4:
            next_5_amenities = filtered_amenities[5:10]
            amenities_text = "\n\n".join([f"{amenities_with_emojis.get(item, '')} {item}" for item in next_5_amenities if item])
            st.write(amenities_text)
        col1, col2, col3= st.columns([1,4,1])
        with col2:
            if len(filtered_amenities) > 10:
                remaining_count = len(filtered_amenities) - 10
                additional_amenities = filtered_amenities[10:]
                with st.expander(f"Show {remaining_count} More Amenities"):
                    additional_amenities_text = "\n\n".join([f"{amenities_with_emojis.get(item, '')} {item}" for item in additional_amenities if item])
                    st.write(additional_amenities_text)
    fields1 = ['Space', 'Transit']
    for key in fields1:
        value = selected_row.get(key, 'N/A')
        if value and value != 'N/A':
            st.markdown(f"<h2 style='text-align: center;'>{key.replace('_', ' ').title()}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{value}</p>", unsafe_allow_html=True)
    fields1 = {'House_Rules': 'House Rules',
        'Extra_people': 'Extra People',
        'Security_deposit': 'Security Deposit',
        'Cleaning_fee': 'Cleaning Fee',
        'Guest_included': 'Guests Included',
        'Cnacellation_policy': 'Cancellation Policy'}
    col1, col2, col3 = st.columns(3)
    for key, label in fields1.items():
        value = selected_row.get(key, 'N/A')
        if value and value != 'N/A':
            with col2:
                st.info(f"**__{label}:__** {value}")
    
    st.markdown(f"<h2 style='text-align: center;'>What Guests Are Saying 💬 \n\n {selected_row.get('Number_of_reviews')} Reviews</h2>" , unsafe_allow_html=True)
    global reviews  
    filtered_reviews = reviews[reviews['Listing_id'] == selected_row.get('_id')]
    if not filtered_reviews.empty:
        num_reviews = len(filtered_reviews)
        if num_reviews <= 5:
            for _, review in filtered_reviews.iterrows():
                st.markdown(f"**{review['Reviewer_name']}**  |  **{review['Date']}**")
                st.caption(f"Review ID: {review['Reviewer_id']}")
                st.markdown(review['Comments'])
                st.write("---")
        else:
            for _, review in filtered_reviews.head(5).iterrows():
                st.markdown(f"**{review['Reviewer_name']}**  |  **{review['Date']}**")
                st.caption(f"Review ID: {review['Reviewer_id']}")
                st.markdown(review['Comments'])
                st.write("---")
            with st.expander(f"Show {num_reviews - 5} More Reviews"):
                for _, review in filtered_reviews.iloc[5:].iterrows():
                    st.markdown(f"**{review['Reviewer_name']}**  |  **{review['Date']}**")
                    st.caption(f"Review ID: {review['Reviewer_id']}")
                    st.markdown(review['Comments'])
                    st.write("---")
    else:
        st.markdown(f"<h6 style='text-align: center;'>No reviews available.</h6>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'> Destination Address 📍 </h2>", unsafe_allow_html=True)
    coli,colj,colk = st.columns([1,3,1])
    with colj:
        global address  
        filtered_address = address[address["_id"] == selected_row.get("_id")]
        for _, row in filtered_address.iterrows():
            street = row.get('Street', 'N/A')
            suburb = row.get('Suburb', 'N/A')
            government_area = row.get('Government_area', 'N/A')
            market = row.get('Market', 'N/A')
            country = row.get('Country', 'N/A')
        st.info(f"**Street :** {street} \n\n**Government Area :** {government_area} \n\n**Market :** {market} \n\n**Suburb :** {suburb} \n\n**Country :** {country}")
    st.markdown(f"<h2 style='text-align: center;'> Meet Your Host 🤝 </h2>", unsafe_allow_html=True)
    global host 
    filtered_host = host[host['Host_id'].isin(data['Host'])]
    col1, col2, col3 = st.columns([2,2,2])
    with col1:
        if not filtered_host.empty:
            host = filtered_host.iloc[0]
            image_url = selected_row.get('Host_picture_url', placeholder_image_path)
            if is_valid_image_url(image_url):
                st.image(image_url, use_column_width=True)
            else:
                st.image(placeholder_image_path, caption="No Image Available", use_column_width=True)
            st.caption(f"**ID:** {host['Host_id']}")
    with col2:
        st.error(f"**{host['Host_name'].upper()}   ({host['Host_listings_count']} Listings)**")
        st.error(f" \n\n **{host['Host_location']}**")
        if host['Host_is_superhost']:
            st.error(f"**SUPERHOST**")
        else:
            st.error(f"**NO SUPERHOST**")
    with col3:
        st.warning(f"**Response Time:** **{host['Host_response_time']}**")
        st.warning(f"**{host['Host_response_rate']}%** **Response Rate**")
        if host['Host_identity_verified']:
            st.warning(f"**Identity Verified :** ✅")
        else:
            st.warning(f"Identity Verified : ❌")
    st.success(f"Verified--- \t\t" + "\t\t".join([f"✔️ {item.capitalize().replace('_', ' ')}" for item in host["Host_verifications"]]))
    if host['Host_about'] != 'No Information Provided':
        st.info(f"**About:** {host['Host_about']}")
    if st.button("Close", key="close_unique"):
        st.session_state.show_more = False
        st.experimental_rerun()
    st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)
st.set_page_config(page_icon="D:/CAPSTONE/AIRBNB/IMAGES/logo.png", page_title="Airbnb Data Analysis", layout="wide")
st.title("AIRBNB LISTINGS")
st.markdown("""
    Airbnb analysis involves examining various aspects of rental listings to derive insights about property characteristics, 
    pricing strategies, and guest preferences. This analysis typically includes evaluating data on amenities, property types,
    location, availability, and review scores to understand trends and optimize rental performance.
""")
filtered_data = data.copy()
filtered_add = address.copy()
filtered_host = host.copy()
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    selected = option_menu(menu_title=None, options=["HOME", "ANALYSIS"], icons=["house", "search"], orientation="horizontal")
if selected == "HOME":
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        countries = address["Country"].unique()
        selected_filter_1 = st.selectbox("COUNTRY", options=["All"] + list(countries))
    with col2:
        property_types = data["Property_type"].unique()
        selected_filter_2 = st.selectbox("PROPERTY TYPE", options=["All"] + list(property_types))
    with col3:
        price_ranges = {
            "All": (100, 50000),
            "Under $500": (0, 500),
            "$500 - $1000": (500, 1000),
            "$1000 - $5000": (1000, 5000),
            "Above $5000": (5000, 50000)}
        selected_filter_3 = st.selectbox("PRICE RANGE", options=list(price_ranges.keys()))
    with col4:
        selected_review_range = st.slider("Select Review Range",min_value=0,max_value=10,value=(0, 10),step=1)

    if selected_filter_1 != "All":
        filtered_add = filtered_add[filtered_add["Country"] == selected_filter_1]
        filtered_data = filtered_data[filtered_data.index.isin(filtered_add.index)]
    if selected_filter_2 != "All":
        filtered_data = filtered_data[filtered_data["Property_type"] == selected_filter_2]
    min_price_range, max_price_range = price_ranges[selected_filter_3]
    if selected_filter_3 != "All":
        filtered_data = filtered_data[(filtered_data["Price"] >= min_price_range) & (filtered_data["Price"] <= max_price_range)]
    min_review_score, max_review_score = selected_review_range
    filtered_data = filtered_data[(filtered_data["Review_scores_value"] >= min_review_score) & (filtered_data["Review_scores_value"] <= max_review_score)]
    start_index = st.session_state.current_page * items_per_page
    end_index = min(start_index + items_per_page, len(data))
    display_items()
    # col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    # with col1:
    #     if st.button("<< Previous", disabled=st.session_state.current_page == 0):
    #         st.session_state.current_page -= 1
    #         st.experimental_rerun()
    # with col4:
    #     if st.button("Next >>", disabled=end_index >= len(data)):
    #         st.session_state.current_page += 1
    #         st.experimental_rerun()
                