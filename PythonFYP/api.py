from flask import Flask, request, jsonify
import random
import pandas as pd
import re
app = Flask(__name__)

# Load the CSV file into a DataFrame
df = pd.read_csv('C://Users//sulai//Downloads//PythonFYP//data.csv')

# Drop all rows with NaN values
df.fillna({'Property Size (sq.m)': 0, 'Parking': 0}, inplace=True)

# Define general bot responses
greetings = ["Hi there!", "Hello!", "Hey!", "Greetings!"]
farewells = ["Goodbye!", "See you later!", "Farewell!"]
property_subtypes = {'Hotel Apartments', 'Industrial', 'Residential', 'Office', 'Sports Club', 'Building', 'Flats', 'Land', 'Commercial', 'Villas', 'General Use', 'Shop', 'Government Housing', 'Hotel Rooms', 'Residential Flats'}

# Function to answer questions and handle greetings/farewells
def chatbot_response(question):
    if any(word in question.lower() for word in ['hi', 'hello', 'hey', 'greetings']):
        return random.choice(greetings)
    elif any(word in question.lower() for word in ['bye', 'goodbye', 'see you']):
        return random.choice(farewells)
    else:
        # Parse the question and identify what information is being asked
        if ' apartment price' in question.lower() or 'AED' in question.lower():
            # Extract the target amount from the question
            target_amount = None
            for word in question.lower().split():
                if word.isdigit():
                    target_amount = int(word)
                    break
            if target_amount:
                return get_apartments_at_target_amount(target_amount)
            else:
                return "I'm sorry, I couldn't determine the target amount from your query."

        elif 'what is your job' in question.lower():
            return "I'm a chatbot designed to provide information about Dubai real estate data."
        
        elif 'over' in question.lower() or 'above' in question.lower() or "aed" in question.lower():
            # Extract the property subtype and amount from the question using regular expressions
            property_subtype_pattern = r'([a-zA-Z\s]+) (over|above)'
            amount_pattern = r'(\d+)'
            property_subtype_match = re.search(property_subtype_pattern, question, flags=re.IGNORECASE)
            if property_subtype_match:
                property_subtype = property_subtype_match.group(1).strip().split()[-1]
            else:
                return "Property subtype not found in the question."
            amount_match = re.search(amount_pattern, question)
            if amount_match:
                amount = int(amount_match.group())
            else:
                return "Amount not found in the question."
            return get_properties_above_amount(property_subtype, amount)
        
        elif 'under' in question.lower() or "aed" in question.lower():
            # Extract the property subtype and amount from the question using regular expressions
            property_subtype_pattern = r'([a-zA-Z\s]+) under'
            amount_pattern = r'(\d+)'
            property_subtype_match = re.search(property_subtype_pattern, question, flags=re.IGNORECASE)
            if property_subtype_match:
                property_subtype = property_subtype_match.group(1).strip().split()[-1]
            else:
                return "Property subtype not found in the question."
            amount_match = re.search(amount_pattern, question)
            if amount_match:
                amount = int(amount_match.group())
            else:
                return "Amount not found in the question."
            return get_properties_under_amount(property_subtype, amount)

        elif 'cheap' in question.lower() and ('with' in question.lower() or 'beds' in question.lower()):
            # Parse the question to extract the property subtype and number of beds
            property_subtype = None
            num_beds = None
            for subtype in df['Property Sub Type'].unique():
                if subtype and subtype != "nan":
                    if re.search(r'\b' + re.escape(str(subtype)) + r'\b', question.lower()):
                        property_subtype = str(subtype)
                        break
                    elif subtype.lower() in question.lower():
                        property_subtype = str(subtype)
                        break
            for word in question.split():
                if word.isdigit():
                    num_beds = int(word)
                    break
            
            print(property_subtype, num_beds)
            if property_subtype and num_beds:
                return get_cheap_properties_x(property_subtype, num_beds)
            else:
                return "Could not determine the property subtype or number of beds."

        elif 'cheap' in question.lower() or 'lowest price' in question.lower():
            return get_cheap_properties()

        elif 'show me all' in question.lower() and 'with' in question.lower() or 'beds' in question.lower() or 'bedrooms' in question.lower():
            # Extract property type and number of bedrooms from the query
            words = question.split()
            property_type = None
            num_bedrooms = None
            for i, word in enumerate(words):
                if word == 'all':
                    if i+1 < len(words):
                        property_type = words[i+1]
                if word.isdigit():
                    num_bedrooms = int(word)
            if property_type and num_bedrooms:
                result = get_properties_with_specific_bedrooms(property_type, num_bedrooms)
                if result:
                    return result
                else:
                    return "No records found."
            else:
                return "I'm sorry, I couldn't determine the property type or number of bedrooms from your query."

        elif 'near' in question.lower():
            # Extract property subtype and location from the query
            words = question.split()
            property_subtype = None
            location = None
            for i, word in enumerate(words):
                if word.lower() == 'near':
                    property_subtype = words[i-1].lower()
                    potential_location = ' '.join(words[i+1:])
                    if potential_location.title() in property_subtypes:
                        location = potential_location.title()
                        break
                    else:
                        location = potential_location.title()
                        break
            if property_subtype and location:
                return get_properties_near_location(property_subtype, location)
            else:
                return "I'm sorry, I couldn't determine the property subtype or location from your query."

        elif 'list of apartments with 70 square meter dimensions' in question.lower():
            return get_apartments_with_70_square_meter_dimensions()

        elif 'apartments with square meter dimensions' in question.lower() or 'square meter dimensions' in question.lower():
            # Extract the square meter dimensions from the question
            square_meter = None
            for word in question.lower().split():
                try:
                    square_meter = float(word)
                    break
                except ValueError:
                    continue
            if square_meter:
                return get_apartments_with_specific_square_meter_dimensions(square_meter)
            else:
                return "I'm sorry, I couldn't determine the square meter dimensions from your query."

        elif 'bed apartments' in question.lower() or 'bedroom apartments' in question.lower() or '':
            # Extract the number of bedrooms from the query
            num_bedrooms = None
            for word in question.lower().split():
                if word.isdigit():
                    num_bedrooms = int(word)
                    break
            if num_bedrooms:
                return get_available_bedroom_apartments(num_bedrooms)
            else:
                return "I'm sorry, I couldn't determine the number of bedrooms from your query."

        elif 'apartments near dubai mall' in question.lower():
            return get_apartments_near_dubai_mall()
        
        elif 'average price of properties in dubai' in question.lower():
            print("average")
            return get_average_price_in_dubai()

        elif 'average price' in question.lower() and 'business bay' in question.lower():
            return get_average_price_in_business_bay()

        elif 'properties' in question.lower() and 'business bay' in question.lower():
            return get_properties_in_business_bay()

        elif 'show me all properties' in question.lower():
            # Extract the number of bedrooms from the query
            num_bedrooms = None
            for word in question.lower().split():
                if word.isdigit():
                    num_bedrooms = int(word)
                    break
            if num_bedrooms:
                return get_bedrooms_info(num_bedrooms)
            else:
                return "I'm sorry, I couldn't determine the number of bedrooms from your query."

        elif 'nearest metro' in question.lower():
            return get_nearest_metro_info()

        elif 'registration type' in question.lower():
            return get_registration_type_info()

        elif 'buyers' in question.lower():
            return get_buyers_info()

        elif 'project name' in question.lower():
            return get_project_name_info()

        elif 'usage' in question.lower():
            return get_usage_info()

        elif 'parking' in question.lower():
            return get_parking_info()

        elif 'nearest landmark' in question.lower():
            return get_nearest_landmark_info()
        
        elif 'properties' in question.lower():
            # Extract the area name from the query
            area_indicators = ['in', 'at', 'located', 'near', 'around', 'within']
            area = None
            words = question.split()
            for i, word in enumerate(words):
                if word.lower() in area_indicators and i < len(words) - 1:
                    area = words[i+1].upper()
                    break
            if area:
                return get_properties_in_area(area)
            else:
                return "I'm sorry, I couldn't determine the area name from your query."

        elif 'properties' in question.lower() and ' in dubai' in question.lower():
            return get_properties_in_dubai()

        else:
            return "I'm sorry, I don't understand that question."

