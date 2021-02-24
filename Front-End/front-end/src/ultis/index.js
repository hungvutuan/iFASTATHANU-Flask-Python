export function get(url, config = {}) {
    return fetch(url, {
        method: "GET",
        ...config
    }).then(res => {
        if (res.ok) {
            return res.json()
        }
    })
}

export function deleted(url, config = {}) {
    return fetch(url, {
        method: "DELETE",
        ...config
    })
}

export function post(url, data, config = {}) {
    return fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        },
        ...config
    }).then(res => {
        if (res.ok) {
            return res;
        }
        else {

        }
    })
}

export function put(url, data, config = {}) {
    return fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            Accept: "application/json",
            "Content-type": "application/json"
        },
        ...config
    })
}    