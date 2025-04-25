document.addEventListener('DOMContentLoaded', function(){

  //Open post text editor
  document.querySelector('#write-post').addEventListener('click', (event)=>{
    event.preventDefault();
    document.querySelector('.new-post-container').style.display = 'block';
    document.querySelector('.feed-container').style.paddingTop = '200px';
  })

  //cancel post
  document.querySelector('.post-action').addEventListener('click', ()=>{
    document.querySelector('.new-post-container').style.display = 'none';
    document.querySelector('.post-text').value ='';
  })

  //Save Post
  /*
  document.querySelector('#save-post').addEventListener('click', ()=>{
    document.querySelector('.new-post-container').style.display = 'none';
    document.querySelector('.post-text').value ='';
  })*/

 // Fetch likes

 const likeButton = document.querySelectorAll('.like-button')
  if (likeButton){
    likeButton.forEach(button=>{
      let postId = button.getAttribute("data-id")
      fetch(`/likes/${postId}`,{
            metho: "POST",
          headers:{'Accept': 'application/json',
              'X-Requested-With': 'XMLHttpRequest',
          },
      })
      .then(response=>{return response.json()})
      .then(data=>{
          if (data.likes != 0){
              button.innerHTML=`${data.likes} like`
          } 
          if (data.isLiked){
              button.style.color = "#dd6b00"
          }
      })
  })
  }          

  // Like a post

  likeButton.forEach(button=>{button.addEventListener('click', ()=>{
    let postId = button.getAttribute("data-id")
    fetch(`/like/${postId}`,{
        headers:{'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response=>{return response.json()})
    .then(data=>{
        if (data.likes != 0){
            button.innerHTML=`${data.likes} like`
        }
        else{
            button.innerHTML=`like`
        }
        if (data.isLiked){
            button.style.color = "#dd6b00"
        }else{
            button.style.color = "white"

        }
    })
    })
  })

  /********Edit function*********/

  const editButton = document.querySelectorAll('.edit')
  const overlayDiv = document.querySelector(".overlay")

  editButton.forEach(button=>{button.addEventListener('click', ()=>{
      postId = button.getAttribute("data-id")
      /*fetch post to be edited*/
      fetch(`/edit/${postId}`,{
          headers:{'Accept': 'application/json',
              'X-Requested-With': 'XMLHttpRequest',
          },
      })
      .then(response=>{return response.json()})
      .then(data=>{
          
          /**Creat a text area and fill it with the contents of the post to be edited**/

          const posActions = document.querySelector(`#post-footer-${postId}`)
          const editActions = document.querySelector(`#edit-footer-${postId}`)
          const postContent = document.querySelector(`#content-${postId}`)
          const postTimestamp = document.querySelector(`#timestamp-${postId}`)

          const postEditText = document.querySelector(`#edit-${postId}`)
          postEditText.value = data.content

          postEditText.style.zIndex = 11
          editActions.style.zIndex = 11
          overlayDiv.style.zIndex = 10
          overlayDiv.style.opacity = 0.05
          postEditText.style.display = "block"
          postContent.style.display = "none"
          posActions.style.display = "none"
          editActions.style.display = "block"
          editActions.style.display = "flex"
          
          /** Create an eventlistener for the save button**/

          const saveButton = document.querySelector(`#save-${postId}`)

          saveButton.addEventListener('click', ()=>{
              editedPostContent = postEditText.value
              
              fetch(`/edited/${postId}`,{
                  method: "PUT",
                  headers:{'Accept': 'application/json',
                  'X-Requested-With': 'XMLHttpRequest',
                  },
                  body: JSON.stringify({"contents": editedPostContent}),
              })
              .then(response =>{return response.json()})
              .then(data => {
                  postContent.innerHTML = data.content
                  postTimestamp.innerHTML = data.timeStamp
                  cancelEdit()
              })
              .catch(error => {console.log(error)})
          })

          // Cancel Edit button eventlistener
          const cancelButton = document.querySelector(`#cancel-${postId}`)

          cancelButton.addEventListener("click", cancelEdit)

          function cancelEdit(){
              postEditText.style.zIndex = 1
              editActions.style.zIndex = 1
              overlayDiv.style.zIndex = -10
              overlayDiv.style.opacity = 0

              postEditText.style.display = "none"
              postContent.style.display = "block"
              posActions.style.display = "block"
              posActions.style.display = "flex"
              editActions.style.display = "none"
          }
          
      })
  })})

  /** Follow or unfollow a user**/

  const followButton = document.querySelector(".follow")
  const followersDiv = document.querySelector(".followers")
  followButton.addEventListener('click',()=>{
    userId = followButton.getAttribute("data-id")
    fetch(`/follow/`,{
        method: "POST",
        headers:{'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({"userId": userId}),
    })
    .then(response => {return response.json()})
    .then(data =>{

        data.isFollowing? followButton.value = "Unfollow":followButton.value = "Follow"
        followersDiv.innerHTML= `${data.followers} Followers`
        
    })
  })
  
})