# Function to get properties above a specified amount
def get_properties_above_amount(property_subtype, amount):
    filtered_properties = df[(df['Property Sub Type'].str.contains(re.compile(f'\\b{re.escape(property_subtype)}s?\\b', re.IGNORECASE))) & (df['Amount'] >= amount)]
    if filtered_properties.empty:
        return f"No {property_subtype} properties found above {amount} AED."
    formatted_properties = []
    for _, property_record in filtered_properties.iterrows():
        formatted_property = (
            f"Property Sub Type: {property_record['Property Sub Type']}\n"
            f"Amount: {property_record['Amount']}\n"
            f"Property Size (sq.m): {property_record['Property Size (sq.m)']}\n"
            f"Room(s): {property_record['Room(s)']}\n"
            f"Parking: {property_record['Parking']}\n"
            f"Nearest Metro: {property_record['Nearest Metro']}\n"
            f"Nearest Mall: {property_record['Nearest Mall']}\n"
            f"Nearest Landmark: {property_record['Nearest Landmark']}"
        )
        formatted_properties.append(formatted_property)
    return '\n\n'.join(formatted_properties)

# Function to get properties under a specified amount
def get_properties_under_amount(property_subtype, amount):
    filtered_properties = df[(df['Property Sub Type'].str.contains(re.compile(f'\\b{re.escape(property_subtype)}s?\\b', re.IGNORECASE))) & (df['Amount'] <= amount)]
    if filtered_properties.empty:
        return f"No {property_subtype} properties found under {amount} AED."
    formatted_properties = []
    for _, property_record in filtered_properties.iterrows():
        formatted_property = (
            f"Property Sub Type: {property_record['Property Sub Type']}\n"
            f"Amount: {property_record['Amount']}\n"
            f"Property Size (sq.m): {property_record['Property Size (sq.m)']}\n"
            f"Room(s): {property_record['Room(s)']}\n"
            f"Parking: {property_record['Parking']}\n"
            f"Nearest Metro: {property_record['Nearest Metro']}\n"
            f"Nearest Mall: {property_record['Nearest Mall']}\n"
            f"Nearest Landmark: {property_record['Nearest Landmark']}"
        )
        formatted_properties.append(formatted_property)
    return '\n\n'.join(formatted_properties)

