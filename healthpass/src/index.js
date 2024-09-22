import { createClient } from "@propelauth/javascript";

const authClient = createClient({
    // The base URL where your authentication pages are hosted. You can find this under the Frontend Integration section for your project.
    authUrl: "https://96933199.propelauthtest.com",
    // If true, periodically refresh the access token in the background. This helps ensure you always have a valid token ready to go. Default true.
    enableBackgroundTokenRefresh: true
});

var userid = ""

function displayprofile(userid) {
  fetch("http://127.0.0.1:5000/users?userid="+userid).then(response => response.json()).then(data => {
      console.log(data);
      document.getElementById("name").innerText = data['name'];
      document.getElementById("dob").innerText = data['dob'];
      document.getElementById("height").innerText = data['height'];
      document.getElementById("weight").innerText = data['weight'];
      document.getElementById("sex").innerText = data['sex'];
      document.getElementById("address").innerText = data['address'];
      document.getElementById("provider").innerText = data['insurance_provider'];
      document.getElementById("policy").innerText = data['insurance_policy_number'];
      document.getElementById("ssn").innerText = data['social_security_number'];
    })
}

function deletemedication() {
  let medid = this.id;
  fetch("http://127.0.0.1:5000/deletemedication?userid="+userid+"&medid="+medid).then(response => response.json()).then(data => {
    displaymedications();
  })
}

function displaymedications() {
  fetch("http://127.0.0.1:5000/users?userid="+userid).then(response => response.json()).then(data => {
    console.log(data);
    let arr = data['medications'];

    // Get the list container element
  let list =
  document.getElementById('medlist');

  // Create the unordered list element 
  //and set its inner HTML using map() and join()
  let ul = `<ul>${arr.map(item =>
  `<li>${item.medication_name}, ${item.dosage}, ${item.frequency}, ${item.duration}, ${item.intended_use}<button class = "delete" id = ${item.medication_id}>Delete</button></li>`).join('')}
        </ul>`;

  // Set the inner HTML of the list container
  list.innerHTML = ul;
  var elems = document.getElementsByClassName("delete");
  for (var i = 0; i < elems.length; i++) {
   elems.item(i).addEventListener('click', deletemedication);
  }
})
}


function addmedication() {
  const medname = document.getElementById('mednameinput').value;
  const use = document.getElementById('meduseinput').value;
  const dosage = document.getElementById('dosageinput').value;
  const frequency = document.getElementById('frequencyinput').value;
  const duration = document.getElementById('durationinput').value;
  fetch("http://127.0.0.1:5000/addmedication?userid="+userid+"&medname="+medname+"&use="+use+"&dosage="+dosage+"&frequency="+frequency+"&duration="+duration).then(response => response.json()).then(data => {
    console.log(data);
    displaymedications();
    document.getElementById("mednameinput").value = "";
      document.getElementById("meduseinput").value = "";
      document.getElementById("dosageinput").value = "";
      document.getElementById("frequencyinput").value = "";
      document.getElementById("durationinput").value = "";
  })
}


function updateprofile() {
  const name = document.getElementById('nameinput').value;
  const dob = document.getElementById('dobinput').value;
  const height = document.getElementById('heightinput').value;
  const weight = document.getElementById('weightinput').value;
  const sex = document.getElementById('sexinput').value;
  const address = document.getElementById('addressinput').value;
  const provider = document.getElementById('providerinput').value;
  const policy = document.getElementById('policyinput').value;
  const ssn = document.getElementById('ssninput').value;
  fetch("http://127.0.0.1:5000/updateuser?userid="+userid+"&name="+name+"&dob="+dob+"&height="+height+"&weight="+weight+"&sex="+sex+"&address="+address+"&provider="+provider+"&policy="+policy+"&ssn="+ssn).then(response => response.json()).then(data => {
      console.log(height);
      document.getElementById("name").innerText = data['user']['name'];
      document.getElementById("dob").innerText = data['user']['dob'];
      document.getElementById("height").innerText = data['user']['height'];
      document.getElementById("weight").innerText = data['user']['weight'];
      document.getElementById("sex").innerText = data['user']['sex'];
      document.getElementById("address").innerText = data['user']['address'];
      document.getElementById("provider").innerText = data['user']['insurance_provider'];
      document.getElementById("policy").innerText = data['user']['insurance_policy_number'];
      document.getElementById("ssn").innerText = data['user']['social_security_number'];

      document.getElementById("nameinput").value = "";
      document.getElementById("dobinput").value = "";
      document.getElementById("heightinput").value = "";
      document.getElementById("weightinput").value = "";
      document.getElementById("sexinput").value = "";
      document.getElementById("addressinput").value = "";
      document.getElementById("providerinput").value = "";
      document.getElementById("policyinput").value = "";
      document.getElementById("ssninput").value = "";
    })
}

const authInfo = await authClient.getAuthenticationInfoOrNull()
if (authInfo) {
    userid = authInfo.user.userId;
    console.log("User is logged in as", authInfo.user.userId);
    document.getElementById("display-when-logged-in").style.display = "revert";
    document.getElementById("display-when-logged-out").style.display = "none";

    displayprofile(authInfo.user.userId);
    document.getElementById("updateprofile").onclick = updateprofile;
    document.getElementById("addmed").onclick = addmedication;
    displaymedications();
    
        // Get authentication info and set email to it
        authClient.getAuthenticationInfoOrNull()
            .then(authInfo => {
                document.getElementById("userid").innerText = authInfo?.user?.userId;
            });
} else {
    console.log("User is not logged in");
    document.getElementById("display-when-logged-in").style.display = "none";
    document.getElementById("display-when-logged-out").style.display = "revert";
}

// Hook up buttons to redirect to signup, login, etc
document.getElementById("signup").onclick = authClient.redirectToSignupPage;
document.getElementById("login").onclick = authClient.redirectToLoginPage;
document.getElementById("account").onclick = authClient.redirectToAccountPage;
document.getElementById("logout").onclick = authClient.logout;