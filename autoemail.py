import csv
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import params
except ImportError:
    print("Please create params.py based on params_default.py first.")
    sys.exit(1)


def parse_csv_to_dict(file_path, required_columns):
    """Parses a CSV file and returns a list of dictionaries representing each row."""
    data = []

    with open(file_path, mode='r', encoding=params.csv_encoding) as file:
        # Uses the first row as column names
        reader = csv.DictReader(
            file, delimiter=params.csv_delimiter, quotechar=params.csv_quotechar)

        # Validate required columns
        missing_columns = required_columns - set(reader.fieldnames)
        if missing_columns:
            print(
                f"Error: Missing required columns: {', '.join(missing_columns)}")
            sys.exit(1)

        for row in reader:
            # Convert each row to a dictionary and add to the list
            data.append(dict(row))

    return data


def format_body(template, row_data):
    """Formats the 'body' column using the other row values."""
    try:
        return template.format(**row_data)
    except KeyError as e:
        missing_key = str(e).strip("'")
        print(
            f"Warning: Missing placeholder '{missing_key}' in row {row_data}. Leaving it unchanged.")
        return template


def generate_email_preview(row):
    """Generates an email preview from a row dictionary."""
    email_preview = {
        "From": row["from"],
        "To": row["to"],
        "Subject": row["subject"],
        "CC": row.get("cc", ""),  # Optional
        "BCC": row.get("bcc", ""),  # Optional
        "Reply-To": row.get("reply-to", ""),  # Optional
        "Body": format_body(row["body"], row)  # Format body column
    }
    return email_preview


def send_email(email_data):
    """Sends an email using SMTP server settings from params.py."""
    msg = MIMEMultipart()
    msg["From"] = email_data["From"]
    msg["To"] = email_data["To"]
    msg["Subject"] = email_data["Subject"]

    if email_data["CC"]:
        msg["Cc"] = email_data["CC"]

    if email_data["Reply-To"]:
        msg["Reply-To"] = email_data["Reply-To"]

    msg.attach(MIMEText(email_data["Body"], "plain"))

    recipients = [email_data["To"]]
    if email_data["CC"]:
        recipients.append(email_data["CC"])
    if email_data["BCC"]:
        recipients.append(email_data["BCC"])

    try:
        with smtplib.SMTP(params.smtp_server, params.smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(params.smtp_username, params.smtp_password)
            server.sendmail(email_data["From"], recipients, msg.as_string())
            print(f"✅ Email sent to: {email_data['To']}")
    except Exception as e:
        print(f"❌ Failed to send email to {email_data['To']}: {e}")


def main():
    """Main function to handle command-line arguments and send emails."""
    csv_file_path = params.csv_file

    if not os.path.isfile(csv_file_path):
        print(f"Error: File '{csv_file_path}' does not exist.")
        sys.exit(1)

    try:
        required_columns = {"from", "to", "subject", "body"}
        parsed_data = parse_csv_to_dict(csv_file_path, required_columns)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        sys.exit(1)

    email_previews = []
    for row in parsed_data:
        email_preview = generate_email_preview(row)
        email_previews.append(email_preview)
        print("\n--- Email Preview ---")
        for key, value in email_preview.items():
            if value == "":
                continue
            space = "\n" if key == "Body" else " "
            print(f"{key}:{space}{value}")
        print("----------------------")

    confirmation = input("Send all emails? (y/n): ").strip().lower()
    if confirmation == "y":
        for email_preview in email_previews:
            send_email(email_preview)
    else:
        print("❌ All emails were skipped.")


if __name__ == "__main__":
    main()
