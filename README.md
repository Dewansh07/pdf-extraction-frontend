
# PDF Extraction Application

This is a full-stack application for extracting specific details such as **Name**, **Phone**, and **Address** from PDF files. The application consists of a React-based frontend and a Flask-based backend.

---

## Features

- Upload PDF files via the frontend.
- Automatically extracts relevant details using NLP (Natural Language Processing) in the backend.
- Secure communication between the frontend and backend with CORS support.
- Minimalistic design for easy use.

---

## Tech Stack

### Frontend
- **React 18.2.0**
- **Axios 1.7.9** for API communication.

### Backend
- **Flask 2.3.2** for building the API.
- **Flask-CORS 3.0.10** for enabling cross-origin resource sharing.
- **pdfplumber 0.10.0** for text extraction from PDF files.
- **spaCy 3.6.1** for NLP processing.

---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- **Node.js** (for frontend development)
- **Python 3.9** or above (for backend development)

---

### Setup Instructions

#### Backend Setup

1. Navigate to the `Backend` folder:
   ```bash
   cd Backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```
   By default, the server runs on `http://localhost:5050`.

---

#### Frontend Setup

1. Navigate to the root of the project:
   ```bash
   cd ..
   ```

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```
   The app runs on `http://localhost:3000`.

---

## How to Use

1. **Start the Backend**: Ensure the Flask server is running.
2. **Start the Frontend**: Launch the React app.
3. **Upload a PDF**: Use the interface to upload the PDF files.
4. **View Results**: The extracted details will be displayed on the frontend.

---

## Folder Structure

```
Project
├── Backend
│   ├── app.py
│   ├── requirements.txt
│   └── ... (other backend files)
├── Frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── ... (other frontend files)
```

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add some feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or feedback, feel free to reach out via email: **[your-email@example.com]**.