# MeetSmart 🚀

## Prerequisites ✅
Before running the application, ensure you have the following installed:
- 📌 [Node.js](https://nodejs.org/)
- 🐍 [Python 3](https://www.python.org/)
- 📦 [pip](https://pip.pypa.io/en/stable/)
- 🌐 [virtualenv](https://virtualenv.pypa.io/en/latest/) (for backend environment management)
- 🎬 [ffmpeg](https://ffmpeg.org/download.html)

## Installation and Setup ⚙️

### 1. Clone the repository 📂
```sh
git clone https://github.com/yourusername/MeetSmart.git
cd MeetSmart
```

### 2. Setting up environment variables 🔑
Create a `.env` file in the `./backend` folder with the necessary API keys and configurations:

```
LLAMACLOUD_KEY="your_api_key_from_llamacloud.com"

GROQ_API_KEY="your_api_key_from_groqcloud.com"

EMAIL_PASSWORD="your_email_password_from_google_smtp_server"
EMAIL_ADDRESS="your_email_address_from_google_smtp_server"
```

## Running the Application ▶️

### 1. Start the Backend (Python) 🖥️
```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 2. Start the Frontend (React) 🌍
```sh
cd ../MeetSmart
npm install
npm run dev
```
The frontend will now be running at `http://localhost:5173` 🎉

---

# Running the Application in Docker 🐳
### Prerequisites 🛠️
Before running the application, ensure you have the following installed:
- 🏗️ [Docker](https://www.docker.com/products/docker-desktop/)

## Installation and Running the Application 🚀
### 1. Clone the repository 📥
```sh
git clone https://github.com/yourusername/MeetSmart.git
cd MeetSmart
```
### 2. Setting up environment variables 🔐
Create a `.env` file in the `./backend` folder with the necessary API keys and configurations:

```
LLAMACLOUD_KEY="your_api_key_from_llamacloud.com"

GROQ_API_KEY="your_api_key_from_groqcloud.com"

EMAIL_PASSWORD="your_email_password_from_google_smtp_server"
EMAIL_ADDRESS="your_email_address_from_google_smtp_server"
```

### 3. Run the Docker Compose command 🏃‍♂️
#### (It will take around 10 minutes to build ⏳)

```sh
MeetSmart/ docker compose up --build -d
```
The frontend will now be running at `http://localhost:3000` 🎊

