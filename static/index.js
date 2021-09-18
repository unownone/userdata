let user;
$(document).ready(function(){
    $("#search").click(function(){
        const username=$("#usr").val();
        const options = {
            method:"GET",
            headers:{'x-access-token':getCookie('x-access-token')}
        }
        console.log(options);
        fetch('/user?'+new URLSearchParams({username:username}),options)
            .then(data =>data.json())
            .then(data=>{
                $("#data").html("");
                for(const key in data){
                    console.log(1);
                $("#data").append("<p>"+key+" : "+data[key]+"</p>");}
            });
    });
});

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }