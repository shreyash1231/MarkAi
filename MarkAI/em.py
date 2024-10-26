
import os
import app
from flask import session
import pandas as pd
import google.generativeai as genai
from googletrans import Translator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set the new API key
os.environ["API_KEY"] = 'AIzaSyC8z6KpLFjp6qGEYC2yBMr5vcb9rGM0RdY'  # Replace with your new API key
genai.configure(api_key=os.environ["API_KEY"])

# Create the model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Load the CSV file into a DataFrame
csv_file_path = "MarkAI\custom_dataset.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path)

# Extract the 'Name', 'State/UT', and 'Email' columns and convert them to lists
name_list = df['Name'].tolist()
state_ut_list = df['State/UT'].tolist()
email_list = df["Email"].tolist()  # Get the list of emails from the DataFrame

# Creating a dictionary of language codes
language_codes = {
    "england": "en",
    "spain": "es",
    "france": "fr",
    "germany": "de",
    "hindi": "hi",
    "bengal": "bn",
    "gujarat": "gu",
    "karnataka": "kn",
    "kerala": "ml",
    "maharashtra": "mr",
    "punjab": "pa",
    "tamilnadu": "ta",
    "telangana": "te",
    "odisha": "or",
}

# Initialize the translator
translator = Translator()

# Loop through each name to generate marketing email
for name, email in zip(name_list, email_list):
    # product_name = app.product_name
    # product_desc = app.product_description
    product_name = session.get('product_details', {}).get('name', 'Default Product Name')
    product_desc = session.get('product_details', {}).get('description', 'Default Product Description')

    # Generate user input for the content generation
    user_input = f"write a marketing email with keyword '{product_name}' and '{product_desc}' to customer '{name}'"
    
    # Generate the content based on user input
    try:
        response = model.generate_content(user_input)
        output_lines = response.text.split('\n')
        subject = output_lines[0] if output_lines else "No subject generated"
        content = '\n'.join(output_lines[1:]) if len(output_lines) > 1 else ""

        # Print the subject and content
        print(f"Subject: {subject}")
        print(f"Content: {content}")

        # Loop through states to translate the email content
        for state in state_ut_list:
            state = state.lower() 
            if state in language_codes:
                target_lang = language_codes[state]
                
                # Perform the translation
                translated = translator.translate(content, dest=target_lang)
                
                # Display the translated text
                print(f"\nTranslating to {translated.dest.title()}:")
                print(translated.text)

                # Send email
                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.ehlo()
                smtp.starttls()
                smtp.login('mayurpc2002@gmail.com', 'rxta zdpe yrmc crhk')  # Your email credentials
                
                # Create email message
                msg = MIMEMultipart()
                msg['From'] = 'mayurpc2002@gmail.com'
                msg['To'] = email  # Set the recipient email
                msg['Subject'] = subject
                msg.attach(MIMEText(translated.text, 'plain'))

                # Send email
                smtp.sendmail(from_addr='mayurpc2002@gmail.com', to_addrs=email, msg=msg.as_string())
                smtp.quit()
                
                print(f"Email sent successfully to {email}.")

    except Exception as e:
        print(f"An error occurred: {e}")
