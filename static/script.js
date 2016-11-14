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

        $("#playlist_preview").html("<h3>Playlist Preview</h3><ol>");

        for (var key in data){
            if (data.hasOwnProperty(key)) {

                console.log(key + " - " + data[key]);

                for (var innerKey in data[key]) {
                    if (data[key].hasOwnProperty(innerKey)) {

                        console.log(innerKey + " - " + data[key][innerKey]);

                        $('#playlist_preview').append('<li data-trackid="' + data[key][innerKey] +'">' + key + ' - ' + innerKey + '</li>');
                    }
                }
            }
        }
        $("#playlist_preview").append("</ol>");
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

});