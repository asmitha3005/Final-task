function confirmDelete(){

return confirm("Are you sure you want to delete this post?");

}

function validatePost(){

let title=document.getElementsByName("title")[0].value;

let content=document.getElementsByName("content")[0].value;

if(title=="" || content==""){

alert("Please fill all fields.");

return false;

}

return true;

}

function commentAdded(){

alert("Comment Added Successfully");

}
