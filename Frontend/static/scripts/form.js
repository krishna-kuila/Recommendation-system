document.addEventListener('DOMContentLoaded', () => {
const openBtn = document.getElementById('openFormBtn');
const closeBtn = document.getElementById('closeFormBtn');
const modal = document.getElementById('formModal');
const form = document.getElementById('contactForm');
const url = "http://127.0.0.1:5000/new-user"

openBtn.addEventListener('click', () => {
    modal.classList.add('show');
});

closeBtn.addEventListener('click', () => {
    modal.classList.remove('show');
});

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.classList.remove('show');
    }
});

form.addEventListener('submit', async function(e) {
    e.preventDefault();
    left.style.display="none";
    right.style.display = "none"
    clearAll();
    const name = document.getElementById('name_')
    const bio = document.getElementById('bio_')

    let new_name = name.value.trim();
    let new_bio = bio.value.trim();

    if(new_name!=='' || new_bio!=='') {
        try {
            loader.style.display = "flex";
            const res = await fetch(url, {
                method: 'POST',
                headers : {
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify({
                    "name" : new_name,
                    "bio" : new_bio
                })
            })

            if(res.ok) {
                const user = await res.json();
                left.style.display = "flex";
                label_output.style.display = "flex";
                search_btn.disabled = false;
                clear_btn.disabled = false;
                const new_user = {
                    "name" : new_name,
                    "bio" : new_bio
                }
                console.log(new_user)
                display_new_user(user, new_user);
            }
        } catch(e) {
            label_output.style.display = "none";
            left.style.display = "none";
            label_output.style.display = "none";
            console.error('NETWORK ERROR');
        } finally {
            loader.style.display = "none";
            search_btn.disabled = false;
            clear_btn.disabled = false;
        }

    }
    modal.classList.remove('show');
    form.reset();
    });
});

function display_new_user(user, new_user) {
    left.innerHTML = `
        <div style="
            border: 1px solid black;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding-left: 10px;
        " id="org-user-div">
            <img src="static/user.png" width="80" height="80">
            <p>User : ${new_user.name}</p>
            <p>Bio : ${new_user.bio}</p>
        </div>
    `

    right.innerHTML = ''
    right.style.display = 'grid'

    for(let i=0; i<4; i++) {
        right.innerHTML += `
            <div style="
                background-color: #4a90e2;
                padding: 30px;
                border-radius: 8px;
                text-align: center;
                font-family: sans-serif;
                max-width: 300px;
                max-height: 300px;
            ">
                <img src="static/account.png" width="50", height="50">
                <p>user : ${user.users[i].name}</p>
                <p>handle : ${user.users[i].handle}</p>
                <p>Score : <span style="background-color:green; font-weight: bold">${user.users[i].score}</span></p>
            </div>
        `
    }

}