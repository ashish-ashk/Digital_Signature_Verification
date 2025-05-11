# Digital Signature Verification System

This project is a **Digital Signature Verification System** developed using **Elliptic Curve Digital Signature Algorithm (ECDSA)**. It provides robust authentication for messages by allowing users to securely sign and verify the authenticity of data. The application is built with Django and uses **PostgreSQL** as its database for reliable data storage.

## Features

- **Generate Key Pair**: Allows users to generate a secure ECDSA key pair (Private Key, Public Key X, Public Key Y).
- **Message Signing and Verification**: Users can input messages, sign them with their private key, and verify authenticity using the generated signature.
- **User-Friendly Interface**: A clean and responsive UI for an enhanced user experience.
- **Enhanced Security**: Utilizes ECDSA to provide a high level of cryptographic security.
- **PostgreSQL Database**: Stores user data and keys securely in a robust, SQL-compliant database.

## Screenshots

| Generate Key Pair | Sign Message | Verify Signature |
|-------------------|--------------|------------------|
| ![Generate Key Pair](https://github.com/Pratham-verma/Digital_Signature_Verification/raw/master/assets/Generate_Key.jpg) | ![Sign Message](https://github.com/Pratham-verma/Digital_Signature_Verification/raw/master/assets/Sign_Message.jpg) | ![Verify Signature](https://github.com/Pratham-verma/Digital_Signature_Verification/raw/master/assets/Verify_Signature.jpg) |

## Technical Overview

- **Backend**: Django for handling request processing, key generation, signing, and verification.
- **Database**: PostgreSQL for secure, structured data storage.
- **Frontend**: HTML, CSS, and JavaScript for a responsive user interface.
- **Cryptography**: ECDSA, using private-public key pairs to ensure data integrity and non-repudiation.

## Usage

1. **Generate Key Pair**: Click on "Generate Key Pair" to create a private-public key pair. The generated keys are displayed on the screen.
2. **Sign Message**: Enter a message, use the private key to generate a unique signature, and obtain signature values (R, S).
3. **Verify Signature**: Input the original message, public key, and the signature values to validate the authenticity of the message.

## Future Improvements

1. **Document Authentication**: Extend functionality to include document signing and verification, ensuring integrity and authenticity of larger files.
2. **Timestamping Feature**: Integrate a timestamp to provide a verified time for each signature, improving non-repudiation.
3. **User Authentication and Access Control**: Add user registration, authentication, and role-based access control for secure multi-user operations.

---
