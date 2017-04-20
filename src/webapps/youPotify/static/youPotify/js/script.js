function showAddNewSongModal(spotifyId) {

  // getting current playlist data
  var url = "/get_playlists"

  $.get(url)
    .done(function(data) {

      if(data.length == 0) {
        var msg = "No playlist exist. Please create at least one playlist"
        
        $('#confirm-modal-msg').html(msg)
        $('#confirmModal').modal('show')        
      } else {
        $('#playlistOptions').html('')
        for(entry of data) {
          $('#playlistOptions').append('<option value="' + entry.pk + '">' + entry.fields.name + '</option>')
        }

      // getting song data
      var url = "https://api.spotify.com/v1/tracks/" + spotifyId

      $.get(url)
        .done(function(data) {
          $('#song-artist').html(data.artists[0].name)
          $('#song-title').html(data.name)
          $("#song-thumbnail").data("id", spotifyId);
          $('#song-thumbnail').attr("src", data.album.images[1].url);
          $('#addSongModal').modal('toggle')
        });

      }
    });
}

function addNewSong() {

  $('#addSongModal').modal('hide')
  var id = $("#song-thumbnail").data("id")  
  var playlistId = $('#playlistOptions').val();
  var name = $('#playlistOptions option:selected').text();

  var url = '/add_new_song'

  $.post(url, {'songId': id, 'playlistId': playlistId}) 
    .done(function(data) {
      var msg = "This song has been added to '" + name + "'"
      
      $('#confirm-modal-msg').html(msg)
      $('#confirmModal').modal('show')
    });
}


function showAddSongModal(spotifyId, songId) {

  // getting current playlist data
  var url = "/get_playlists"

  $.get(url)
    .done(function(data) {

      if(data.length == 0) {
        var msg = "No playlist exist. Please create at least one playlist"
        
        $('#confirm-modal-msg').html(msg)
        $('#confirmModal').modal('show')        
      } else {

        $('#playlistOptions').html('')
        for(entry of data) {
          $('#playlistOptions').append('<option value="' + entry.pk + '">' + entry.fields.name + '</option>')
        }

      // getting song data
      var url = "https://api.spotify.com/v1/tracks/" + spotifyId

      $.get(url)
        .done(function(data) {
          $('#song-artist').html(data.artists[0].name)
          $('#song-title').html(data.name)
          $("#song-thumbnail").data("id", spotifyId);
          $("#song-thumbnail").data("songId", songId);
          $('#song-thumbnail').attr("src", data.album.images[1].url);
          $('#addSongModal').modal('toggle')
        });
      }

    });
}

function pickSongToPlaylist() {

  $('#addSongModal').modal('hide')
  var id = $("#song-thumbnail").data("songId")  
  var playlistId = $('#playlistOptions').val();
  var name = $('#playlistOptions option:selected').text();

  var url = '/pick_song_to_playlist'

  $.post(url, {'songId': id, 'playlistId': playlistId}) 
    .done(function(data) {
      if(data.code == 'duplicate') {
        var msg = "This song is already in '" + name + "'" + ". Skipping duplicates."
      } else {
        var msg = "This song has been added to '" + name + "'"
      }

      $('#confirm-modal-msg').html(msg)
      $('#confirmModal').modal('show')
    });
}

function showSendSongModal(id) {
  var url = "https://api.spotify.com/v1/tracks/" + id

  $.get(url)
    .done(function(data) {
      $('#send-song-text').val('')

      $('#song-artist-send').html(data.artists[0].name)
      $('#song-title-send').html(data.name)
      $("#song-thumbnail-send").data("id", id);
      $('#song-thumbnail-send').attr("src", data.album.images[1].url);
      $('#sendSongModal').modal('toggle')
    });
}


function sendSong() {
  $('#sendSongModal').modal('hide')
  var songId = $("#song-thumbnail-send").data("id")
  var to = $('#send-song-to').val()
  var msg = $('#send-song-text').val()

  $.post('/send_song', {'songId': songId, 'to': to, 'msg': msg})
    .done(function(data) {
      var msg = "This song has been sent to " + data.receiver +"."
      $('#confirm-modal-msg').html(msg)
      $('#confirmModal').modal('show')

      // websocket
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      var song_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

      var message = {
                sender: data.sender,
                message: data.message,
                songId: songId,
      }

      setTimeout(function(){ song_socket.send(JSON.stringify(message)); }, 1000);


    });
}

function notification(sender, msg, songName) {
  console.log(sender)
  console.log(msg)
  $("#notificationIcon").html('')
  $("#notification-modal-sender").html("<p>From: " + sender + "</p><p>Song: " + songName + "</p>" )
  // $("#notification-modal-sender").html(sender + " sent you " + "\"" + songName + "\"" + " and left the following message:")
  $("#notification-modal-msg").html("Message: " + msg)
  $('#notificationModal').modal('show')
}


function deleteSongOnClick(id) {
  $('#deleteModal').modal('show')
  $("#deleteSongId").data("id", id)
}


// this will be called from playlist and bucket, it deletes relations only
function deleteSong(source, sourceId) {
  $('#deleteModal').modal('hide')
  var songId = $("#deleteSongId").data("id")

  $.post('/delete_song', {'songId': songId, 'source': source, 'sourceId': sourceId})
    .done(function(data) {
      $(".track_row[data-id='" + songId + "']").remove()

      var msg = "Successfully deleted"
      $('#confirm-modal-msg').html(msg)
      $('#confirmModal').modal('show')
    });
}


// this will only be call from library page, it actually delete songs
function deleteSongFromLibrary() {
  $('#deleteModal').modal('hide')
  var songId = $("#deleteSongId").data("id")
  $.post('/delete_from_library', {'songId': songId})
    .done(function(data) {
      $(".track_row[data-id='" + songId + "']").remove()

      var msg = "Successfully deleted"
      $('#confirm-modal-msg').html(msg)
      $('#confirmModal').modal('show')
    });
}

function deletePlaylist(id) {

  $.post('/delete_playlist', {'playlistId': id})
    .done(function(data) {
      window.location = "/library";
    });
}


function showMsg(msg) {
  console.log(msg)
  $('#show-modal-msg').html(msg)
  $('#msgModal').modal('show')
}

function selectTrack(id) {
  $('.iframe').html('')
  var iframe = '<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + id + '" height="80" frameborder="0" allowtransparency="true"></iframe>'
  $('.iframe').html(iframe)
}

function unpublicPlaylist(id) {

  $.post('/unpublic_playlist', {'playlistId': id})
    .done(function(data) {
      location.reload();
    });
}

function publicPlaylist(id) {

  $.post('/public_playlist', {'playlistId': id})
    .done(function(data) {
      location.reload();
    });
}



//Ajax for playlist

function createPlaylistOnClick() {
  $('#create-playlist-name').val('')
  $('#createPlaylistModal').modal('show')
}


function createPlaylist() {
  var playListName = $('#create-playlist-name').val()
  $.post('/create_playlist', {'name': playListName})
    .done(function(data) {
      var newPlaylist = $('<a href="/playlist/' + data.playlistId + '" class="list-group-item">' + playListName + '</a>')
      newPlaylist.insertBefore('.add-playlist');
      $('#createPlaylistModal').modal('hide')
    });
}




$(document).ready(function () {

  // CSRF set-up copied from Django docs
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
  var csrftoken = getCookie('csrftoken');
  // $.ajaxSetup({
  //   beforeSend: function(xhr, settings) {
  //       xhr.setRequestHeader("X-CSRFToken", csrftoken);
  //   }
  // });
});


