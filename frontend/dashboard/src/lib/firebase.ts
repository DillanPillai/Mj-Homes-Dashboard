// src/lib/firebase.ts
import { initializeApp, getApps } from "firebase/app";
import { getAuth } from "firebase/auth";

const cfg = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
};

// Helpful checks:
["VITE_FIREBASE_API_KEY","VITE_FIREBASE_AUTH_DOMAIN","VITE_FIREBASE_PROJECT_ID",
 "VITE_FIREBASE_STORAGE_BUCKET","VITE_FIREBASE_MESSAGING_SENDER_ID","VITE_FIREBASE_APP_ID"
].forEach(k => {
  if (!import.meta.env[k as keyof ImportMetaEnv]) {
    console.warn(`[env] Missing ${k}`);
  }
});

console.log("[firebase] projectId =", cfg.projectId);
// after your config object
console.log("[firebase] projectId =", import.meta.env.VITE_FIREBASE_PROJECT_ID);

// Optional: expose a safe peek so you can check from the console without using import.meta
// (remove later)
;(window as any).__VITE = {
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  hasApiKey: !!import.meta.env.VITE_FIREBASE_API_KEY,
};



const app = getApps().length ? getApps()[0] : initializeApp(cfg);
export const auth = getAuth(app);
