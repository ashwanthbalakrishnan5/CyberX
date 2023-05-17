const express = require('express')
const bodyParser = require('body-parser');
const request = require('request');
const ejs = require('ejs');

const app =  express()
app.set('view engine', 'ejs')

app.use(bodyParser.json())
app.use(express.static("public"));

app.get("/", (req,res)=>{
    res.render("mainDashBoard")
})

app.get("/adb", (req,res)=>{
    res.render("adbWaitScreen")
})

app.get("/dashboard", (req,res)=>{
    res.render("secondaryDashBoard")
})

app.get("/contacts", (req,res)=>{
    var phNums = [], names = []

    request('http://127.0.0.1:8000/api/CallLog/?start_date=&end_date=&is_known=true&is_international=false&call_type=', function (error, response, body) {
        if (!error && response.statusCode == 200) {
            var callLogs = JSON.parse(body)
            for(let i = 0; i < callLogs.length; i++) {
                phNums.push(callLogs[i]['number'])
                names.push(callLogs[i]['contacts']['name'])
            }
            const uniqueContacts = names.filter((value, index, self) => {
                return self.indexOf(value) == index;
            });
            const uniquephNums = phNums.filter((value, index, self) => {
                return self.indexOf(value) == index;
            });

            res.render("contacts",{names: uniqueContacts, phnos: uniquephNums})
        }
    })

})

app.get("/contacts/:name-:phno", (req,res)=>{
    console.log(req.params)
})

app.get("/calllogs", (req,res)=>{
    res.render("callLogs")
})

app.get("/sms", (req,res)=>{
    res.render("sms")
})

app.get("/files", (req,res)=>{
    res.render("fileDashBoard")
})

app.get("/files/vedios", (req,res)=>{
    res.render("vedios")
})

app.get("/files/documents", (req,res)=>{
    res.render("documents")
})

app.get("/files/photos", (req,res)=>{
    res.render("photos")
})

app.listen(3000, ()=>{
    console.log("listening to port : 3000")
})
