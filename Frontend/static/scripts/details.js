function showDetails(element) {
    let name = element.getAttribute('data-name');
    let handle = element.getAttribute('data-handle')
    let id = element.getAttribute('data-id')
    let bio = element.getAttribute('data-bio');
    let comments = element.getAttribute('data-comments');
    let image = element.getAttribute('data-src');
    
    if(bio === "null") {
        bio = ""
    }
    if(comments === null) {
        comments = "no comments yet."
    }

    if(handle === null) {
        handle = '@'+name;
        name = ''
    }
    
    document.getElementById('modalImage').src = image;
    document.getElementById('modalName').innerText = name;
    document.getElementById('modalHandle').innerText = handle;
    document.getElementById('modalId').innerText = id;
    document.getElementById('modalBio').innerText = bio;
    document.getElementById('modalComments').innerText = comments.substring(0, 300)+'...';

    document.getElementById('profileModal').style.display = "flex";
}

function closeProfile(event) {
    if(event.target.id === 'profileModal') {
        document.getElementById('profileModal').style.display = 'none';
    }
}