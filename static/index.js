
$(document).ready(function(){
    $("#signout").click(function(){
        document.cookie = "x-access-token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
        window.location.href='/';
    });
        const options = {
            method:"GET",
            headers:{'x-access-token':getCookie('x-access-token')}
        }
        fetch('/user',options)
            .then(data =>data.json())
            .then(data=>{
                $("#myform").html("");
                for(const key in data){
                $("#myform").append("<p>"+key+" : "+"<input type='text' name='"+key+"' value='"+data[key]+"'></p>");
            }
            $("#myform").append("<input type='submit' id='submit' value='Save'>");
            });
        
        $("#delete").submit(function(){
            var val = $("#delete").serializeArray();
            var options = {
                method:"GET",
                headers:{'x-access-token':getCookie('x-access-token')},
                body:val
            }
            fetch('/delete',options).then(data => data.json()).then(data=>{
                window.location.href='/';
            });
        });

        $("#myform").submit(function(){
            var val = $("#myform").serializeArray();
            let vall={};
            for(var i=0;i<val.length;i++){
                vall[val[i].name]=val[i].value
            }
            var options = {
                method:"GET",
                headers:{'x-access-token':getCookie('x-access-token')},
            }
            let data =fetch('/update?'+new URLSearchParams(vall),options).then(data=>data.json());
            console.log(data);
            for(const key in data){
                $("#data").append("<p>"+key+" : "+data[key]+"</p>");
            }
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