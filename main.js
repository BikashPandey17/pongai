var mainApp = {};

(function(){
    var firebase = app_firebase;
    var uid = null;
    var email = null;
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
          // User is signed in.
          uid = user.uid;
          email = user.email;
          console.log(uid);
        }else{
            uid=null;
            window.location.replace('index.html');
        }
      });  
      function logOut(){
        firebase.auth().signOut();
        window.location.replace('index.html');
      
      }
      
      function messageHandler(err){
        if(!!err){
          console.log(err);
        }else{
          console.log('success');
        }
      }
      function fnCreate(){
        var database = firebase.database();
        var ref = database.ref('players/'+uid);
        var data = {
            name : email,
            player_score : ball.score_player,
            ai_score : ball.score_ai
        }
        ref.set(data);
      }

      function uploadData(){
        
        var file = filejson;
        var storageRef = firebase.storage().ref();

        
        var metadata = {
          contentType: 'text/json'
        };

        // var uploadTask = storageRef.child('train_data/' + file.name).put(file, metadata);
        var uploadTask = storageRef.child('train_data/' + (new Date())).put(file, metadata);
       
        uploadTask.on(firebase.storage.TaskEvent.STATE_CHANGED, // or 'state_changed'
          function(snapshot) {
            // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
            var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            console.log('Upload is ' + progress + '% done');
            switch (snapshot.state) {
              case firebase.storage.TaskState.PAUSED: // or 'paused'
                console.log('Upload is paused');
                break;
              case firebase.storage.TaskState.RUNNING: // or 'running'
                console.log('Upload is running');
                break;
            }
          }, function(error) {

          
          switch (error.code) {
            case 'storage/unauthorized':
              // User doesn't have permission to access the object
              break;
            case 'storage/canceled':
              // User canceled the upload
              break;
            case 'storage/unknown':
              // Unknown error occurred, inspect error.serverResponse
              break;
          }
        }, function() {
          // Upload completed successfully, now we can get the download URL
          uploadTask.snapshot.ref.getDownloadURL().then(function(downloadURL) {
            console.log('File available at', downloadURL);
          });
        });

      }
      mainApp.logOut = logOut;
      mainApp.fnCreate = fnCreate;
      mainApp.uploadData = uploadData;
})()
