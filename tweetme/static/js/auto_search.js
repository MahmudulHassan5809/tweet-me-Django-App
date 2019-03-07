jQuery(document).ready(function($) {
	var typingTimer;
	var doneIterval = 500;
	var searchInput = $("#navbar-search-form input[type=text]");
	var searchQuery;

	searchInput.keyup(function(e) {
		searchQuery = $(this).val()
		clearTimeout(typingTimer)
		typingTimer = setTimeout(doneSearchTyping,doneIterval)
	});

	searchInput.keydown(function(e) {
		clearTimeout(typingTimer)
	});

	function doneSearchTyping(){
		if(searchQuery){
			var url = '/tweets/search/?q=' + searchQuery
			document.location.href = url
		}
	}

});
