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

    function loadCheckedArtists(array, artist, i){
        if (typeof array !== 'undefined' && array.length > 0) {
            for (var index=0; index < artistsToAdd.length; index++) {
                if (artistsToAdd[index] === artist) {
                    console.log(artist);
                    console.log(i);
                    $("#box_input"+i).prop('checked', true);
                }
            }
        }
    }


    function loadLineup(data, index){

        for (var i=index; i < data.length; i++) {
            var boxClass, disabledCheck, onSpotifyString;
            var artistName = data[i].artist_name;

            if (data[i].spotify_artist_id === null){
                boxClass = "not-on-spotify";
                disabledCheck = true;
                onSpotifyString = '<br/>(Not on Spotify)';
            } else {
                boxClass = "in-spotify";
                disabledCheck = false;
                onSpotifyString = '';
            }

            clearCustom(i);                
            $("#box_label"+i).parent().addClass(boxClass);
            $("#box_label"+i).parent().attr("data-day", data[i].playing_on);
            $("#box_label"+i).parent().attr("data-stage", data[i].stage);
            $("#box_input"+i).val(artistName);
            $("#box_input"+i).attr("disabled", disabledCheck);
            $("#box_span"+i).html(artistName + onSpotifyString);
            loadCheckedArtists(artistsToAdd, artistName, i);
        }
    }


    function composeSortByABC(data) {

        var sortABC = data.sort(function (a, b) {
            var artistNameABCA = a.artist_name.toLowerCase().localeCompare(b.artist_name.toLowerCase());
            var artistNameABCB = b.artist_name.toLowerCase().localeCompare(a.artist_name.toLowerCase());
            return ( artistNameABCA < artistNameABCB ) ? -1 : 1;
        });

        loadLineup(sortABC, 0);
    };


    function composeSortByDay(data) {

        var sortByDay = data.sort(function (a, b) {
            if (a.playing_on == b.playing_on) {
                var artistNameDayA = a.artist_name.toLowerCase().localeCompare(b.artist_name.toLowerCase());
                var artistNameDayB = b.artist_name.toLowerCase().localeCompare(a.artist_name.toLowerCase());
                return (artistNameDayA < artistNameDayB) ? -1 : (artistNameDayA > artistNameDayB) ? 1 : 0;
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
                var artistNameStageA = a.artist_name.toLowerCase().localeCompare(b.artist_name.toLowerCase());
                var artistNameStageB = b.artist_name.toLowerCase().localeCompare(a.artist_name.toLowerCase());

                return (artistNameStageA < artistNameStageB) ? -1 : (artistNameStageA > artistNameStageB) ? 1 : 0;
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
                .before('<div class="filter_header col-sm-12"><h3 class="filter-header-text">' + value + '</h3></div>');
        });
    }


    function addStageHeader() {
        var stages = ["Sahara", "Outdoor", "Yuma", "Do Lab", "Gobi", "Mojave", "Coachella", "Despacio"]

        for (var i = 0; i < stages.length; i++){
            // var stageName = $('.lineup-box[data-stage="' + stages[i] + '"]').first();
            // console.log("First" + stages[i] + "div", stageName);
            $('.lineup-box[data-stage="' + stages[i] + '"]').first()
                .before('<div class="filter_header col-sm-12"><h3 class="filter-header-text">' + stages[i] + '</h3></div>');
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

    // loadLineup(artistInfo, 0);
    composeSortByABC(artistInfo);
    
    $('#sort_abc').on('click', loadSortABC);
    $('#sort_by_day').on('click', loadSortByDay);
    $('#sort_by_stage').on('click', loadSortByStage);


    // function getCheckedArtists(){

    //     // var artistsArray = [];

    //     // $("input.artist_checkbox:checkbox[name=artist]:checked").each(function() {
    //     //     artistsArray.push($(this).val());
    //     // });

    //     // console.log("getCheckedArtists returns", artistsArray);
    //     // return artistsArray;
    // }


    function displayPlaylist(data){
        console.log(data);

        var topHTML = "<h3>Preview of songs on playlist</h3>" +
            "<ul id='song_preview_list'>";

        var bottomHTML = '</ul>' +
            '<form>' +
            '<p class="playlist-field"><span class="playlist-naming">Playlist name: </span>' +
            '<input id="playlist_name" type="text" name="playlist_name"></p>' +
            '<div class="generate_div">' +
            '<button id="generate_button" type="button" class="btn">' +
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
        console.log("Click!")
        event.preventDefault();
        console.log("event prevented!")
        var artistsToSubmit = artistsToAdd;
        console.log("State of artists to add:", artistsToAdd)
        console.log("Artist to Submit:", artistsToSubmit);
        if (typeof artistsToSubmit !== 'undefined' && artistsToSubmit.length > 0) {
            $.post("/preview.json", {"artists": artistsToSubmit}, displayPlaylist);
            console.log("post!");
        }
    }


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
        $('#artist_preview_list').remove();
        artistsToAdd = [];
        $('#playlist_preview').empty();
    }


    function getTrackId(){
        var trackIdArray = [];

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


    function addToArtistPreview(array, artist) {
        if (array.length === 1) {
            $(".artist_preview_table").append("<ul id='artist_preview_list'></ul>");
        }
        $("#artist_preview_list").append("<li>" + artist + "</li>");
    }


    function addToArtistArray(evt){
        var artistChecked = $(this).attr("value");

        if ($(this).is(':checked')) {
            artistsToAdd.push(artistChecked);
            console.log("artistChecked checked:", artistChecked);
            console.log("addArtistToTable checked:", artistsToAdd);
            //add to ul=artist_preview_list
            addToArtistPreview(artistsToAdd, artistChecked);
        } else {
            var index = artistsToAdd.indexOf(artistChecked);
            artistsToAdd.splice(index, 1);
            console.log("artistChecked unchecked:", artistChecked);
            console.log("addArtistToTable unchecked:", artistsToAdd);
            //remove from ul=artist_preview_list (li with artistToAdd text)
            $('li:contains(' + artistChecked + ')').remove();
        }

    }

 
    var artistsToAdd = [];

    $("#playlist_submit").on("click", submitCheckedArtists);
    $("button#playlist_clear").on("click", clearArtistsEvent);
    $("input.artist_checkbox").on("click", addToArtistArray);

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('.page-scroll a').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

});