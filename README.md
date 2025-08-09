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

![Login Page](docs/screenshots/homepage.png)
*Home Page*

![Dashboard](docs/screenshots/user_dashboard.png)
*User dashboard*

## Running Locally Without Docker
Prerequisites
- Python 3.10+
- MySQL Server installed and running
- pip and virtualenv

 Steps

 **1. Clone the repository:**
   ```bash
   git clone https://github.com/abhay41/Brain_Tumor_Detection_App.git
   cd Brain_Tumor_Detection_App
```
**2. Create & activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```
**4. Setup MySQL database:**
- Create a database named **brain_tumor_db.**
- Run SQL scripts inside **mysql-init/** to create tables and seed data.
  
**5. Configure .env file with your MySQL credentials and Flask settings.**

**6. Run the app**
```bash
run.py
```
**7. Open browser at** http://localhost:5000

## Running with Docker
Prerequisites
- Docker Engine installed
- Docker Compose installed
- (Optional) Docker Hub account

**Steps**
**Option 1: Build and run locally**
```bash
docker-compose build
docker-compose up -d
```
**Option 2: Pull prebuilt images and run**
```bash
docker-compose pull
docker-compose up -d
```
**Access the app**

Open http://localhost:5000 in your browser.

**Docker Compose Services**
- mysql: MySQL 8.0 container with persistent volume and initialization scripts.
- web: Flask app served by Gunicorn, connected to MySQL.

**Environment Variables (.env)**
```bash
FLASK_ENV=production
DATABASE_URI=mysql+pymysql://root:root_admin123@mysql:3306/brain_tumor_db
SECRET_KEY=some_secret_key
```
**Volumes & Persistence**
- Upload folders (app/static/uploads) are mounted as volumes for persistent file storage.
- MySQL data is persisted via Docker volumes to avoid data loss on container restarts.

**How to Access the MySQL Database in Docker Container**
**Step 1: List running containers**
```bash
docker ps
```
**Step 2: Access MySQL container shell**
```bash
docker exec -it brain_tumor_mysql bash
```
**Step 3: Log into MySQL**
```bash
mysql -u root -p
```
*Enter your MySQL root password when prompted*

**Step 4: Switch to application database**
```bash
USE brain_tumor_db;
```
**Step 5: View tables and data**
```bash
SHOW TABLES;
SELECT * FROM user LIMIT 10;
```
**Step 6: Exit**
```bash
exit;    -- Exit MySQL shell
exit     -- Exit container shell

```
**Optional: Connect from host (if port 3306 exposed)**
```bash
mysql -h 127.0.0.1 -P 3306 -u root -p
```
**Contributions**

Feel free to open issues or pull requests.




