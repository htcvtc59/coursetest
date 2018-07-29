var jwt_token = localStorage.getItem('jwt_token');
data = {
    "token": jwt_token
}

if (jwt_token) {

    axios({
        method: "post",
        url: "/api-token-refresh/",
        data: data,

        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": "JWT" + " " + localStorage.getItem('jwt_token')
        },
    }).then(function (response) {
        if (response.data) {
            localStorage.setItem('jwt_token', response.data.token);
        }
    }).catch(function (error) {
        window.location.href = '/';
        localStorage.clear();
    });

    axios({
        method: "post",
        url: "/api-token-verify/",
        data: {
            "token": localStorage.getItem('jwt_token')
        },
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": "JWT" + " " + localStorage.getItem('jwt_token')
        },
    }).then(function (response) {
        if (response.data) {
        } else {
            window.location.href = '/';
            localStorage.clear();
        }
    }).catch(function (error) {
        window.location.href = '/';
        localStorage.clear();
    });

} else {
    window.location.href = '/';
}


