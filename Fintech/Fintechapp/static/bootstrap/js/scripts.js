/*!
    * Start Bootstrap - SB Admin v7.0.5 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2022 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

var predictVal=1500;
var actualVal=1800;
var today;
var nextday;
var nextdayPred=2000;

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function CalculateError() {

    var error = document.getElementById("errorval");

    if (predictVal>actualVal) {
        //blue
        error.innerHTML += " -";
        error.style.color = "blue";
    } else {
        //red
        error.innerHTML += " +";
        error.style.color = "red";
    }

    var errorVal=Math.abs(predictVal-actualVal);
    return error.innerHTML+errorVal;
}

function printDate() {

    const day = new Date();
    const year = day.getFullYear();
    const month = day.getMonth()+1;
    const date = day.getDate();
    const nextdate = day.getDate()+1;

    today = year +"."+ month +"."+ date;
    nextday = year +"."+ month +"."+ nextdate;

    return today;
}

printDate();

function printResult() {

    var str = nextday;

    return str;
}

document.getElementById("dates").innerHTML = today+"(오늘)";
//document.getElementById("errorval").innerHTML += CalculateError();
document.getElementById("resultday").innerHTML += printResult();

function movepage() {
    var company = document.getElementById("company-list");
    var companyval = company.options[company.selectedIndex].value;
    
    var item = document.getElementById("item-list");
    var itemnum = item.options[item.selectedIndex].value;

    window.location.href = "https://pnu-fintech.run.goorm.app/company_good/"+companyval+"/"+itemnum;
}

//--------------------------------------------------//
//select 하면 유지되게 하는 부분(드롭다운)
var addr =  window.location.href
var c_opt;
var g_opt;

if (addr === "https://pnu-fintech.run.goorm.app/company_good/c0/g0") {
    c_opt = document.querySelector('option[value="c0"]');
    g_opt = document.querySelector('option[value="g0"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c0/g1") {
    c_opt = document.querySelector('option[value="c0"]');
    g_opt = document.querySelector('option[value="g1"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c1/g0") {
    c_opt = document.querySelector('option[value="c1"]');
    g_opt = document.querySelector('option[value="g0"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c1/g1") {
    c_opt = document.querySelector('option[value="c1"]');
    g_opt = document.querySelector('option[value="g1"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c2/g0") {
    c_opt = document.querySelector('option[value="c2"]');
    g_opt = document.querySelector('option[value="g0"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c2/g1") {
    c_opt = document.querySelector('option[value="c2"]');
    g_opt = document.querySelector('option[value="g1"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c3/g0") {
    c_opt = document.querySelector('option[value="c3"]');
    g_opt = document.querySelector('option[value="g0"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c3/g1") {
    c_opt = document.querySelector('option[value="c3"]');
    g_opt = document.querySelector('option[value="g1"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c4/g0") {
    c_opt = document.querySelector('option[value="c4"]');
    g_opt = document.querySelector('option[value="g0"]');
} else if (addr === "https://pnu-fintech.run.goorm.app/company_good/c4/g1") {
    c_opt = document.querySelector('option[value="c4"]');
    g_opt = document.querySelector('option[value="g1"]');
}

c_opt.selected = true;
g_opt.selected = true;