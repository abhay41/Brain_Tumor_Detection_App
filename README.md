# Brain Tumor Prediction App

A web-based AI application that leverages deep learning to analyze brain MRI scans and detect tumors. Designed for doctors and patients, this system provides accurate classifications, confidence scores, and treatment suggestions to aid diagnosis and medical decision-making.

---

## 🚀 Features

- **Deep Learning-Based Detection:** Classifies MRI scans into Glioma, Meningioma, Pituitary Tumor, or No Tumor using a trained model.
- **Prediction Confidence:** Shows percentage confidence for predictions.
- **Treatment Suggestions:** Recommends medical treatments and follow-ups.
- **User Authentication:** Secure login and session management for doctors and patients.
- **Patient Management:** Dashboard to manage and view patient history.
- **Data Visualizations:** Displays statistical insights with charts and graphs.

---

## 🧠 Technologies Used

- **Frontend:** HTML, CSS, JavaScript (Jinja Templates)
- **Backend:** Flask (Python)
- **Database:** MySQL
- **Machine Learning:** TensorFlow, Keras
- **Deployment:** Docker + Flask
- **Containerization:** Docker Compose
- **Email Notifications:** Gmail SMTP with App Passwords

## Future Work
- Automate the ML pipeline (training → deployment) with CI/CD workflows.
- Add Kubernetes orchestration for scalability and high availability.
- Improve security with secret management and role-based access.
- Implement monitoring and alerting with Prometheus and Grafana.

## Project Structure

- **app/**— Flask app source code (routes, models, templates)
- **model/**— ML model files
- **mysql-init/**— Initial SQL scripts for database setup and seeding
- **.env**— Environment variables for configuration
- **Dockerfile**— Multi-stage Dockerfile for building the Flask app
- **docker-compose.yml**— Compose file to run MySQL and Flask services together

---

## Screenshots

![Login Page](docs/screenshots/login.png)
*Login page*

![Dashboard](docs/screenshots/dashboard.png)
*User dashboard displaying patient data*


 **Clone the repository:**
   ```bash
   git clone https://github.com/abhay41/Brain_Tumor_Detection_App.git
   cd Brain_Tumor_Detection_App


