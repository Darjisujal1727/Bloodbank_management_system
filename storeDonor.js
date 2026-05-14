// Example: Store donor data in Firestore from a web form
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCjBL9hOXsyrncbQuRQiwnjjRAd2BJpN1s",
  authDomain: "bbms-fa959.firebaseapp.com",
  databaseURL: "https://bbms-fa959-default-rtdb.firebaseio.com",
  projectId: "bbms-fa959",
  storageBucket: "bbms-fa959.firebasestorage.app",
  messagingSenderId: "818136261245",
  appId: "1:818136261245:web:e0395f0ab2eca2ad880714",
  measurementId: "G-BT275HF7N6"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Call this function with donor data to store in Firestore
document.getElementById('donorForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const donorData = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    blood_group: document.getElementById('blood_group').value,
    contact: document.getElementById('contact').value,
    address: document.getElementById('address').value,
    next_eligibility: document.getElementById('next_eligibility').value,
    status: document.getElementById('status').value
  };
  await addDoc(collection(db, 'donors'), donorData);
  alert('Donor data saved!');
});
