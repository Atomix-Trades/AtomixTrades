<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Signup Form</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="css/loader.css" />
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", "sans-serif";
}
body {
  position: relative;
  background-color: #333;
  background: #333;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
::selection {
  color: #ececec;
  background: #333;
}
.form {
  position: relative;
  background: #f2f3f7;
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: -3px 3px 10px -5px rgba(0, 0, 0, 0.2);
  padding: 30px 30px;
  
}
.form h2 {
  font-size: 30px;
  font-weight: 700;
}
.form p {
  font-size: 14px;
  padding-bottom: 8px;
}
.form form .profile-img {
  margin: 18px 30px;
  position: absolute;
  top: 0;
  right: 0;
  width: 75px;
  height: 75px;
  background: #f2f3f7;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/768px-Circle-icons-profile.svg.png");
  border-radius: 50%;
  border: 4px solid #006692;
}
.file-upload {
  position: absolute;
  top: 0;
  right: -15px;
  height: 35px;
  width: 35px;
  display: flex;
  border-radius: 50%;
  border: 2px solid #d2d3d7;
  overflow: hidden;
  background-image: linear-gradient(to bottom, #006692, #f2f3f7 50%);
  background-size: 100% 200%;
  transition: all 1s;
  font-size: 14px;
  cursor: pointer;
}
.form input[type="file"] {
  position: relative;
  height: 40px;
  width: 40px;
  padding: 20px;
  opacity: 0;
  cursor: pointer;
}
.form i {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  color: #333;
  z-index: 100;
  pointer-events: none;
  cursor: pointer;
}
.file-upload:hover {
  background-position: 0 100%;
}
.file-upload:hover i {
  color: #2983aa;
}
.form form {
  margin: 8px 0;
}
.form form .error-text {
  display: none;
  color: #851923;
  padding: 4px 6px;
  text-align: center;
  border-radius: 4px;
  background: #ffe3e5;
  border: 1px solid #dfa5ab;
  margin-bottom: 8px;
}
.form .grid-details {
  display: flex;
}
.form .grid-details .input:first-child {
  margin-right: 8px;
  width: 100%;
}
.form .grid-details .input:last-child {
  margin-left: 8px;
  width: 100%;
}
.form form .input {
  display: flex;
  margin-bottom: 6px;
  flex-direction: column;
}
.form form .input input {
  height: 40px;
  width: 100%;
  font-size: 14px;
  padding: 0 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}
.form form .input input:focus,
.form form .input input:valid {
  border: 2px solid #00b3ff;
  transition: 0.1s ease;
  outline: none;
}
.form form input.button {
  height: 45px;
  border: none;
  color: #f2f3f7;
  width: 100%;
  font-size: 17px;
  background: #006692;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 13px;
  border: 2px solid #2983aa;
}

.form .link {
  text-align: center;
  margin: 10px 0;
  font-size: 17px;
}
.form .link a {
  color: #006692;
}
.form .link a:hover {
  text-decoration: underline;
}


  </style>
  </head>
  <body>

  <!-- loader -->

  <div id="loader">
  <div class="loader row-item">
	<span class="circle"></span>
	<span class="circle"></span>
	<span class="circle"></span>
	<span class="circle"></span>
	<span class="circle"></span>
</div>
</div>

  <!-- loader end -->

  <!-- form start -->
    <div class="form">
      <h2>Signup Form</h2>
      <p>It's free and always will be.</p>
      <form action="" enctype="multipart/form-data" autocomplete="off">
        <div class="error-text">Error</div>
      <div class="grid-details">
        <div class="input">
            <label>First Name</label>
            <input type="text" name="fname" placeholder="First Name" required pattern="[a-zA-Z'-'\s]*" >
        </div>
        <div class="input">
            <label>Last Name</label>
            <input type="text" name="lname" placeholder="Last Name" required pattern="[a-zA-Z'-'\s]*">
        </div>
      </div>
      <div class="input">
        <label>Email</label>
        <input type="email" name="email" placeholder="Enter Your Email" required>
    </div>
      <div class="input">
        <label>Phone</label>
        <input type="phone" name="phone" placeholder="Phone Number" >
    <div class="grid-details">
        <div class="input">
            <label>Password</label>
            <input type="password" name="pass" placeholder="Password" required>
        </div>
        <div class="input">
            <label>Confirm Password</label>
            <input type="password" name="cpass" placeholder="Confirm Password" required>
        </div>
      </div>
      <div class="profile-img">
        <div class="file-upload">
            <input name="image" id="image-preview" type="file" class="file-input"  required oninvalid="this.setCustomValidity('Select an Profile Image')"oninput="this.setCustomValidity('')"/>
            <i class="fas fa-user-edit"></i>
        </div>
        </div>
        <div class="submit">
      <input type="submit" value="Signup Now" class="button">
    </div>
    </form>
    <div class="link">Already signed up? <a href="login.php">Login now</a></div>
    </div>

  <!-- form end -->


<script>
    $(document).ready(function() {
    //Preloader
    preloaderFadeOutTime = 1200;
    function hidePreloader() {
    var preloader = $('#loader');
    preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
    });
    </script>

  <script>const form = document.querySelector('.form form'),
submitbtn = form.querySelector('.submit input'),
errortxt = form.querySelector('.error-text');

form.onsubmit = (e) =>{
    e.preventDefault();            //stops the default action

}      
 

submitbtn.onclick = () =>{
    // start ajax

    let xhr = new XMLHttpRequest(); // create xml object
    xhr.open("POST","./php/signup.php",true);
    xhr.onload = () =>{

        if(xhr.readyState === XMLHttpRequest.DONE){
            if(xhr.status === 200){
                let data = xhr.response;
                        if(data == "success"){
                        location.href = "./verify.php";
                        }
                    else{
                        errortxt.textContent = data;
                        errortxt.style.display = "block";
                    }

            }
        }

    }
    // send data through ajax to php
    let formData = new FormData(form); //creating new object from form data
    xhr.send(formData);  //sending data to php

}

</script>
  </body>
</html>
