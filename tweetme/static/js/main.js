/* Get url Parameter By name */

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

/* Get url Parameter By name */


function loadTweetContainer(tweetContainerId){
	var query = getParameterByName('q');
	var tweetList = [];
	var nextTweetUrl;

	var initialContainer;
	if(tweetContainerId){
		initialContainer = $("#" + tweetContainerId)
	}else{
		initialContainer = $("#tweet-container");
	}

	var initialUrl = initialContainer.attr("data-url") || ("/api/tweets/");


	$(document.body).on("click",".tweet-like",function(e){
		e.preventDefault();

		var this_ = $(this);
		var tweetId = this_.attr("data-id")
		console.log(tweetId)
		var likedUrl = '/api/tweets/' + tweetId + '/like/'
		$.ajax({
			method:"GET",
			url:likedUrl,
			success: function(data){
				if (data.liked){
					this_.text('Liked');
				}else{
					this_.text('Unliked');
				}
			},
			error: function(err){
				console.log(err)
			}
		})

	});


	$(document.body).on("click",".tweet-reply",function(e) {
		e.preventDefault();
		var this_ = $(this)
		var parentId = this_.attr("data-id")
		var username = this_.attr("data-user")
		$("#replyModal").modal({})
		$("#replyModal textarea").after("<input type='hidden' value='" + parentId + "' name='parent_id' />")
    	$("#replyModal textarea").after("<input type='hidden' value='" + true + "' name='is_reply' />")
    	$("#replyModal textarea").val("@" + username + " ")
    	$("#replyModal #replyModalLabel").text("Reply to " + content)

		$("#replyModal textarea").val("@" + username + " ")
		$("#replyModal").on("shown.bs.modal",function(){
			$('textarea').focus();
		})
	});



	$(document.body).on("click",".retweetBtn",function(e) {
		e.preventDefault();
		console.log('cliked');
		var url = "/api" + $(this).attr("href");
		$.ajax({
			url: url,
			type: 'GET',
		})
		.done(function(data) {
			console.log(data);
			if(initialUrl == '/api/tweets/'){
				attachTweet(data,true,true);
				updateHashLinks();
			}

		})
		.fail(function(err) {
			console.log("error");
			console.log(err);
		})
		.always(function() {
			console.log("complete");
		});

	});

	function updateHashLinks(){
		$(".media-body").each(function(data) {
			var hashtagRegex = /(^|\s)#([\w\d-]+)/g
			var usernameRegex = /(^|\s)@([\w\d-]+)/g
			var newText = $(this).html().replace(hashtagRegex,"$1<a href='/tags/$2/'>#$2</a>")
			var newText = $(this).html().replace(usernameRegex,"$1<a href='/$2/'>@$2</a>")
			$(this).html(newText)
		});
	}


	function formatTweet(tweetValue){

		var preContent = null;
		var container;
		var is_reply = tweetValue.is_reply;
		if(tweetValue.parent && !is_reply){
			tweetValue = tweetValue.parent
			preContent = `ReTweet Via ${tweetValue.user.username} on ${tweetValue.date_display} <br/>`
		}else if(tweetValue.parent && is_reply){
			preContent = `Reply To @${tweetValue.parent.user.username}<br/>`
		}

		var verb = 'Like'
		if(tweetValue.did_like)	{
			verb = "Unlike"
		}


		var tweetContent = `${tweetValue.content}<br>
				via <a href='${tweetValue.user.url}'>${tweetValue.user.username}</a> | ${tweetValue.date_display} | ${tweetValue.timesince} | <a href="/tweets/${tweetValue.id}">View</a> | <a class='retweetBtn'  href="/tweets/${tweetValue.id}/retweet/">Retweet</a> | <a href="#" data-id=${tweetValue.id} class='tweet-like'>${verb} (${tweetValue.likes})</a> | <a href="#" data-id=${tweetValue.id} data-user=${tweetValue.user.username} class='tweet-reply'> Reply </a>`

		if(preContent){
			container = `<div class="media"><div class="media-body">${preContent} ${tweetContent}</div></div><hr/>`
		}else{
			container = `<div class="media"><div class="media-body">${tweetContent}</div></div><hr/>`
		}
		return container;
	}


	function attachTweet(tweetValue,prepend,retweet){
		var tweetFormatedHtml = formatTweet(tweetValue)
		if(prepend == true){
			initialContainer.prepend(tweetFormatedHtml)
		}else{
			initialContainer.append(tweetFormatedHtml)
		}
	}

	function parseTweets(){
		if (tweetList == 0) {
			initialContainer.text("No Tweets Found")
		}else{
			$.each(tweetList,function(key,value) {
				var tweetKey = key;
				if(value.parent){
					attachTweet(value,false,true);
				}else{
					attachTweet(value);
				}

			});
		}
	}

	function fetchTweets(url){
		var fetchUrl;
		if(!url){
			fetchUrl = initialUrl
		}else{
			fetchUrl = url
		}
		$.ajax({
		url: fetchUrl,
		data:{
			"q" : query
		},
		type: 'GET',
		})
		.done(function(data) {
			console.log("success");
			tweetList = data.results
			if(data.next){
				nextTweetUrl = data.next
			}else{
				$("#loadmore").css("display","none")
			}

			parseTweets()
			updateHashLinks()
		})
		.fail(function(err) {
			console.log(err)
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});

	}





	fetchTweets()


	$("#loadmore").click(function(e) {
		e.preventDefault();
		if(nextTweetUrl){
			fetchTweets(nextTweetUrl)
		}
	});

	var charStart = 140;
	var charCurrent = 0;
	$(".tweet-form").append(`<span class="tweetCharLeft">${charStart}</span>`)

	$(".tweet-form textarea").keyup(function(e) {
		var tweetValue = $(this).val()
		charCurrent = charStart - tweetValue.length;
		var spanChar =  $(".tweet-form").find("span.tweetCharLeft");
		spanChar.text(charCurrent)

		if(charCurrent > 0){
		 	spanChar.removeClass('gray-color');
		 	spanChar.removeClass('red-color');
		}else if (charCurrent == 0) {
			spanChar.removeClass('red-color')
			spanChar.addClass('gray-color')
		}else if (charCurrent < 0) {
			spanChar.removeClass('gray-color');
			spanChar.addClass('red-color')
		}

	});

	$(".tweet-form").submit(function(event) {
		event.preventDefault();
		formData = $(this).serialize()
		if (charCurrent >= 0){
			$.ajax({
			url: "/api/tweets/create/",
			data: formData,
			type: 'POST',
			})
			.done(function(data) {
				console.log(data)
				$('#id_content').val('');
				attachTweet(data,true);
				updateHashLinks();
				$("#replyModal").modal("hide")
			})
			.fail(function(err) {
				console.log(err.status)
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
		}else{
			$(".tweet-form").append(`Your Limit Is Over..`)
		}
	});
}


jQuery(document).ready(function($) {
	loadTweetContainer("tweet-container")
});



