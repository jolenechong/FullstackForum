function deleteNote(noteId) {
  fetch("/delete-note", {
    // send note rewuest to delete note end point
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    // reload after getting response to show the home page with the delted note
    window.location.href = "/";
  });
}

function showcreatepost() {
  var form = document.getElementById("createPost");
  form.style.display = form.style.display === 'none' ? '' : 'none'
}

//create comments
var comment = document.querySelector("#create-comment #text ");
comment.addEventListener("keyup", function (event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("submitComment").click();
  }
});

//view comments
var btncomment = document.querySelectorAll(".viewComments");
for(var i = 0; i < btncomment.length; i++){
    btncomment[i].addEventListener("click", function (e) {
        var comments = e.currentTarget.parentElement.parentElement.parentElement.getElementsByClassName('comments')[0]
        comments.style.display =
        comments.style.display === "none"
            ? ""
            : "none";
      });
}


function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    fetch(`/like-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
          likeButton.className = "fas fa-sort";
        } else {
          likeButton.className = "fas fa-sort";
        }
      })
      .catch((e) => alert("Could not like post."));
  }