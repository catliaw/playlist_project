"use strict";

$(function(){

    function clearCustom(i){
        $("#box_label"+i).parent().removeClass("not-on-spotify");
        $("#box_label"+i).parent().removeClass("in-spotify");
        $("#box_span"+i).empty();
        $("#box_input"+i).attr("disabled", false);
        $(".filter_header").remove();
        // console.log("Done custom attributes!");
    }


    function loadLineup(data, index){

        for (var i=index; i < data.length; i++){
            // console.log("Start Javascript for", data[i].artist_name);
            var boxClass, disabledCheck, spotifyString;
            if (data[i].spotify_artist_id === null){
                // console.log("Start custom attributes!");
                boxClass = "not-on-spotify";
                disabledCheck = true;
                spotifyString = '<br/>(Not on Spotify)';
                // console.log("Done with Not in Spotify for", data[i].artist_name);
            } else {
                boxClass = "in-spotify";
                disabledCheck = false;
                spotifyString = '';
                // $("#box_input"+i).after().html(data[i].artist_name);
                // console.log("Done with In Spotify for", data[i].artist_name);
            }
            clearCustom(i);                
            $("#box_label"+i).parent().addClass(boxClass);
            // console.log(data[i].playing_on);
            $("#box_label"+i).parent().attr("data-day", data[i].playing_on);
            $("#box_label"+i).parent().attr("data-stage", data[i].stage);
            $("#box_input"+i).val(data[i].artist_name);
            $("#box_input"+i).attr("disabled", disabledCheck);
            $("#box_span"+i).html(data[i].artist_name + spotifyString);

        }
    }


    function composeSortByABC(data) {

        var sortABC = data.sort(function (a, b) {
            return (a.artist_name < b.artist_name) ? -1 : 1;
        });

        loadLineup(sortABC, 0);
    };


    function composeSortByDay(data) {

        var sortByDay = data.sort(function (a, b) {
            if (a.playing_on == b.playing_on) {
                return (a.artist_name < b.artist_name) ? -1 : (a.artist_name > b.artist_name) ? 1 : 0;
            }
            else {
                return (a.playing_on < b.playing_on) ? -1 : 1;
            }
        });

        loadLineup(sortByDay, 0);
    };


    function composeSortByStage(data) {

        var sortByStage = data.sort(function (a, b) {
            if (a.stage == b.stage) {
                return (a.artist_name < b.artist_name) ? -1 : (a.artist_name > b.artist_name) ? 1 : 0;
            }
            else {
                return (a.stage < b.stage) ? -1 : 1;
            }
        });

        loadLineup(sortByStage, 0);
    };


    function addDayHeader() {

        var dowList = {
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        };

        $.each( dowList, function(key, value) {
            // var dowName = $('.lineup-box[data-day="' + key + '"]').first();
            // console.log("First" + value + "div", dowName);
            $('.lineup-box[data-day="' + key + '"]').first()
                .before('<div class="filter_header col-sm-12"><h3>' + value + '</h3></div>');
        });
    }


    function addStageHeader() {
        var stages = ["Sahara", "Outdoor", "Yuma", "Do Lab", "Gobi", "Mojave", "Coachella", "Despacio"]

        for (var i = 0; i < stages.length; i++){
            // var stageName = $('.lineup-box[data-stage="' + stages[i] + '"]').first();
            // console.log("First" + stages[i] + "div", stageName);
            $('.lineup-box[data-stage="' + stages[i] + '"]').first()
                .before('<div class="filter_header col-sm-12"><h3>' + stages[i] + '</h3></div>');
        }
    }


    function loadSortByDay(evt) {
        evt.preventDefault();
        clearArtists();
        composeSortByDay(artistInfo);
        addDayHeader();
    }

    function loadSortByStage(evt) {
        evt.preventDefault();
        clearArtists();
        composeSortByStage(artistInfo);
        addStageHeader();
    }

    function loadSortABC(evt) {
        evt.preventDefault();
        clearArtists();
        composeSortByABC(artistInfo);
    }

    loadLineup(artistInfo, 0);
    $('#sort_abc').on('click', loadSortABC);
    $('#sort_by_day').on('click', loadSortByDay);
    $('#sort_by_stage').on('click', loadSortByStage);


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

        console.log(bottomHTML);

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


    $("#playlist_submit").on("click", submitCheckedArtists);


    function clearArtists(){
        $('input[type=checkbox]').each(function() {
            this.checked = false;
        });
    }


    function clearArtistsEvent(event){
        event.preventDefault();
        $('input[type=checkbox]').each(function() {
            this.checked = false;
        });
    }

    $("button#playlist_clear").on("click", clearArtistsEvent);


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