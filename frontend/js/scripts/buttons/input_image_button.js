$(document).ready(function () {

    $("#import_image_button").on("click", function() {
        $("#import_image_file_input").trigger("click");
    });
    $("#import_image_file_input").on('change',function(){
    	try {
        	var filepath = document.getElementById("import_image_file_input").files[0].path;
        	set_image_from_file(filepath);
    	}
    	catch (err) {
    		return
    	}
    });
});