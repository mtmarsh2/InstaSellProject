$("body").onload = start();
var shouldChange = true;

function start() {
	load_disqus();
	load_rating_html()
	
}

//loads proper stars for each sellpost
function load_rating_html() {
	//grab all rating container divs and find each sellpost's respective rating
	var rating_container_list = $('.starratings')
	var current_star_type = ""
	for (var i = 0; i < rating_container_list.length; i++) {
		var rating_amount = $(rating_container_list[i]).children('.ratingnum').html();
		for(var k = 1; k <= 5; k++) {
			if(rating_amount > 0) {
					//add full star
					current_star_type = "&#9733";
				}
				else {
					//add empty star type
					current_star_type = "☆";
				}
			rating_amount =  rating_amount - 1;
			$(rating_container_list[i]).append("<span class='stars' id = 'stars" + k + "'>" + current_star_type + "</span>");
		}
		
	}
}



function get_csrf_token(){
	return $("input[name='csrfmiddlewaretoken']").val();
}

//loads main dorm pictue
function load_sellpostture() {
	//grab the larger span column of the first row, since this is what we will be appending to, not container
	var targetdiv = $('.span10:first');

	//*INFO CONTAINER

	var info_container_html = "<div class='individualimagecontainer'>";

	//add title
	info_container_html = info_container_html.concat("<p> Title: " + sellpostinfo['title'] + "</p>");

	//add username 
	info_container_html = info_container_html.concat("<p> User: " + sellpostinfo['username'] + "</p>");

	//add description
	info_container_html = info_container_html.concat("<p> Description: " + sellpostinfo['description'] + "</p>");

	//add tags
	var tag_html = "<p> Tags:";
	for(var i = 0; i < sellpostinfo['tags'].length; i++) {
		tag_html = tag_html.concat(" " + sellpostinfo['tags'][i]);
	}
	info_container_html = info_container_html.concat(tag_html);

	//add ratings
	var ratings_html = "";
	var current_star_type = "";
			//add rating container tag for stars
			var ratings_div_html = "<div id='starratings'>"
			var rating = Math.round(sellpostinfo['ratings']);
			for(var k = 1; k <= 5; k++) {
				if(rating>0) {
					//add full star
					current_star_type = "&#9733";
				}
				else {
					//add empty star type
					current_star_type = "☆";
				}
				rating = rating - 1;
				//get star html
				var starr_html = load_star_html(k, current_star_type);
				var ratings_html = starr_html;
				//add full star html to div
				ratings_div_html = ratings_div_html.concat(ratings_html);
				//clear ratings_html for next iteration
			}
			//add closing div tag for ratings container for stars
			//*END RATINGS SECTION
			ratings_div_html= ratings_div_html.concat("</div>");
			info_container_html = info_container_html.concat(ratings_div_html);

	//*END OF INFO CONTAINER
	targetdiv.append(info_container_html);


	//*END INFO CONTAINER

	//make container div for image
	var image_full_html = "<div class='individualimage'>";

	//link image to full size image on filesystem
	image_full_html = image_full_html.concat("<a href='" + sellpostinfo['full_url'] + "'>");

	//add image tag
	var image_html = "<img src='" + sellpostinfo['full_url'] + "'/>";

	//add and close image html and container div
	image_full_html = image_full_html.concat(image_html, "</div>", "</div>");

	targetdiv.append(image_full_html);
}

//takes in sellpost index and returns proper html for star ratings div
function load_star_html(index, star_type) {
	var star_html = ""
	//add star
	star_html = "<span class='stars' id='stars" + index + "''>"
	//add star type
	star_html = star_html.concat(star_type)
	//add end of span tag
	star_html = star_html.concat("</span>")
	return star_html
}

$('.stars').click(function() {
	//ajax stuff
	shouldChange = false;
	//change this so that if user sends multiple requests, it will be right
	var rating = $(this).attr('id')[5];
	$.ajax({
		type:"POST",
		url:("/rate/images/"),
		dataType: 'json',
		data: {
			value: rating,
			image: $('#sellpost_image').attr('src'),
			csrfmiddlewaretoken: get_csrf_token(),
		},
		success: function() {
			$('.ratingnum').html(rating);
		}


	});
});

$('.stars').hover(function() {
	//find value of current star thats selected
	var index = $(this).attr('id')[5];
	//change all stars left and including the current star to be full
	for(var i = 1; i <= index; i++) {
		$('#stars' + i).html("&#9733");
	}
	for( ; i <=5; i++) {
		$('#stars' + i).html("&#9734");
	}
},
	function() {
		if(shouldChange) {
			//find value of current star thats selected
			var rating_container_list = $('.starratings')
			var current_star_type = ""
			var rating_amount = parseInt($(rating_container_list).children('.ratingnum').html());
			var index = $(this).attr('id')[5];
			for(var i = rating_amount + 1; i <= index; i++) {
			$('#stars' + i).html("☆");
			}
		}
		shouldChange = true;
	}
);

//loads disqus comments underneath picture 
function load_disqus() {
	$('.span9:first').append("<div id='disqus_thread'></div>");
}
