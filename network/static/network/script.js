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

  
  
})