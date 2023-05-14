const express = require('express')
const mongoose = require('mongoose')
const app =  express()

app.set('view engine', 'ejs')

app.use(express.static("public"));

mongoose.connect("mongodb://0.0.0.0:27017/call_logs", {
    useNewUrlParser:true,
    useUnifiedTopology:true
})

app.get("/", (req,res)=>{
    res.render("secondaryDashBoard")
})

app.get("/dashboard", (req,res)=>{
    res.render("mainDashBoard")
})

app.listen(3000, ()=>{
    console.log("listening to port : 3000")
})

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       console.log(xhttp.responseText)
    }
};
xhttp.open("GET", "filename", true);
xhttp.send();
