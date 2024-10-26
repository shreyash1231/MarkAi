# em.py
import os
import google.generativeai as genai
from googletrans import Translator
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_marketing_emails(product_details, csv_file_path):
    os.environ["API_KEY"] = 'AIzaSyC8z6KpLFjp6qGEYC2yBMr5vcb9rGM0RdY'
    genai.configure(api_key=os.environ["API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    df = pd.read_csv(csv_file_path)
    name_list = df['Name'].tolist()
    state_ut_list = df['State/UT'].tolist()
    email_list = df["Email"].tolist()

    language_codes = {
        "england": "en", "spain": "es", "france": "fr", "germany": "de",
        "hindi": "hi", "bengal": "bn", "gujarat": "gu", "karnataka": "kn",
        "kerala": "ml", "maharashtra": "mr", "punjab": "pa", "tamilnadu": "ta",
        "telangana": "te", "odisha": "or"
    }

    translator = Translator()
    product_name = product_details['name']
    product_desc = product_details['description']

    for name, email in zip(name_list, email_list):
        user_input = f"write a marketing email with keyword '{product_name}' and '{product_desc}' to customer '{name}'"

        try:
            response = model.generate_content(user_input)
            output_lines = response.text.split('\n')
            subject = output_lines[0] if output_lines else "No subject generated"
            content = '\n'.join(output_lines[1:]) if len(output_lines) > 1 else ""

            for state in state_ut_list:
                state = state.lower()
                if state in language_codes:
                    target_lang = language_codes[state]
                    translated = translator.translate(content, dest=target_lang)

                    smtp = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login('mayurpc2002@gmail.com', 'rxta zdpe yrmc crhk')

                    msg = MIMEMultipart()
                    msg['From'] = 'mayurpc2002@gmail.com'
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(translated.text, 'plain'))

                    smtp.sendmail('mayurpc2002@gmail.com', email, msg.as_string())
                    smtp.quit()

                    print(f"Email sent successfully to {email}.")

        except Exception as e:
            print(f"An error occurred: {e}")
