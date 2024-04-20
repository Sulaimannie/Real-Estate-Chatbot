from flask import Flask, request, jsonify
import random
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a DataFrame
df = pd.read_csv('C://xampp//htdocs//PythonFYP//data.csv')

# Define general bot responses
greetings = ["Hi there!", "Hello!", "Hey!", "Greetings!"]
farewells = ["Goodbye!", "See you later!", "Farewell!"]

# Function to answer questions and handle greetings/farewells
def chatbot_response(question):
    if any(word in question.lower() for word in ['hi', 'hello', 'hey', 'greetings', 'my name is']):
        return random.choice(greetings)
    elif any(word in question.lower() for word in ['bye', 'goodbye', 'see you']):
        return random.choice(farewells)
    else:
        # Parse the question and identify what information is being asked
        if 'show me apartments in dubai for 3000 aed' in question.lower():
            return get_apartments_in_dubai_for_3000_aed()
        elif 'list of apartments with 70 square meter dimensions' in question.lower():
            return get_apartments_with_70_square_meter_dimensions()
        elif 'one bed apartments' in question.lower():
            return get_available_one_bed_apartments()
        elif 'apartments near dubai mall' in question.lower():
            return get_apartments_near_dubai_mall()
        elif 'properties' in question.lower() and 'business bay' in question.lower():
            return get_properties_in_business_bay()
        elif 'properties' in question.lower() and 'dubai' in question.lower():
            return get_properties_in_dubai()
        elif 'average price' in question.lower() and 'dubai' in question.lower():
            return get_average_price_in_dubai()
        elif 'average price' in question.lower() and 'business bay' in question.lower():
            return get_average_price_in_business_bay()
        elif 'bedrooms' in question.lower():
            return get_bedrooms_info()
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
        else:
            return "I'm sorry, I don't understand that question."

# Function to get properties in Business Bay
# Function definitions for getting property information
def get_properties_in_business_bay():
    properties = df[df['Area'] == 'BUSINESS BAY'][['Usage', 'Property Sub Type', 'Amount', 'Property Size (sq.m)', 'Room(s)', 'Parking', 'Nearest Metro', 'Nearest Mall', 'Nearest Landmark']]
    return properties.to_dict(orient='records')

def get_properties_in_dubai():
    properties = df['Property Type'].unique()
    return properties.tolist()

# Function to get average price in Business Bay
def get_average_price_in_dubai():
    average_price = df['Amount'].mean()
    return f"The average price in Dubai is AED {average_price:.2f}."
# Function to get average price in Business Bay
def get_average_price_in_business_bay():
    average_price = df[df['Area'] == 'BUSINESS BAY']['Amount'].mean()
    return f"The average price in Business Bay is AED {average_price:.2f}."

# Function to get generic bedrooms information
def get_bedrooms_info():
    bedrooms_info = df['Room(s)'].value_counts().to_dict()
    return bedrooms_info

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

# Function to get apartments in Dubai for 3000 AED
def get_apartments_in_dubai_for_3000_aed():
    # Assuming a range of 2000 to 4000 AED for the example
    lower_limit = 2000
    upper_limit = 10000000000
    apartments = df[(df['Area'] == 'DUBAI') & (df['Amount'] >= lower_limit) & (df['Amount'] <= upper_limit)]['Property Type'].unique()
    return f"Apartments in Dubai within the range of AED {lower_limit} to AED {upper_limit}: {apartments.tolist()}"


# Function to get apartments with 70 square meter dimensions
def get_apartments_with_70_square_meter_dimensions():
    apartments = df[df['Transaction Size (sq.m)'] == 70]['Property Type'].unique()
    return apartments.tolist()

# Function to get available one bed apartments
def get_available_one_bed_apartments():
    one_bed_apartments = df[df['Room(s)'] == '1 B/R']['Property Type'].unique()
    return one_bed_apartments.tolist()

# Function to get apartments near Dubai Mall
def get_apartments_near_dubai_mall():
    apartments_near_dubai_mall = df[df['Nearest Mall'] == 'Dubai Mall']['Property Type'].unique()
    return apartments_near_dubai_mall.tolist()


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
