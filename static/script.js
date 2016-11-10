$(function(){

    function getCheckedArtists(){

        var artistsArray = [];

        $("input.artist_checkbox:checkbox[name=artist]:checked").each(function() {
            artistsArray.push($(this).val());
        });

        console.log("getCheckedArtists returns", artistsArray);
        return artistsArray;
    }


    function submitCheckedArtists(event){
        event.preventDefault();
        
        var artistsAdded = getCheckedArtists();
        console.log("artistsAdded", artistsAdded);

        var artistsObject = {'artists': artistsAdded};
        console.log("artistsObject", artistsObject);

        $.get("/preview", artistsObject, displayPlaylist);
    }


    function displayPlaylist(data){
        console.log(data);
    }


    $("#playlist_submit").on("submit", submitCheckedArtists);

});