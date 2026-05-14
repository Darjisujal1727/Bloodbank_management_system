// Example: Write data to Firebase Realtime Database
import { database } from './firebaseInit.js';
import { ref, set, push, onValue } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-database.js";

// Write user data
function writeUserData(userId, name, email) {
    set(ref(database, 'users/' + userId), {
        username: name,
        email: email
    });
}

// Read user data (real-time listener)
function listenUserData(userId, callback) {
    const userRef = ref(database, 'users/' + userId);
    onValue(userRef, (snapshot) => {
        const data = snapshot.val();
        callback(data);
    });
}

export { writeUserData, listenUserData };
