# MarkAi
# Customer Sorting and Email Notification System

This project is a Flask-based web application that processes a customer dataset, matches customers to a product based on their interests using an ML model, and sends email notifications in their state-specific language.

## Features
- Upload a customer dataset (CSV format).
- Match customers with a specified product using cosine similarity.
- Send personalized emails to matched customers in their regional language.

## Prerequisites
- Python 3.8+
- Flask
- pandas
- scikit-learn
- smtplib for email integration

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install flask pandas scikit-learn
   ```

3. Configure the email sender:
   - Update the `send_email` function in `app.py` with your email credentials or use Gemini for email creation and delivery.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at:
   ```
   http://127.0.0.1:5000
   ```

## Endpoints

### 1. Upload Dataset
- **URL**: `/upload`
- **Method**: POST
- **Description**: Upload a CSV file containing customer data.
- **Request Format**: Multipart form-data with a file input field named `file`.

### 2. Match and Notify
- **URL**: `/match`
- **Method**: POST
- **Description**: Matches customers with the specified product and sends email notifications.
- **Request Format**:
  ```json
  {
      "product_name": "<product_name>"
  }
  ```

## Customer Dataset Format
The uploaded CSV file should have the following columns:
- `Name`: Customer name
- `Email`: Customer email
- `State`: State where the customer resides
- `Interests`: Keywords describing customer interests

Dataset may contains Different data.

### Example:
| Name        | Email             | State         | Interests              |
|-------------|-------------------|---------------|------------------------|
| John Doe    | john@example.com  | Maharashtra   | gadgets, electronics  |
| Jane Smith  | jane@example.com  | Tamil Nadu    | clothing, fashion     |

## How It Works
1. **Upload the Dataset**:
   - The customer data is saved on the server as `customer_data.csv`.

2. **Product Matching**:
   - The system calculates the similarity between the product name and customers' interests using cosine similarity.

3. **Email Notification**:
   - Sends an email to matched customers using their state-specific greeting. The email can be created and sent via Gemini for enhanced functionality.

## Language Translations
The application supports the following state-specific greetings:
- Maharashtra: "Hello"
- Tamil Nadu: "Vanakkam"
- Kerala: "Namaskaram"
- Karnataka: "Namaskara"

## Future Improvements
- Add more state-specific language support.
- Improve the matching algorithm for better accuracy.
- Add a frontend for easier interaction.

## License
This project is open-source and available under the MIT License.




