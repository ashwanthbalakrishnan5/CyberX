const express = require('express')
const mongoose = require('mongoose')
const app =  express()

mongoose.connect("mongodb://0.0.0.0:27017/call_logs", {
    useNewUrlParser:true,
    useUnifiedTopology:true
})

app.listen(3001, ()=>{
    console.log("listening to port : 3001")
})

