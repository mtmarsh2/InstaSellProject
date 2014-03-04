/*  Global Variables List */
var sellposttitles = sellposttitles;
var sellposturls = sellposturls;
var sellpostratings = sellpostratings;
var sellposttags =sellposttags;
var mediaurl = "/static/media"


$("body").onload = start();


function start() {
	load_rating_html()
}

//loads proper stars for each sellpost
function load_rating_html() {
	//grab all rating container divs and find each sellpost's respective rating
	var rating_container_list = $('.starratings')
	var current_star_type = ""
	for (var i = 0; i < rating_container_list.length; i++) {
		var rating_amount = $(rating_container_list[i]).children('.ratingnum').html();
		for(var k = 0; k < 5; k++) {
			if(rating_amount > 0) {
					//add full star
					current_star_type = "&#9733";
				}
				else {
					//add empty star type
					current_star_type = "☆";
				}
			rating_amount =  rating_amount - 1;
			$(rating_container_list[i]).append("<span class='stars'>" + current_star_type + "</span>");
		}
		
	}
}

//takes paths to thumbnails of images and adds proper bootstrap divs along with images themselves to 'containter' in body
function load_sellposttures() {

	//grab the larger span column of the first row, since this is what we will be appending to, not container
	var targetdiv = $('.span10:first');

	for(var i = 0; i < sellposturls.length; i=i+3) {
		//add row div to body
		var newrow = "<div class='row sellpostrow' id='row" + i + "'>" ;
		targetdiv.append(newrow);
		for(var j = 0; j < 3; j++) {
			if((i + j) >= sellposturls.length) {
				//index out of bounds
				break;
			}
			//add column div to row
			var newcolumn = "<div class='span3' id='column" + j + "'>" ;
			$("#row" + i).append(newcolumn);

			//add image div to column
			//*DORM IMAGE SECTION
			//link image, we need to strip the thumbnails extension so the path is just the path to the image on the filesystem
			var image_html = "<a href='" + "/" +  sellposturls[i+j].split("/")[5] + "/sellposttures" + "'>";
			var image = "<img src='" + sellposturls[i+j] + "'>" + "</div>";
			image_html = image_html.concat(image, "</a>");
			$($("#row" + i).children()[j]).append(image_html);




			//add image info to same column
			var sellpostinfohtml = "<div class='sellpostinfocontainer'>";			

			//add image title
			var imagetitle = "<h4 class='sellposttitle'>" + sellposttitles[i+j] + "</h4>";
			sellpostinfohtml = sellpostinfohtml.concat(imagetitle);

			//*SELLPOST TAGS SECTION
			var imagetagshtml = "<div class='sellposttagcontainer'>"

			//start adding tags
			var tags_html = "<h5>Tags:</h5>";
			for(var k = 0; k < sellposttags[i+j].length; k++ ) {
				var tag_html = "<p>" + " " + sellposttags[i+j][k] + "," + "</p>"
				tags_html = tags_html.concat(tag_html);
			}

			//*END DORM TAGS SECTION
			imagetagshtml = imagetagshtml.concat(tags_html, "</div>");

			



			//*RATINGS SECTION
			//add ratings
			//add specific type of star depending on amount passed in through sellpostratings element
			var ratings_html = "";
			var current_star_type = "";
			//add rating container tag for stars
			var ratings_div_html = "<div id='starratings'>"
			var rating = Math.round(sellpostratings[i+j]);
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
			

			//*END DORM IMAGE INFO CONTAINER
			sellpostinfohtml =sellpostinfohtml.concat(imagetagshtml ,ratings_div_html, "</div");
			$($("#row" + i).children()[j]).append(sellpostinfohtml);
			
			$($("#row" + i).children()[j]).append("</div>");



		}
		targetdiv.append(" </div>");
		
	}

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

