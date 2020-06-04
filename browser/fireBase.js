var app_firebase = {};

(function(){
    // Initialize Firebase
    var config = {
        apiKey: "AIzaSyD-YkuZamopwNX_581fFobGefywR-LiOc8",
        authDomain: "pongai-d6660.firebaseapp.com",
        databaseURL: "https://pongai-d6660.firebaseio.com",
        projectId: "pongai-d6660",
        storageBucket: "pongai-d6660.appspot.com",
        messagingSenderId: "1051076549691"
    };
    firebase.initializeApp(config);
    console.log(firebase);
    app_firebase = firebase;

})()