const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const ejs = require("ejs");

const app = express();
app.set("view engine", "ejs");

app.use(bodyParser.json());
app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended: true}))

let call_type = [],
  durations = [],
  date = [],
  time = [];

let uniqueContacts = [];
let uniquephNums = [];

let addresses = [], truncatedMessages = []
let smsMessages = [], smsType = []

app.get("/", (req, res) => {
  res.render("mainDashBoard");
});

app.get("/adb", (req, res) => {
  res.render("adbWaitScreen");
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

app.post("/calllogsfilter", (req,res)=>{
  var data = req.body

  var is_known;

  if(data.calltype === 'first') {
    is_known = false
  }else if(data.calltype === 'business') {
    is_known = true
  } else {
    is_known = ''
  }

  var is_international;

  if(data['International-Number'] === 'on') {
    is_international = true;
  } else {
    is_international = false
  }

  var ordering;

  if(data.ascending === 'on') {
    ordering = 'duration'
  }
  if(data.descending === 'on') {
    ordering = '-duration'
  }

  var start_date = data.From;
  var end_date = data.To;
  var start_time;
  var end_time;
  if(data.from === '') {
    start_time = '00:00:00'
  } else {
    start_time = data.from+':00'
  }
  if(data.to === '') {
    end_time = '00:00:00'
  } else {
    end_time = data.to+':00'
  }
  
  let start_date_time = start_date + 'T' + start_time
  let end_date_time = end_date + 'T' + end_time
  let final_req;
  if(start_date === '' && end_date != ''){
    final_req = '?'+'end_date='+end_date_time+'&'+'is_known='+is_known+'&'+'is_international='+is_international+'&'+'ordering='+ordering
  }
  if(end_date === '' && start_date != ''){
    final_req = '?'+'start_date='+start_date_time+'&'+'is_known='+is_known+'&'+'is_international='+is_international+'&'+'ordering='+ordering
  }
  if(end_date === '' && start_date === '') {
    final_req = '?'+'is_known='+is_known+'&'+'is_international='+is_international+'&'+'ordering='+ordering

  }
  if(start_date != '' && end_date != '') {
    final_req = '?'+'start_date='+start_date_time+'&'+'end_date='+end_date_time+'&'+'is_known='+is_known+'&'+'is_international='+is_international+'&'+'ordering='+ordering
  }
  console.log(final_req)
  request(
    "http://127.0.0.1:8000/api/CallLog/"+final_req,
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var result = JSON.parse(body)
        console.log(result)

        let phNumsfilterd = [],
          namesfilterd = [];
        for (let i = 0; i < result.length; i++) {
          phNumsfilterd.push(result[i]["number"]);
          console.log(result[i]["contacts"])
          if(result[i]["contacts"] != null){
            namesfilterd.push(result[i]["contacts"]["name"]);
          }
        }

        res.render("calllogs", {
          names: namesfilterd,
          phnos: phNumsfilterd,
          call_type: call_type,
          durations: durations,
          date: date,
          time: time,
        });
      }
    }
  );
})

app.get("/contacts", (req, res) => {
  request(
    "http://127.0.0.1:8000/api/Contacts",
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var contacts = JSON.parse(body)
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
  request(
    "http://127.0.0.1:8000/api/SmsLog/?unique_number=true",
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        var smsUniqueList = JSON.parse(body)
        addresses = []
        truncatedMessages = []
        for(let i=0; i<smsUniqueList.length; i++) {
          addresses.push(smsUniqueList[i]['address'])
          truncatedMessages.push(smsUniqueList[i]['message'].substring(0,20)+'..')
        }
        res.render('sms', {addresses: addresses, truncatedMessages : truncatedMessages, smsMessages: smsMessages, smsType: smsType})
      }
    }
  );
});

app.get("/sms/:address", (req,res)=> {
  request(
    "http://127.0.0.1:8000/api/SmsLog/?address=" + req.params.address,
    function (error, response, body) {
      if (!error && response.statusCode == 200) {
        let smsDate = [], smsTime = []
        var smsLog = JSON.parse(body)
        smsMessages = []
        smsType = []
        for(let i=0; i<smsLog.length; i++) {
          smsMessages.push(smsLog[i]['message'])
          smsType.push(smsLog[i]['sms_type'])

          var datetime = smsLog[i]["datetime"].split("T");

          const string_after_splitting = datetime[0].split("-");
          datetime[0] = string_after_splitting.join("/");

          smsDate.push(datetime[0]);
          datetime[1] = datetime[1].substring(0, datetime[1].length - 1);

          smsTime.push(datetime[1]);
        }
      }
    }
  );
  res.render('sms', {addresses: addresses, truncatedMessages : truncatedMessages, smsMessages: smsMessages, smsType: smsType})
})

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

app.get("/facialrecognition", (req,res)=> {
  res.render("facialRecognition");
})

app.listen(3000, () => {
  console.log("listening to port : 3000");
});