# Function to get properties with the lowest price for a specific property subtype and number of beds
def get_cheap_properties_x(property_subtype, num_beds):
    filtered_properties = df[(df['Property Sub Type'].str.contains(re.compile(f'\\b{re.escape(property_subtype)}s?\\b', re.IGNORECASE))) & (df['Room(s)'].str.lower() == f'{num_beds} b/r')]
    if filtered_properties.empty:
        return "No properties found with the specified property subtype and number of beds."
    min_amount = filtered_properties['Amount'].min()
    cheap_properties = filtered_properties[filtered_properties['Amount'] == min_amount]
    formatted_properties = []
    for _, property_record in cheap_properties.iterrows():
        formatted_property = (
            f"Property Sub Type: {property_record['Property Sub Type']}\n"
            f"Amount: {property_record['Amount']}\n"
            f"Property Size (sq.m): {property_record['Property Size (sq.m)']}\n"
            f"Room(s): {property_record['Room(s)']}\n"
            f"Parking: {property_record['Parking']}\n"
            f"Nearest Metro: {property_record['Nearest Metro']}\n"
            f"Nearest Mall: {property_record['Nearest Mall']}\n"
            f"Nearest Landmark: {property_record['Nearest Landmark']}"
        )
        formatted_properties.append(formatted_property)
    return '\n\n'.join(formatted_properties)

def get_properties_under_amount(property_subtype, amount):
    # Filter the DataFrame for the specified property subtype and amount
    filtered_properties = df[(df['Property Sub Type'].str.contains(re.compile(f'\\b{re.escape(property_subtype)}s?\\b', re.IGNORECASE))) & (df['Amount'] <= amount)]

    # If there are no properties matching the criteria, return a message
    if filtered_properties.empty:
        return f"No {property_subtype} properties found under {amount} AED."

    # Create a list to store formatted property information
    formatted_properties = []

    # Iterate through each property record and format it
    for _, property_record in filtered_properties.iterrows():
        formatted_property = (
            f"Property Sub Type: {property_record['Property Sub Type']}\n"
            f"Amount: {property_record['Amount']}\n"
            f"Property Size (sq.m): {property_record['Property Size (sq.m)']}\n"
            f"Room(s): {property_record['Room(s)']}\n"
            f"Parking: {property_record['Parking']}\n"
            f"Nearest Metro: {property_record['Nearest Metro']}\n"
            f"Nearest Mall: {property_record['Nearest Mall']}\n"
            f"Nearest Landmark: {property_record['Nearest Landmark']}"
        )
        formatted_properties.append(formatted_property)


    return '\n\n'.join(formatted_properties)

# def get_cheap_properties_x(property_subtype, num_beds):
#     # Filter the DataFrame for the specified property subtype and number of beds
#     filtered_properties = df[(df['Property Sub Type'] == property_subtype) & (df['Room(s)'] == num_beds)]

#     # If there are no properties matching the criteria, return a message
#     if filtered_properties.empty:
#         return "No properties found with the specified property subtype and number of beds."

#     # Find the minimum amount among the filtered properties
#     min_amount = filtered_properties['Amount'].min()

