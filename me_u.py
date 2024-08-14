import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


# URL Setup
st.set_page_config(
    page_title="Braza Churrascaria - me&u",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and display image
image = Image.open(logob.png')
resized_image = image.resize((520, 180))  # Resize to 250x250 pixels
st.image(resized_image)

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")


# File upload button
st.header("Upload your file")
uploaded_file = st.file_uploader('', type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:

    # Read the uploaded Excel file into a DataFrame
    df_1 = pd.read_csv(uploaded_file)
    df = df_1.loc[:, ['orderId', 'localCreatedAt', 'productName', 'menuCategoryName',
                      'menuSectionName', 'type', 'category', 'quantity', 'totalPrice', 'kind', 'status']]

    # Convert the 'localCreatedAt' column to datetime
    df['localCreatedAt'] = pd.to_datetime(df['localCreatedAt'])

    # Extract just the date
    df['date'] = df['localCreatedAt'].dt.date
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')
    st.write(f"File Date: {df['date'].iloc[0]}")
    df['quantity'] = df['quantity'].astype(float)

    import pandas as pd
    import numpy as np

    # lists for modifiers (updated: 7/aug/2024)
    mod_hot_choc = ['Soy milk', 'Almond milk']
    mod_coffee = ['Double shot', 'Decaf', 'Soy milk', 'Almond milk']
    mod_caipirinha = ['Lime', 'Strawberry',
                      'Kiwi', 'Passion Fruit', 'Pomegranate']
    mod_f_batida = ['Coconut', 'Pineapple', 'Strawberry', 'Passion fruit']
    mod_gin_martini = ['Bombay Sapphire',
                       'Roku Gin', "Hendrick's", 'Hendrick’s']
    mod_batida = ['Cachaça', 'Vodka', 'White Rum']
    mod_icec = ['Vanilla', 'Rock salt caramel', 'Green apple', 'Lemon lime']
    mod_lunchbox = ['Coke', 'Coke No Sugar', 'Sprite', 'Guaraná Antarctica Can', 'Fanta', 'Lift', 'Orange juice', 'Pineapple juice',
                    'Apple juice', 'Guava juice', 'House Beer', 'House White Wine - Sauvignon Blanc', 'House Red Wine - Shiraz']
    mod_hotplate = ['Rare', 'Medium Rare',
                    'Medium', 'Medium Well', 'Well Done']
    mod_spirits = ['w/ Coke', 'w/ Coke No Sugar', 'w/ Sprite', 'w/ Tonic', 'w/ Soda Water', 'w/ Dry Ginger Ale', 'w/ Fanta',
                   'w/ Lift', 'w/ Cramberry juice', 'w/ Pineapple juice', 'w/ Apple juice', 'w/ Orange juice', 'Just ICE', 'NO ICE - Straight']
    mod_lunchbox_gsalad = ['Rump Cap', 'Chicken Thigh', 'Halloumi cheese']
    mod_lunchbox_pulled = ['Pulled Beef', 'Pulled Pork']

    # Creating a flag in the DF
    def set_mod_flag(row):
        if row['type'] == 'menu_item' or row['type'] == 'upsell_item':
            if row['menuSectionName'] == 'Coffee':
                if row['productName'] == 'Hot Chocolate':
                    return 1
            elif row['menuSectionName'] == 'Coffee':
                return 2
            elif row['menuSectionName'] == 'Martinis':
                return 5
            elif row['menuCategoryName'] == 'Cocktails' or row['menuSectionName'] == 'Caipirinha Family':
                return 3
            elif row['menuSectionName'] == 'Batidas':
                return 4
            elif row['menuSectionName'] == 'Desserts':
                if row['productName'] == 'Ice Cream and Sorbet - 3 Scoops' or row['productName'] == 'Ice Cream and Sorbet - 2 Scoops' or row['productName'] == 'Ice Cream and Sorbet':
                    return 6
            elif row['menuSectionName'] == 'Lunch Boxes':
                return 7
            elif row['menuSectionName'] == 'Hot Iron Plate - All served with Beer Battered Chips ':
                return 8
            elif row['menuCategoryName'] == 'Spirits':
                return 9
            else:
                return 0  # Default value for unmatched conditions
        return None

    # AFFIRMATION STATEMENT
    # Apply the function to each row
    df['mod_flag'] = df.apply(set_mod_flag, axis=1)

    df_no_modifier = df[(df['mod_flag'] == 0) & (df['kind'] == 'affirmation')]

    # Creating a database with items that need modifier and modifiers
    df_filter_mod = df[(df['mod_flag'] != 0) & (df['kind'] == 'affirmation')]

    # Flagging the the respective modifiers ad their prices
    mod_flag_map = {
        1: mod_hot_choc,
        2: mod_coffee,
        3: mod_caipirinha,
        4: mod_f_batida,
        5: mod_gin_martini,
        6: mod_icec,
        7: mod_lunchbox,
        8: mod_hotplate,
        9: mod_spirits
    }

    def find_modifiers(row, df_filter_mod, used_modifiers):
        if row['mod_flag'] > 0:
            order_id = row['orderId']
            # Check specific productName for additional lists
            if row['productName'] == 'Garden Salad Box':
                primary_mod_list = mod_lunchbox_gsalad
                secondary_mod_list = mod_lunchbox
            elif row['productName'] == 'Pulled Burger':
                primary_mod_list = mod_lunchbox_pulled
                secondary_mod_list = mod_lunchbox
            elif row['menuSectionName'] == 'Batidas':
                primary_mod_list = mod_batida
                secondary_mod_list = mod_f_batida
            else:
                primary_mod_list = mod_flag_map.get(row['mod_flag'], [])
                secondary_mod_list = []

            # Get all modifiers for the given orderID
            modifiers = df_filter_mod[(df_filter_mod['orderId'] == order_id) & (
                df_filter_mod['type'] == 'modifier')]

            primary_mod = ""
            secondary_mod = ""
            primary_mod_price = ""
            secondary_mod_price = ""

            # Check each modifier against the primary list first
            for _, mod_row in modifiers.iterrows():
                if mod_row['productName'] in primary_mod_list and mod_row['productName'] not in used_modifiers:
                    primary_mod = mod_row['productName']
                    primary_mod_price = mod_row['totalPrice']
                    used_modifiers.add(primary_mod)
                    break

            # If there is a secondary list, check against it
            for _, mod_row in modifiers.iterrows():
                if mod_row['productName'] in secondary_mod_list and mod_row['productName'] not in used_modifiers:
                    secondary_mod = mod_row['productName']
                    secondary_mod_price = mod_row['totalPrice']
                    used_modifiers.add(secondary_mod)
                    break

            return primary_mod, secondary_mod, primary_mod_price, secondary_mod_price

        return "", "", "", ""

    # Apply the function to each row and create the 'modifier_1', 'modifier_2', 'modifier_1_price', and 'modifier_2_price' columns

    used_modifiers_by_order = {order_id: set()
                               for order_id in df_filter_mod['orderId'].unique()}
    df_filter_mod[['modifier_1', 'modifier_2', 'modifier_1_price', 'modifier_2_price']] = df_filter_mod.apply(
        lambda row: pd.Series(find_modifiers(row, df_filter_mod, used_modifiers_by_order[row['orderId']])), axis=1
    )

    # Create the 'new_name' column
    df_filter_mod['new_name'] = df_filter_mod.apply(
        lambda row: f"{row['productName']} {row['modifier_1']} {row['modifier_2']}".strip(), axis=1
    )

    # Ensuring that 'modifier_1_price' and 'modifier_2_price' are converted to numeric values
    df_filter_mod['modifier_1_price'] = pd.to_numeric(
        df_filter_mod['modifier_1_price'], errors='coerce').fillna(0)
    df_filter_mod['modifier_2_price'] = pd.to_numeric(
        df_filter_mod['modifier_2_price'], errors='coerce').fillna(0)

    # Create the new column with the calculation
    df_filter_mod['total_with_modifiers'] = df_filter_mod['totalPrice'] + (
        df_filter_mod['quantity'] *
        (df_filter_mod['modifier_1_price'] + df_filter_mod['modifier_2_price'])
    )

    # Final base modifiers
    df_filter_mod_vf = df_filter_mod[['orderId', 'new_name', 'menuCategoryName',
                                      'menuSectionName', 'type', 'total_with_modifiers', 'quantity', 'kind', 'status']]
    df_mod_f = df_filter_mod_vf.rename(
        columns={'new_name': 'productName', 'total_with_modifiers': 'totalPrice'})
    df_mod_f = df_mod_f[df_mod_f['type'] == 'menu_item']

    # Concat tables
    df_full = df_no_modifier[['orderId', 'productName', 'menuCategoryName',
                              'menuSectionName', 'type', 'totalPrice', 'quantity', 'kind', 'status']]
    df_combined = pd.concat([df_mod_f, df_full], ignore_index=True)

    valid = df_combined[df_combined['kind'] == 'affirmation']

    # Reporting valid
    result = valid.groupby(['productName', 'menuCategoryName', 'menuSectionName']).agg(
        count=('quantity', 'sum'),
        total_price=('totalPrice', 'sum')
    ).reset_index()

    result = result.rename(columns={
        'productName': 'Product Name',
        'menuCategoryName': 'Category',
        'menuSectionName': 'Section',
        'count': 'Quantity',
        'total_price': 'Total Price'})

    result_final_valid = result[['Category', 'Section',
                                 'Product Name', 'Quantity', 'Total Price']]

    df_sorted = result_final_valid.sort_values(
        by=['Category', 'Section', 'Product Name'], ascending=[True, True, True])

    df_sum = df_sorted['Total Price'].sum()

    def highlight_rows(row):
        if row['Quantity'] > 5:
            return ['background-color: red; color: black;' for _ in row]
        elif row['Quantity'] > 4:
            return ['background-color: orange; color: black;' for _ in row]
        elif row['Quantity'] > 3:
            return ['background-color: pink; color: black;' for _ in row]
        elif row['Quantity'] > 2:
            return ['background-color: lightgreen; color: black;' for _ in row]
        elif row['Quantity'] > 1:
            return ['background-color: yellow; color: black;' for _ in row]
        else:
            return ['' for _ in row]

    # Apply the style
    df_sorted = df_sorted.reset_index(drop=True)
    df_sorted = df_sorted.sort_values(
        by=['Category', 'Section', 'Product Name'], ascending=[True, True, True])
    df_st_sum = df_sorted['Total Price'].sum()
    df_st = df_sorted

    # st.dataframe(df_st, use_container_width=True, height=850)

# REVERSAL STATEMENT
    df_no_modifier_reversal = df[(
        df['mod_flag'] == 0) & (df['kind'] == 'reversal')]

    # Creating a database with items that need modifier and modifiers
    df_filter_mod_reversal = df[(df['mod_flag'] != 0)
                                & (df['kind'] == 'reversal')]

    q_df1 = df_no_modifier_reversal['quantity'].sum()
    q_df2 = df_filter_mod_reversal['quantity'].sum()

    # if q_df1 > 0:
    #   st.write('q_df1_OK')

   # if q_df2 > 0:
    #    st.write('q_df2_OK')
   # else:
    #    st.write(q_df2)

    if not q_df1 == 0 and q_df2 == 0:
        result_reversal = df_no_modifier_reversal.groupby(['productName', 'menuCategoryName', 'menuSectionName']).agg(
            count=('quantity', 'sum'),
            total_price=('totalPrice', 'sum')
        ).reset_index()

        result_reversal = result_reversal.rename(columns={
            'productName': 'Product Name',
            'menuCategoryName': 'Category',
            'menuSectionName': 'Section',
            'count': 'Quantity',
            'total_price': 'Total Price'})

        result_final_valid_reversal = result_reversal[['Category', 'Section',
                                                       'Product Name', 'Quantity', 'Total Price']]

        df_sorted_reversal = result_final_valid_reversal.sort_values(
            by=['Category', 'Section', 'Product Name'], ascending=[True, True, True])

        df_sum_reversal = df_sorted_reversal['Total Price'].sum()
        df_sorted_reversal['Quantity'] = df_sorted_reversal['Quantity'] * -1
        df_af_sum = df['totalPrice'].sum()

        df_final = pd.concat([df_sorted, df_sorted_reversal])
        df_final = df_final.groupby(['Category', 'Section', 'Product Name'], as_index=False).agg({
            'Quantity': 'sum', 'Total Price': 'sum'})
        df_final = df_final[df_final['Quantity'] > 0]
        df_final_sum = df_final['Total Price'].sum()

        def highlight_rows(row):
            if row['Quantity'] > 5:
                return ['background-color: red; color: black;' for _ in row]
            elif row['Quantity'] > 4:
                return ['background-color: orange; color: black;' for _ in row]
            elif row['Quantity'] > 3:
                return ['background-color: pink; color: black;' for _ in row]
            elif row['Quantity'] > 2:
                return ['background-color: lightgreen; color: black;' for _ in row]
            elif row['Quantity'] > 1:
                return ['background-color: yellow; color: black;' for _ in row]
            else:
                return ['' for _ in row]

        # Apply the style
        df_final = df_final.reset_index(drop=True)
        df_final = df_final.sort_values(
            by=['Category', 'Section', 'Product Name'], ascending=[True, True, True])
        df_final['Total Price'] = df_final['Total Price'].apply(
            lambda x: f"${x:,.2f}")
        df_final['Quantity'] = df_final['Quantity'].astype(int)
        df_final = df_final.style.apply(highlight_rows, axis=1)

        st.dataframe(df_final, use_container_width=True, height=850)
        st.write(f"Total refunded: $ {df_sum_reversal:.2f}")
        st.write(f"Total sales: $ {df_af_sum:.2f}")
        st.write(f"Total sales - refund: $ {df_final_sum:.2f}")

        if df_final_sum == df_af_sum:
            st.markdown(
                '<p style="color:green;">Validation: CORRECT - OK</p>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<p style="color:red;">Validation: INCORRECT - NOK</p>', unsafe_allow_html=True)

    elif (q_df1 > 0 and q_df2 > 0) or (q_df1 == 0 and q_df2 > 0):
        # Flagging the the respective modifiers ad their prices
        mod_flag_map = {
            1: mod_hot_choc,
            2: mod_coffee,
            3: mod_caipirinha,
            4: mod_f_batida,
            5: mod_gin_martini,
            6: mod_icec,
            7: mod_lunchbox,
            8: mod_hotplate,
            9: mod_spirits
        }

        def find_modifiers_reversal(row, df_filter_mod_reversal, used_modifiers_reversal):
            if row['mod_flag'] > 0:
                order_id = row['orderId']

                # Check specific productName for additional lists
                if row['productName'] == 'Garden Salad Box':
                    primary_mod_list_reversal = mod_lunchbox_gsalad
                    secondary_mod_list_reversal = mod_lunchbox
                elif row['productName'] == 'Pulled Burger':
                    primary_mod_list_reversal = mod_lunchbox_pulled
                    secondary_mod_list_reversal = mod_lunchbox
                elif row['menuSectionName'] == 'Batidas':
                    primary_mod_list_reversal = mod_batida
                    secondary_mod_list_reversal = mod_f_batida
                else:
                    primary_mod_list_reversal = mod_flag_map.get(
                        row['mod_flag'], [])
                    secondary_mod_list_reversal = []

                # Get all modifiers for the given orderID
                modifiers_reversal = df_filter_mod_reversal[
                    (df_filter_mod_reversal['orderId'] == order_id) &
                    (df_filter_mod_reversal['type'] == 'modifier')
                ]

                primary_mod_reversal = None
                secondary_mod_reversal = None
                primary_mod_price_reversal = 0.0
                secondary_mod_price_reversal = 0.0

                # Check each modifier against the primary list first
                for _, mod_row in modifiers_reversal.iterrows():
                    if mod_row['productName'] in primary_mod_list_reversal and mod_row['productName'] not in used_modifiers_reversal:
                        primary_mod_reversal = mod_row['productName']
                        primary_mod_price_reversal = mod_row['totalPrice']
                        used_modifiers_reversal.add(primary_mod_reversal)
                        break

                # If there is a secondary list, check against it
                for _, mod_row in modifiers_reversal.iterrows():
                    if mod_row['productName'] in secondary_mod_list_reversal and mod_row['productName'] not in used_modifiers_reversal:
                        secondary_mod_reversal = mod_row['productName']
                        secondary_mod_price_reversal = mod_row['totalPrice']
                        used_modifiers_reversal.add(secondary_mod_reversal)
                        break

                return primary_mod_reversal, secondary_mod_reversal, primary_mod_price_reversal, secondary_mod_price_reversal

            return None, None, 0.0, 0.0  # Ensure four values are returned

        used_modifiers_by_order_reversal = {order_id: set()
                                            for order_id in df_filter_mod_reversal['orderId'].unique()}
        df_filter_mod_reversal[['modifier_1', 'modifier_2', 'modifier_1_price', 'modifier_2_price']] = df_filter_mod_reversal.apply(
            lambda row: pd.Series(find_modifiers(row, df_filter_mod_reversal, used_modifiers_by_order_reversal[row['orderId']])), axis=1
        )

        # Create the 'new_name' column
        df_filter_mod_reversal['new_name'] = df_filter_mod_reversal.apply(
            lambda row: f"{row['productName']} {row['modifier_1']} {row['modifier_2']}".strip(), axis=1
        )

        # Ensuring that 'modifier_1_price' and 'modifier_2_price' are converted to numeric values
        df_filter_mod_reversal['modifier_1_price'] = pd.to_numeric(
            df_filter_mod_reversal['modifier_1_price'], errors='coerce').fillna(0)
        df_filter_mod_reversal['modifier_2_price'] = pd.to_numeric(
            df_filter_mod_reversal['modifier_2_price'], errors='coerce').fillna(0)

        # Create the new column with the calculation
        df_filter_mod_reversal['total_with_modifiers'] = df_filter_mod_reversal['totalPrice'] + (
            df_filter_mod_reversal['quantity'] *
            (df_filter_mod_reversal['modifier_1_price'] +
             df_filter_mod_reversal['modifier_2_price'])
        )

        # Final base modifiers
        df_filter_mod_vf_reversal = df_filter_mod_reversal[['orderId', 'new_name', 'menuCategoryName',
                                                            'menuSectionName', 'type', 'total_with_modifiers', 'quantity', 'kind', 'status']]
        df_mod_f_reversal = df_filter_mod_vf_reversal.rename(
            columns={'new_name': 'productName', 'total_with_modifiers': 'totalPrice'})
        df_mod_f_reversal = df_mod_f_reversal[df_mod_f_reversal['type'] == 'menu_item']

        # Concat tables
        df_full_reversal = df_no_modifier_reversal[['orderId', 'productName', 'menuCategoryName',
                                                    'menuSectionName', 'type', 'totalPrice', 'quantity', 'kind', 'status']]
        df_combined_reversal = pd.concat(
            [df_mod_f_reversal, df_full_reversal], ignore_index=True)

        valid_reversal = df_combined_reversal[df_combined_reversal['kind'] == 'reversal']

        # Reporting valid
        result_reversal = valid_reversal.groupby(['productName', 'menuCategoryName', 'menuSectionName']).agg(
            count=('quantity', 'sum'),
            total_price=('totalPrice', 'sum')
        ).reset_index()

        result_reversal = result_reversal.rename(columns={
            'productName': 'Product Name',
            'menuCategoryName': 'Category',
            'menuSectionName': 'Section',
            'count': 'Quantity',
            'total_price': 'Total Price'})

        df_sorted_reversal = result_reversal.sort_values(
            by=['Category', 'Section', 'Product Name'], ascending=[True, True, True])

        df_sum_reversal = df_sorted_reversal['Total Price'].sum()
        df_sorted_reversal['Quantity'] = df_sorted_reversal['Quantity'] * -1
        df_af_sum = df['totalPrice'].sum()
        # df_sorted['Total Price'] = df_sorted['Total Price'].str.replace('$', '').astype(float)
        df_final = pd.concat([df_sorted, df_sorted_reversal])
        df_final = df_final.groupby(['Category', 'Section', 'Product Name'], as_index=False).agg({
            'Quantity': 'sum', 'Total Price': 'sum'})
        df_final = df_final[df_final['Quantity'] > 0]
        df_final_sum = df_final['Total Price'].sum()

        def highlight_rows(row):
            if row['Quantity'] > 5:
                return ['background-color: red; color: black;' for _ in row]
            elif row['Quantity'] > 4:
                return ['background-color: orange; color: black;' for _ in row]
            elif row['Quantity'] > 3:
                return ['background-color: pink; color: black;' for _ in row]
            elif row['Quantity'] > 2:
                return ['background-color: lightgreen; color: black;' for _ in row]
            elif row['Quantity'] > 1:
                return ['background-color: yellow; color: black;' for _ in row]
            else:
                return ['' for _ in row]

        # Apply the style
        df_final = df_final.reset_index(drop=True)
        df_final = df_final.sort_values(
            by=['Category', 'Section', 'Product Name'], ascending=[True, True, True])
        df_final['Total Price'] = df_final['Total Price'].apply(
            lambda x: f"${x:,.2f}")
        df_final['Quantity'] = df_final['Quantity'].astype(int)
        df_final = df_final.style.apply(highlight_rows, axis=1)

        st.dataframe(df_final, use_container_width=True, height=850)
        st.write(f"Total refunded: $ {df_sum_reversal:.2f}")
        st.write(f"Total sales: $ {df_af_sum:.2f}")
        st.write(f"Total sales - refund: $ {df_final_sum:.2f}")

        if df_final_sum == df_af_sum:
            st.markdown(
                '<p style="color:green;">Validation: CORRECT - OK</p>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<p style="color:red;">Validation: INCORRECT - NOK</p>', unsafe_allow_html=True)
    else:
        df_st['Total Price'] = df_st['Total Price'].apply(
            lambda x: f"${x:,.2f}")
        df_st['Quantity'] = df_st['Quantity'].astype(int)
        df_st = df_st.style.apply(highlight_rows, axis=1)
        st.dataframe(df_st, use_container_width=True, height=850)
        df_af_sum = df['totalPrice'].sum()
        st.write(f"Total sales: $ {df_af_sum:.2f}")
        st.write(f"Total sales - validation: $ {df_st_sum:.2f}")
        st.write("No refund today :)")
        if df_af_sum == df_st_sum:
            st.markdown(
                '<p style="color:green;">Validation: CORRECT - OK</p>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<p style="color:red;">Validation: INCORRECT - NOK</p>', unsafe_allow_html=True)

# Button to toggle the DataFrame visibility
if uploaded_file is not None:
    if st.button('Show Full File'):
        if uploaded_file is not None:
            st.dataframe(df)
        else:
            st.warning('You must upload a ".csv" file')
if uploaded_file is not None:
    if st.button('Show Refunds'):
        if uploaded_file is None:
            st.warning('You must upload a ".csv" file')
        elif q_df1 != 0 or q_df2 != 0:
            st.dataframe(df_sorted_reversal)
        else:
            st.warning('No refund today')
