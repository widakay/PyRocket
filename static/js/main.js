$(document).ready(function(){
	//save root
	var root = '<?php echo ROOT; ?>';

	//------------------------
	//  Responsive Text
	//------------------------
	//var origwidth = $(window).width();
	var origwidth = 1265;
	$(".resp").each(function(){
		$(this).attr("fontsizeratio", $(this).css("font-size").substring(0, $(this).css("font-size").length - 2) / origwidth);
	});
	var resizeText = function(){
		//$(".header").textfill();
		$(".resp").each(function(){
			$(this).css("font-size", ($(this).attr("fontsizeratio") * $(window).width()) + "px");
		});
	}
	resizeText();
	$(window).resize(resizeText);
	
	
	//------------------------
	//   Background Parallax
	//------------------------
	/*var positionBackground = function(){
		var offset =  $(window).scrollTop();
		if (offset > 0 && offset < $(window).height()) {
			$(document.body).css("background-position", "0 " + (-0.3 * offset) + "px");
		}
	}
	positionBackground();
	$(window).scroll(positionBackground);
	
	*/
	//------------------------
	//   Rocket Animation
	//------------------------
	$("#rocket").click(function(){
		var top1 = 0;
		var left1 = 0;
		var velocity = 0.001  * (1.05^50);
		var flying = false;
		var intid = setInterval(function(){
			var top = parseFloat($("#rocket").css("top").substring(0, $("#rocket").css("top").length - 2)) - top1;
			var left = parseFloat($("#rocket").css("left").substring(0, $("#rocket").css("left").length - 2)) - left1;
			top1 = Math.floor((Math.random() * 5) - 2);
			left1 = Math.floor((Math.random() * 5) - 2);
			if (flying) {
				top1 /= 2;
				left1 /= 2;
			}
			$("#rocket").css("top", (top + top1) + "px")
						.css("left", (left + left1) + "px");
		}, 10);
		setTimeout(function(){
			var intid2 = setInterval(function(){
				flying = true;
				$("#rocket").css("top", (parseFloat($("#rocket").css("top").substring(0, $("#rocket").css("top").length - 2)) - velocity) + "px")
							.css("left", (parseFloat($("#rocket").css("left").substring(0, $("#rocket").css("left").length - 2)) + velocity) + "px");
				velocity *= 1.05;
			}, 10);
			setTimeout(function(){
				clearInterval(intid);
				clearInterval(intid2);
				flying = false;
				$("#rocket").hide()
							.css("top", "11%")
							.css("left", "7%")
							.fadeIn();
			}, 3000);
		}, 500);
	});
});