#     # Filter the DataFrame to get properties with the lowest amount for the specified subtype and number of beds
#     cheap_properties = filtered_properties[filtered_properties['Amount'] == min_amount]

#     # Create a list to store formatted property information
#     formatted_properties = []

#     # Iterate through each property record and format it
#     for _, property_record in cheap_properties.iterrows():
#         formatted_property = (
#             f"Property Sub Type: {property_record['Property Sub Type']}\n"
#             f"Amount: {property_record['Amount']}\n"
#             f"Property Size (sq.m): {property_record['Property Size (sq.m)']}\n"
#             f"Room(s): {property_record['Room(s)']}\n"
#             f"Parking: {property_record['Parking']}\n"
#             f"Nearest Metro: {property_record['Nearest Metro']}\n"
#             f"Nearest Mall: {property_record['Nearest Mall']}\n"
#             f"Nearest Landmark: {property_record['Nearest Landmark']}"
#         )
#         formatted_properties.append(formatted_property)

#     return '\n\n'.join(formatted_properties)

# Define function to handle query for cheap or lowest price properties
def get_cheap_properties():
    # Group by 'Property Sub Type' and find the minimum amount within each group
    min_amount_per_subtype = df.groupby('Property Sub Type')['Amount'].min()

    # Create a list to store formatted property information
    formatted_properties = []

    # Iterate through each unique property subtype
    for subtype, min_amount in min_amount_per_subtype.items():
        # Filter the DataFrame to get the property with the lowest amount for the current subtype
        cheap_property = df[(df['Property Sub Type'] == subtype) & (df['Amount'] == min_amount)].iloc[0]

        # Format the property record
        formatted_property = (
            f"Property Sub Type: {cheap_property['Property Sub Type']}\n"
            f"Amount: {cheap_property['Amount']}\n"
            f"Property Size (sq.m): {cheap_property['Property Size (sq.m)']}\n"
            f"Room(s): {cheap_property['Room(s)']}\n"
            f"Parking: {cheap_property['Parking']}\n"
            f"Nearest Metro: {cheap_property['Nearest Metro']}\n"
            f"Nearest Mall: {cheap_property['Nearest Mall']}\n"
            f"Nearest Landmark: {cheap_property['Nearest Landmark']}"
        )
        formatted_properties.append(formatted_property)

    return '\n\n'.join(formatted_properties)



    



# Function to get properties with a specific property type and number of bedrooms
def get_properties_with_specific_bedrooms(property_type, num_bedrooms):
    # Convert property type to lowercase for case-insensitive comparison
    properties = df[(df['Property Sub Type'].str.contains(re.compile(f'\\b{re.escape(property_type)}s?\\b', re.IGNORECASE))) & 
                    (df['Room(s)'].str.lower() == f'{num_bedrooms} b/r')]
                   
    property_records = properties.head(50).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)
