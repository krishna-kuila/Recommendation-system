const loader = document.getElementById('loader');
const left = document.getElementById('left');
const right = document.getElementById('right');
const message = document.getElementById("messages")
const label_output = document.getElementById('predicted-output');
const clear_btn = document.getElementById('clear-btn');
const search_btn = document.getElementById('search-btn');
const form_btn = document.getElementById('openFormBtn');

async function search_user() {
    message.style.display = "none";
    const search_box = document.getElementById('search-inp');
    loader.style.display = "none"
    left.style.display = "none"
    right.style.display = "none"
    label_output.style.display = "none";
    const search_data = search_box.value.trim();
    search_btn.disabled = true;
    clear_btn.disabled = true;
    form_btn.disabled = true;

    if(search_data==='') {
        message.style.display = "flex";
        message.innerText = "Not An Valid Input"
        search_btn.disabled = false;
        clear_btn.disabled = false;
        form_btn.disabled = false;
        return;
    }

    try {
        loader.style.display = "flex";
        const response = await fetch('http://127.0.0.1:5000/user', {
            method: 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify(search_data)
        });
        if(response.ok) {
            const user = await response.json();
            if(!user) {
                message.style.display = "flex";
                message.innerText = "User Not Found...";
            } else {
                left.style.display = "flex";
                right.style.display = "flex";
                label_output.style.display = "flex";
                search_btn.disabled = false;
                clear_btn.disabled = false;
                display_user(user);
            }
        }
    } catch(e) {
        message.style.display = "flex";
        message.innerText = "Internal Server Error...";
        label_output.style.display = "none";
        left.style.display = "none";
        right.style.display = "none";
        search_btn.disabled = false;
        clear_btn.disabled = false;
        form_btn.disabled = false;
        console.error(e);
    } finally {
        loader.style.display = "none";
        search_btn.disabled = false;
        clear_btn.disabled = false;
        form_btn.disabled = false;
    }
}

function display_user(user) {
    left.innerHTML = `
        <div style="
            width: 90%;
            height: 90%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding-left: 10px;
            cursor: pointer;
        " 
            id="org-user-div"

            data-name="${user.user.name}"
            data-bio="${user.user.bio}"
            data-comments="${user.user.comments}"
            data-handle="${user.user.handle}"
            data-src="static/user.png"
            onclick="showDetails(this)"
        >
            <img src="static/user.png" width="80" height="80">
            <h3>${user.user.name}</h3>
            <p>Bio : ${user.user.bio}</p> 
        </div>
    `
    show_limit(user);
}

function clearAll() {
    const search_box = document.getElementById('search-inp');
    search_box.value = ""
    loader.style.display = "none"
    message.innerText = ""
    message.style.display = "none"
    left.style.display = "none"
    right.style.display = "none"
    label_output.style.display = "none";
}

function show_limit(user) {

    right.innerHTML = ''
    right.style.display = 'grid'

    for(let i=0; i<4; i++) {
        right.innerHTML += `
            <div class="profile-card"
                data-name="${user.users[i].name}"
                data-id="${user.users[i].id}"
                data-comments="${user.users[i].comments}"
                data-bio="${user.users[i].bio}"
                data-src="static/account.png"
                onclick="showDetails(this)"
            >
                <img src="static/account.png" class="profile-avatar" alt="Profile">
                <h3 class="profile-name">${user.users[i].id}</h3>
                <p class="profile-handle">@${user.users[i].name}</p>
                <div class="profile-score">
                    Score: <span class="score-num">${user.users[i].score}</span>
                </div>
            </div>
        `
    }
}