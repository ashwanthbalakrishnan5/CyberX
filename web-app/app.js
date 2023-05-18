const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const ejs = require("ejs");

const app = express();
app.set("view engine", "ejs");

app.use(bodyParser.json());
app.use(express.static("public"));

let call_type = [],
  durations = [],
  date = [],
  time = [];

let uniqueContacts = [];
let uniquephNums = [];
app.get("/", (req, res) => {
  res.render("mainDashBoard");
});

app.get("/adb", (req, res) => {
  res.render("contacts");
});

app.get("/dashboard", (req, res) => {
  res.render("secondaryDashBoard");
});

app.get("/calllogs", (req, res) => {
  request(
    "http://127.0.0.1:8000/api/CallLog/?start_date=&end_date=&is_known=true&is_international=false&call_type=",
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var callLogs = JSON.parse(body);
        let phNums = [],
          names = [];
        for (let i = 0; i < callLogs.length; i++) {
          phNums.push(callLogs[i]["number"]);
          names.push(callLogs[i]["contacts"]["name"]);
        }
        uniqueContacts = names.filter((value, index, self) => {
          return self.indexOf(value) == index;
        });
        uniquephNums = phNums.filter((value, index, self) => {
          return self.indexOf(value) == index;
        });
      }
    }
  );

  res.render("calllogs", {
    names: uniqueContacts,
    phnos: uniquephNums,
    call_type: call_type,
    durations: durations,
    date: date,
    time: time,
  });
});

app.get("/calllogs/:phno", (req, res) => {
  request(
    "http://127.0.0.1:8000/api/CallLog/?number=" + req.params.phno,
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        call_type = [];
        durations = [];
        date = [];
        time = [];
        let details = JSON.parse(body);
        for (let i = 0; i < details.length; i++) {
          call_type.push(details[i]["call_type"]);
          durations.push(details[i]["duration"] + "s");
          var datetime = details[i]["datetime"].split("T");

          const string_after_splitting = datetime[0].split("-");
          datetime[0] = string_after_splitting.join("/");

          date.push(datetime[0]);
          datetime[1] = datetime[1].substring(0, datetime[1].length - 1);

          time.push(datetime[1]);
        }
      }
    }
  );

  res.render("calllogs", {
    names: uniqueContacts,
    phnos: uniquephNums,
    call_type: call_type,
    durations: durations,
    date: date,
    time: time,
  });
});

app.get("/contacts", (req, res) => {
  request(
    "http://127.0.0.1:8000/api/Contacts",
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var contacts = JSON.parse(body)
        console.log(contacts)
        let contactName = [], contactNumber = []
        for(let i=0; i<contacts.length; i++) {
            contactName.push(contacts[i]['name'])
            contactNumber.push(contacts[i]['number'])
        }
        res.render("contacts", {names: contactName, phnos: contactNumber})
      }
    }
  );
});

app.get("/sms", (req, res) => {
  res.render("sms");
});

app.get("/files", (req, res) => {
  res.render("fileDashBoard");
});

app.get("/files/videos", (req, res) => {
  res.render("videos");
});

app.get("/files/documents", (req, res) => {
  res.render("documents");
});

app.get("/files/photos", (req, res) => {
  res.render("photos");
});

app.listen(3000, () => {
  console.log("listening to port : 3000");
});
