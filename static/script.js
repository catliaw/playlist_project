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

        // var artistsObject = {"artists[]": artistsAdded};
        // console.log("artistsObject", artistsObject);

        $.post("/preview.json", {"artists": artistsAdded}, displayPlaylist);
    }


    function displayPlaylist(data){
        console.log(data);

        $("#playlist_preview").append("<ul>");

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
        $("#playlist_preview").append("</ul>");
    }


    $("#playlist_submit").on("submit", submitCheckedArtists);

});