# Welcome to your project

## Project info

## How can I edit this code?

There are several ways to edit your application.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

# Follow these steps:

# Follow this link:
https://docs.google.com/document/d/1xEVb7UzcwDebs0dvD-32FPjdkqJnDXUPjX5GE6Z7PPA/edit?tab=t.0

Copy the local files in the root, frontend and backend folder before following the steps in the document or below:

## Frontend Setup

# 1. Create a .env.local file in the frontend folder with the below code:
VITE_FIREBASE_API_KEY=AIzaSyB3n-Gu1Wf1q4bziuvwmG1CSx38lUPdgR8
VITE_FIREBASE_AUTH_DOMAIN=mj-home-dashboard.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mj-home-dashboard
VITE_FIREBASE_STORAGE_BUCKET=mj-home-dashboard.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=74941228201
VITE_FIREBASE_APP_ID=1:74941228201:web:087f66e9e57988eb5c35b8
VITE_FIREBASE_MEASUREMENT_ID=G-M3WHD6DNS8

# 2. Create a .env.local file in the frontend/dashboard folder with the below code:
VITE_FIREBASE_API_KEY=AIzaSyB3n-Gu1Wf1q4bziuvwmG1CSx38lUPdgR8
VITE_FIREBASE_AUTH_DOMAIN=mj-home-dashboard.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mj-home-dashboard
VITE_FIREBASE_STORAGE_BUCKET=mj-home-dashboard.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=74941228201
VITE_FIREBASE_APP_ID=1:74941228201:web:087f66e9e57988eb5c35b8
VITE_FIREBASE_MEASUREMENT_ID=G-M3WHD6DNS8

# 3. Navigate to the frontend folder
cd frontend

# 4. Navigate to the dashboard folder
cd dashboard

# 5. Install dependencies one at a time
npm install 

# 6. Start the frontend server
npm run dev



# NOTE: Input the above if you’re entering the frontend for the first time. After that, you can enter without it as many times as you wish later, as shown below: 

# 1. Navigate to the frontend folder
cd frontend

# 2. Navigate to the frontend/dashboard folder
cd dashboard

# 4. Start the FastAPI server
npm run dev

# 5. Login details for the frontend
Email Address: testing@testing.com
Password: 123456