# Function to get properties near a specific location
def get_properties_near_location(property_subtype, location):
    # Convert property subtype and location to lowercase for case-insensitive comparison
    properties = df[(df['Property Sub Type'].str.contains(re.compile(f'\\b{re.escape(property_subtype)}\\b', re.IGNORECASE))) & 
                    (df[['Nearest Metro', 'Nearest Mall', 'Nearest Landmark']].apply(lambda x: x.str.contains(re.compile(f'\\b{re.escape(location)}\\b', re.IGNORECASE))).any(axis=1))][['Usage', 'Area', 'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = properties.head(50).to_dict(orient='records')

    # Create a list to store formatted property information
    formatted_properties = []

    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)

    return '\n'.join(formatted_properties)



# Function to get apartments with specific square meter dimensions
def get_apartments_with_specific_square_meter_dimensions(square_meter):
    # Convert the square meter value to float to handle decimal points
    square_meter = float(square_meter)
    # Filter apartments with approximately matching square meter dimensions
    apartments = df[df['Transaction Size (sq.m)'].between(square_meter - 0.01, square_meter + 0.01)][['Usage', 'Area' ,'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = apartments.head(15).to_dict(orient='records')
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)
def get_properties_in_area(area):
    area = area.upper()  # Convert the area to uppercase to ensure case insensitivity
    properties = df[df['Area'].str.upper() == area][['Usage', 'Area' ,'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = properties.head(15).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)

def get_properties_in_business_bay():
    properties = df[df['Area'] == 'BUSINESS BAY'][['Usage', 'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = properties.head(15).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)

# Modified function
def get_apartments_at_target_amount(target_amount):
    # Fetch apartments with the specified rental amount
    apartments = df[df['Amount'] == target_amount]
    
    # Check if there are any apartments with the specified amount
    if not apartments.empty:
        # Limit the number of records to 50
        apartments = apartments.head(50)
        
        # Convert property records to a list of dictionaries
        property_records = apartments.to_dict(orient='records')
        
        # Create a list to store formatted property information
        formatted_properties = []
        
        # Iterate through each property record and format it
        for prop in property_records:
            formatted_property = ""
            for key, value in prop.items():
                formatted_property += f"- {key}: {value}\n"
            formatted_properties.append(formatted_property)
        
        return '\n'.join(formatted_properties)
    else:
        return f"No apartments found in Dubai with a rental amount of AED {target_amount}."
def get_properties_in_dubai():
    properties = df[['Usage', 'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = properties.head(50).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)

# Function to get average price in Business Bay
def get_average_price_in_dubai():
    average_price = df['Amount'].mean()
  
    return f"The average price in Dubai is AED {average_price:.2f}."
# Function to get average price in Business Bay
def get_average_price_in_business_bay():
    average_price = df[df['Area'] == 'BUSINESS BAY']['Amount'].mean()
    return f"The average price in Business Bay is AED {average_price:.2f}."

# Function to get generic bedrooms information
def get_bedrooms_info(num_bedrooms):
    # Convert property type to lowercase for case-insensitive comparison
    properties = df[(df['Room(s)'].str.lower() == f'{num_bedrooms} b/r')]
    print(properties)
                   
    property_records = properties.head(50).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)

# Function to get generic nearest metro information
def get_nearest_metro_info():
    nearest_metro_info = df['Nearest Metro'].value_counts().to_dict()
    return nearest_metro_info

# Function to get generic registration type information
def get_registration_type_info():
    reg_type_info = df['Registration type'].value_counts().to_dict()
    return reg_type_info

# Function to get generic number of buyers information
def get_buyers_info():
    buyers_info = df['No. of Buyer'].sum()
    return f"The total number of buyers across all properties is {buyers_info}."

# Function to get generic project name information
def get_project_name_info():
    project_name_info = df['Project'].value_counts().to_dict()
    return project_name_info

# Function to get generic usage information
def get_usage_info():
    usage_info = df['Usage'].value_counts().to_dict()
    return usage_info

# Function to get generic parking information
def get_parking_info():
    parking_info = df['Parking'].value_counts().to_dict()
    return parking_info

# Function to get generic nearest landmark information
def get_nearest_landmark_info():
    nearest_landmark_info = df['Nearest Landmark'].value_counts().to_dict()
    return nearest_landmark_info

def get_apartments_above_3000_aed():
    # Define the lower limit as 3000 AED
    lower_limit = 3000
    # Fetch apartments above 3000 AED
    apartments = df[(df['Amount'] > lower_limit)]
    # Check if there are any apartments above 3000 AED
    if not apartments.empty:
        # Limit the number of records to 50
        apartments = apartments.head(50)
        # Convert property records to a list of dictionaries
        property_records = apartments.to_dict(orient='records')
        
        # Create a list to store formatted property information
        formatted_properties = []
        
        # Iterate through each property record and format it
        for prop in property_records:
            formatted_property = ""
            for key, value in prop.items():
                formatted_property += f"- {key}: {value}\n"
            formatted_properties.append(formatted_property)
        
        return '\n'.join(formatted_properties)
    else:
        return f"No apartments found in Dubai above AED {lower_limit}."




# Function to get apartments with 70 square meter dimensions
def get_apartments_with_70_square_meter_dimensions():
    apartments = df[df['Transaction Size (sq.m)'] == 70]['Property Type'].unique()
    return apartments.tolist()

# Modify get_available_one_bed_apartments to accept a parameter for the number of bedrooms
def get_available_bedroom_apartments(num_bedrooms):
    apartments = df[df['Room(s)'] == f'{num_bedrooms} B/R'][['Usage', 'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = apartments.head(50).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)

# Function to get apartments near Dubai Mall
def get_apartments_near_dubai_mall():
    apartments_near_dubai_mall = df[df['Nearest Mall'] == 'Dubai Mall'][['Usage', 'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    property_records = apartments_near_dubai_mall.head(50).to_dict(orient='records')
    
    # Create a list to store formatted property information
    formatted_properties = []
    
    # Iterate through each property record and format it
    for prop in property_records:
        formatted_property = ""
        for key, value in prop.items():
            formatted_property += f"- {key}: {value}\n"
        formatted_properties.append(formatted_property)
    
    return '\n'.join(formatted_properties)



# API Route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data['question']
    response = chatbot_response(question)
    return jsonify({'response': response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
