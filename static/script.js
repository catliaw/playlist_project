"use strict";

$(function(){

    function getCheckedArtists(){

        var artistsArray = [];

        $("input.artist_checkbox:checkbox[name=artist]:checked").each(function() {
            artistsArray.push($(this).val());
        });

        console.log("getCheckedArtists returns", artistsArray);
        return artistsArray;
    }


    function displayPlaylist(data){
        console.log(data);

        var topHTML = "<h3>Playlist Preview</h3>" +
            "<ul>";

        var bottomHTML = '</ul>' +
            '<form>' +
            '<p>Playlist name: ' +
            '<input id="playlist_name" type="text" name="playlist_name"></p>' +
            '<div class="generate_div">' +
            '<button id="generate_button" type="button">' +
            'Generate Spotify Playlist</button>' +
            '</div>' +
            '</form>';

        console.log(bottomHTML)

        $("#playlist_preview").html(topHTML);

        for (var key in data){
            if (data.hasOwnProperty(key)) {

                console.log(key + " - " + data[key]);

                for (var innerKey in data[key]) {
                    if (data[key].hasOwnProperty(innerKey)) {

                        console.log(innerKey + " - " + data[key][innerKey]);

                        var listHTML = '<li class="trackid" data-trackid="' +
                            data[key][innerKey] + '">' + key + ' - ' +
                            innerKey + '</li>';

                        $('#playlist_preview').append(listHTML);
                    }
                }
            }
        }
        $('#playlist_preview').append(bottomHTML);
        $("#generate_button").on("click", generatePlaylist);
    }


    function submitCheckedArtists(event){
        event.preventDefault();
        
        var artistsAdded = getCheckedArtists();
        console.log("artistsAdded", artistsAdded);

        // var artistsObject = {"artists[]": artistsAdded};
        // console.log("artistsObject", artistsObject);

        $.post("/preview.json", {"artists": artistsAdded}, displayPlaylist);
    }


    $("#playlist_submit").on("submit", submitCheckedArtists);


    function clearArtists(event){
        event.preventDefault();
        $('input[type=checkbox]').each(function() {
            this.checked = false;
        });
    }

    $("button#playlist_clear_button").on("click", clearArtists);


    function getTrackId(){
        var trackIdArray = [];

        // console.log('found a bunch of track ids(?)')
        // console.log($(".trackid").length);

        $(".trackid").each(function() {
            trackIdArray.push($(this).attr("data-trackid"));
        });

        console.log("getTrackId returns", trackIdArray);
        return trackIdArray;
    }


    function getPlaylistName() {
        var playlistName = $("input#playlist_name").val();

        return playlistName;
    }


    function generatePlaylist(event) {
        event.preventDefault();

        var tracksToAdd = getTrackId();
        console.log("Tracks To Add:", tracksToAdd);

        var playlistName = getPlaylistName();
        console.log("Name of Playlist:", playlistName);

        $.post("/generate", {"tracks": tracksToAdd, "playlist_name": playlistName}, playlistNewTab);
    }

    function playlistNewTab(data) {
        console.log("Playlist Spotify URL:", data);
        var url = data['url'];
        // location.replace(url);
        window.open(url, "_blank");
    }
 
});