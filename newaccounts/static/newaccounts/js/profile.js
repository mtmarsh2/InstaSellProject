$('.upload_sellpost_button').click(function(e) {
	$('.span9').prepend("<div class = 'transparencydiv'></div>");
	//make form appear
	$('.form_modal').css('display', 'inline-flex');
	var width = $(window).outerWidth() / 2;
	var height = $(window).outerHeight() / 2;
	width = width - $('.form_modal').parent().width()/2;
	$('.form_modal').css('left', width);
	height = $('.form_modal').parent().height();
	$('.form_modal').css('top', 100);

	//add closing x image
	var closing_image_x = $('.form_modal').position().left + $('.form_modal').width();
	var closing_image_y = $('.form_modal').parent().height();
	
	$('.span9').append("<img class = 'close_modal' src = '/static/images/close_modal.png' />");

	closing_image_y = 100 - $('.close_modal').height()/2;
	$('.close_modal').css('left', closing_image_x);
	$('.close_modal').css('top', closing_image_y);

});

$(document).on('click', '.close_modal', function() {
	$('.form_modal').css('display', 'none');
	$('.transparencydiv').remove()
	$('.close_modal').css('display', 'none');
});

$(document).on('click', '.transparencydiv', function() {
	$('.form_modal').css('display', 'none');
	$('.transparencydiv').remove()
	$('.close_modal').css('display', 'none');
});

function get_csrf_token(){
	return $("input[name='csrfmiddlewaretoken']").val();
}


//submit sellpost through modal
$('.form_modal').submit(function(e) {
	e.preventDefault();
	var title = $('#id_title').val()
	var description = $('#id_description').val()
	//grab image_path from side image
	var image_path = $('#image_ajax_container img').attr('src')
	var tags =  $('#id_tags').val()
	$.ajax({
		type:"POST",
		url:("/accounts/uploadsellpostture/"),
		enctype: 'multipart/form-data',
		data: {
			title: title,
			description: description,
			image_path : image_path,
			tags : tags
		},
		success: function() {
			console.log("Dormpic was rated");
		},
		error: function(xhr, ajax_options, errorthrown) {
			var errorjson = jQuery.parseJSON(xhr.responseText);
			for (key in errorjson) {
				$('#id_' + key).after('<p class = "form_error">' + errorjson[key] + '</p>');
			}
		}
	}).fail( function(d) {
		console.log("This is the fail function" + d);
	});
});

//once user chooses image in modal, have it appear next to the form
$(".form_modal :input[type*='file']").change( function(e) {
	var file = e.orginalEvent.srcElement.files[0];
	var image = $(".form_modal img");
	var reader = new FileReader();
	reader.onloadend = function() {
		image.src = reader.result;
	}
	reader.readAsDataURL(file);
});


//adds image_path returned through ajax to make the user's image appear on the page
function add_image_to_page(path_to_image) {
	var img = new Image()
	$(img).load(function() {
		$('#image_ajax_container').append($(this));
		//add button to container for user to delete picture and select another after
		var delete_button = '<button type = "button" class = "btn btn-danger" id = "delete_ajax_picture">Delete Picture</button>'
		$('#image_ajax_container').append('<div id = "delete_ajax_button_container">' + delete_button + '</div>');
	}).attr({
		src:path_to_image
	}).error(function() {
		console.log('error happened');
	})
	console.log("Reached")
	
	//var image = $(".form_modal img");
}

//removes img + button from container once user clicks the delete button
function remove_ajax_container_content() {
	$('#image_ajax_container').children().remove();
	
}

//once user clicks, have image be deleted from html
$(document).on('click', '#delete_ajax_picture', function()  {
	remove_ajax_container_content()
})

