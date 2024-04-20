import random
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('C://xampp//htdocs//PythonFYP//data.csv')

# Define general bot responses
greetings = ["Hi there!", "Hello!", "Hey!", "Greetings!"]
farewells = ["Goodbye!", "See you later!", "Farewell!"]

# Preprocess the data if necessary
# For example, handle missing values, convert data types, etc.

# Define a function to answer questions
def answer_question(question):
    # Parse the question and identify what information is being asked
    # For example, extract keywords from the question
    if 'properties' in question.lower() and 'dubai' in question.lower():
        return get_properties_in_business_bay()
    elif 'average price' in question.lower() and 'dubai' in question.lower():
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
    elif any(word in question.lower() for word in ['hi', 'hello', 'hey', 'greetings']):
        return greet()
    elif any(word in question.lower() for word in ['bye', 'goodbye', 'see you']):
        return farewell()

    else:
        return "I'm sorry, I don't understand that question."

# Function to greet the user
def greet():
    return random.choice(greetings)

# Function to bid farewell to the user
def farewell():
    return random.choice(farewells)

# Function to get properties in Business Bay
def get_properties_in_business_bay():
    properties = df['Property Type'].unique()
    return properties

# Function to get average price in Business Bay
def get_average_price_in_business_bay():
    average_price = df[df['Area'] == 'BUSINESS BAY']['Amount'].mean()
    return f"The average price in Business Bay is AED {average_price:.2f}."

# Function to get generic bedrooms information
def get_bedrooms_info():
    bedrooms_info = df['Room(s)'].value_counts().to_dict()
    return f"Here is the breakdown of properties by number of bedrooms: {bedrooms_info}"

# Function to get generic nearest metro information
def get_nearest_metro_info():
    nearest_metro_info = df['Nearest Metro'].value_counts().to_dict()
    return f"Here is the breakdown of properties by nearest metro station: {nearest_metro_info}"

# Function to get generic registration type information
def get_registration_type_info():
    reg_type_info = df['Registration type'].value_counts().to_dict()
    return f"Here is the breakdown of properties by registration type: {reg_type_info}"

# Function to get generic number of buyers information
def get_buyers_info():
    buyers_info = df['No. of Buyer'].sum()
    return f"The total number of buyers across all properties is {buyers_info}."

# Function to get generic project name information
def get_project_name_info():
    project_name_info = df['Project'].value_counts().to_dict()
    return f"Here is the breakdown of properties by project name: {project_name_info}"

# Function to get generic usage information
def get_usage_info():
    usage_info = df['Usage'].value_counts().to_dict()
    return f"Here is the breakdown of properties by usage: {usage_info}"

# Function to get generic parking information
def get_parking_info():
    parking_info = df['Parking'].value_counts().to_dict()
    return f"Here is the breakdown of properties by parking availability: {parking_info}"

# Function to get generic nearest landmark information
def get_nearest_landmark_info():
    nearest_landmark_info = df['Nearest Landmark'].value_counts().to_dict()
    return f"Here is the breakdown of properties by nearest landmark: {nearest_landmark_info}"

# Test the chatbot
while True:
    question = input("You: ")
    if question.lower() == 'exit':
        print("Bot:", farewell())
        break
    else:
        answer = answer_question(question)
        print("Bot:", answer)
