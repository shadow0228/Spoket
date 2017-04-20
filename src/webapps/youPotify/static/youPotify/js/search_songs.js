function millisToMinutesAndSeconds(millis) {
  var minutes = Math.floor(millis / 60000);
  var seconds = ((millis % 60000) / 1000).toFixed(0);
	return (seconds == 60 ? (minutes+1) + ":00" : minutes + ":" + (seconds < 10 ? "0" : "") + seconds);
}

function searchSongs(e) {
	var song_name = $('#songs').val();
	var str1 = "https://api.spotify.com/v1/search?q=";
	var str2 = song_name;
	var str3 = "&offset=0&limit=20&type=track";
	var url = str1.concat(str2, str3);
	$.get(url)
		.done(function(data) {

			if(data.tracks.items.length == 0) {
				var table = $("#search_result");
				table.html('<p>No results found, please try another search term.</p>')
			} else {

				var table = $("#search_result");
				var tableHeader = '            <tr>\
	              <td>Send</td>\
	              <td>Save</td>\
	              <td>Song</td>\
	              <td>Artist</td>\
	              <td><span class="glyphicon glyphicon-time" aria-hidden="true"></span></td>\
	            </tr>'

				table.html(tableHeader)
				for (var i = 0; i < data.tracks.items.length; i++) {

					time = millisToMinutesAndSeconds(data.tracks.items[i].duration_ms)

					var tableRow = 
					'<tr id = "' + data.tracks.items[i].id + '" onClick="selectTrack(\'' + data.tracks.items[i].id + '\')">\
					  <td><a href="#">\
					  	<span onClick="showSendSongModal(\'' + data.tracks.items[i].id + '\')" class="glyphicon glyphicon-envelope"></span>\
		              	</a></td>\
		              <td><a href="#">\
		              	<span onClick="showAddNewSongModal(\'' + data.tracks.items[i].id + '\')" class="glyphicon glyphicon-plus"></span>\
		              	</a></td>\
		              <td>' + data.tracks.items[i].name + '</td>\
		              <td>' + data.tracks.items[i].artists[0].name + '</td>\
		              <td>' + time + '</td>\
		            </tr>'
					table.append(tableRow)
				}

				// $('.addSongBtn').click(showAddNewSongModal);
			}

	});
}

function toSearchSongs(e) {
	var term = $('#songs').val();
	url = '/search/?term=' + term
	window.location = url;
}


$(document).ready(function () {
  $('#search-btn').click(searchSongs);
  $('#to-search-btn').click(toSearchSongs);
  // $('.addSongBtn').click(showAddNewSongModal);
  $("#songs").keypress(function (e) { if (e.which == 13) toSearchSongs(); } );
});