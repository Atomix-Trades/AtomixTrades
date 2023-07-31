<?php 
  session_start();
  include 'db.php';
  $unique_id = $_SESSION['unique_id'];
  if(empty($unique_id))
  {
      header ("Location: log.php");
  } 
  $qry = mysqli_query($conn, "SELECT * FROM users WHERE unique_id = '{$unique_id}'");
  if(mysqli_num_rows($qry) > 0){
    $row = mysqli_fetch_assoc($qry);
    if($row){
      $_SESSION['verification_status'] = $row['verification_status'];
      if($row['verification_status'] == 'Verified')
      {
        header ("Location: index.php");
      } 
  }
  }
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Verify Account-Auto Aplha</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <!-- <link rel="stylesheet" href="css/form.css"> -->
  <style>
    /* verify account style start */
    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", "sans-serif";
}
body {
  position: relative;
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
  /* background-image: url('../Images/1.jpg'); */
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
  background: #333;
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


.fields_input {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 15px 0;
}
.otp_field {
  border-radius: 5px;
  font-size: 60px;
  height: 100px;
  width: 100px;
  border: 3px solid #cacaca;
  margin: 1%;
  text-align: center;
  font-weight: 600;
  outline: none;
}
.otp_field::-webkit-inner-spin-button,
.otp_field::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.otp_field:valid {
  border-color: #3095d8;
  box-shadow: 0 10px 10px -5px rgba(0, 0, 0, 0.25);
}
/* .form form input.resend_btn {
  float: right;
  border: none;
  background: #f2f3f7;
  color: #006692;
  padding: 8px;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  border: 2px solid #2983aa;
} */

@media only screen and (max-width: 455px) {
  .otp_field {
    font-size: 55px;
    height: 80px;
    width: 80px;
  }
}


  </style>
  </head>
  <body>
    <div class="form" style="text-align: center;">
      <h2>Verify Your Account</h2>
      <p>We emailed you the four digit otp code to Enter the code below to confirm your email address.</p>
      <form action=""autocomplete="off">
        <div class="error-text">Error</div>
          <div class="fields_input">
            <input type="number" name="otp1" class="otp_field" placeholder="0" min="0" max="9" required onpaste="return false">
            <input type="number" name="otp2" class="otp_field" placeholder="0" min="0" max="9" required onpaste="return false">
            <input type="number" name="otp3" class="otp_field" placeholder="0" min="0" max="9" required onpaste="return false">
            <input type="number" name="otp4" class="otp_field" placeholder="0" min="0" max="9" required onpaste="return false">
        </div>
        <div class="submit">
        <!-- <input type="button" name="resend" class="resend_btn" value="Resend Again"> -->
      <input type="submit" value="Verify Now" class="button">
    </div>
    </form>
    </div>
<script>const otp = document.querySelectorAll('.otp_field');

// Initially focus first input
otp[0].focus();

otp.forEach((field, index) => {
	field.addEventListener('keydown', (e) => {
		if(e.key >= 0 && e.key <= 9) {
            otp[index].value = "";
			setTimeout(() => {
				otp[index+1].focus();
			}, 4);
		} else if (e.key === 'Backspace') {
			setTimeout(() => {
				otp[index-1].focus();
			}, 4);
		}
	});
});


const form = document.querySelector('.form form'),
submitbtn = form.querySelector('.submit .button'),
errortxt = form.querySelector('.error-text');


form.onsubmit = (e) =>{
    e.preventDefault();         //stops the default action
}
submitbtn.onclick = () =>{
    // start ajax

    let xhr = new XMLHttpRequest(); //create xml object
    xhr.open("POST","otp.php",true);
    xhr.onload = () =>{
        if(xhr.readyState == XMLHttpRequest.DONE){
            if(xhr.status == 200){
                let data = xhr.response;
                if(data == "success"){
                    location.href = "../../templates/price1.html";
                }
                else{
                    errortxt.textContent = data;
                    errortxt.style.display = "block";
                }
            }
        }
    }
    let formData = new FormData(form);
    xhr.send(formData);
}</script>
  </body>
</html>
