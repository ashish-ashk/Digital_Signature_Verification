Digital Signature Verification System

This project is a Digital Signature Verification System built with Django and ECDSA. It allows users to generate key pairs, sign messages and documents, and verify digital signatures with a user-friendly web interface.
________________________________________
Prerequisites
•	Python 3.8+
•	VS Code
•	pip (Python package manager)
•	Git (optional, for cloning)
•	(Recommended) Virtual environment tool: venv or virtualenv
________________________________________
Open the VS Code and run the following commands step by step in terminal:-
1. Clone the Repository
git clone https://github.com/ashish-ashk/Digital_Signature_Verification
cd Digital_Signature_Verification
________________________________________
2. Install Dependencies
pip install -r requirements.txt
________________________________________
3. Apply Database Migrations
python manage.py migrate
________________________________________
4. (Optional) Create a Superuser for Django Admin
python manage.py createsuperuser
________________________________________
5. Run the Development Server
python manage.py runserver
________________________________________
6. Access the Application
Open your browser and go to:
http://127.0.0.1:8000/digital_signatures/user/
________________________________________
7. Using the Application
Generate Key Pair
•	Click Generate Key Pair to create a new ECDSA key pair.
•	Copy/save the private and public keys as needed.
Sign a Message
•	Enter your private key and the message you want to sign.
•	Click Sign Message to generate the signature.
Sign a Document
•	Select the file type (Image or Document).
•	Upload your file (JPG, JPEG, PNG).
•	Enter your private key and message.
•	Click Sign Document to sign and download the signed file.
Verify a Signature
•	Use the verification section to upload a signed document or enter signature details.
•	The system will display verification results and extracted message details.
Forge Document (For Demo/Testing)
•	Use the Forge Sign Document button to open the forge editor.
•	Edit the signature data and confirm to generate a forged signed file.
________________________________________
8. Django Admin (Optional)
•	Visit http://127.0.0.1:8000/admin/ and log in with your superuser credentials to manage keys, logs, and users.
________________________________________
9. Notes
•	The project uses ECDSA (secp256k1) for digital signatures.
•	Watermarks and geolocation features are available for signed documents.
•	All cryptographic operations are handled securely on the backend.
________________________________________
Troubleshooting
•	If you encounter missing dependencies, re-run pip install -r requirements.txt.
•	For database issues, try python [manage.py](http://_vscodecontentref_/1) makemigrations then python [manage.py](http://_vscodecontentref_/2) migrate.
•	If static files are not loading, run python [manage.py](http://_vscodecontentref_/3) collectstatic.
________________________________________
License
This project is for educational and demonstration purposes.
________________________________________
Enjoy using your Digital Signature Verification System!


