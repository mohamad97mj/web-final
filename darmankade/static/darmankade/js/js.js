function login() {
    window.open('api/login-as', '_self');
}

function myregister() {
    window.open('api/register-as', '_self');
}


function doctors() {
    window.open('api/doctors', '_self');
}

function doctor_instance(id) {
    window.open('api/doctors/' + id, '_self');
}

function specialities() {
    window.open('medical-specialities.html', '_self');
}

const redirect = function (url) {
    location.href = url;
};

const myfetch = async (url2fetch) => {
    try {
        let response = await fetch(url2fetch);
        // console.log(response)
        return await response.json();
    } catch (e) {
        console.log(e);
    }
};

const addElementBeforeEnd = (targetId, html2insert) => {
    let parent = document.getElementById(targetId);
    parent.insertAdjacentHTML('beforeend', html2insert);
}
