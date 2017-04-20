
window.fbAsyncInit = function() {
  FB.init({
    appId      : 193549377719983,                     
    xfbml      : true,  
    cookie     : true,
    version    : 'v2.8' 
  });

  FB.getLoginStatus(function(response) {
    console.log('statusChangeCallback');

    if (response.status === 'connected') {
      console.log(">>> fb login success")
    } else if (response.status === 'not_authorized') {
      console.log(">>> fb login not_authorized")
    } else {
      console.log(">>> fb logged out")

    }
  });

};

(function(d, s, id){
  var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


function fbLogout() {
  window.location = "/logout";
}

function fbLogin(){
  FB.login(function(response) {
    if (response.status === 'connected') {
      console.log('Welcome!  Fetching your information.... ');
      sendFbData();
    }
  }, {
      scope: 'email, user_friends',
  });

}

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

var inited = false;

function sendFbData() {
  FB.api('/me', {fields: 'picture.type(large), email, id, name, first_name, last_name, friends'}, function(response) {
    var test = []

    for (i = 0; i < response.friends.data.length; i++) {
      test.push(response.friends.data[i].id);
    }

    $.ajax({
       url: '/add_user/',
       type: 'POST',
       data: {'id': response.id, 'picture': response.picture.data.url, 'name': response.name, 
        'email': response.email, 'firstName': response.first_name, 'lastName': response.last_name,
        'friends': test},
       dataType: 'json',
       complete: function() {
        window.location = "/library";
      },
    });
  });
}


function updateFbFriends() {
  FB.api('/me', {fields: 'picture.type(large), email, id, name, first_name, last_name, friends'}, function(response) {
    var test = []

    for (i = 0; i < response.friends.data.length; i++) {
      test.push(response.friends.data[i].id);
    }

    $.ajax({
       url: '/add_user/',
       type: 'POST',
       data: {'id': response.id, 'picture': response.picture.data.url, 'name': response.name, 
        'email': response.email, 'firstName': response.first_name, 'lastName': response.last_name,
        'friends': test},
       dataType: 'json',
       complete: function() {
        window.location = "/friends";
      },
    });
  });

}


