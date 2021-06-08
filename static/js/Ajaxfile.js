$(document).ready(function() {

	$('#form1').on('submit', function(event) {
		$('.loader').css('display', 'block');
		$.ajax({
			data : {
				name : $('#input1').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			$('.loader').css('display', 'none');
			if (data.error) {
				
				$('#Reviews').text(data.error).show();
			}
			else {
				var u=data.imgurl;
				var v=data.productTitle;
				if(u.localeCompare("NA")){
					$("#imageinfo").text("");
					$('.display2').css('background-image', 'url(' + u + ')');
				}
				else{
					$("#imageinfo").text("Image Unavailable").show();
				}
				if(v.localeCompare("NA")){
					$("#infoinfo").text(v);
					
				}
				else{
					$("#infoinfo").text("No Information Unavailable").show();
				}
				$('.display2').css("display","block");
				$('.display3').css("display","block");
				$('#form2').css("display","block");
				$('#change1').text("No. of Available Reviews: ")
				$('#Reviews').text(data.name).show();
				$('#form2').css("display","block");
			}

		});

		event.preventDefault();

	});

	$('#form2').on('submit', function(event) {
		$.ajax({
			data : {
				name : $('#input2').val()
			},
			type : 'POST',
			url : '/final'
		})
		.done(function(data) {
			if (data.error) {
				$('#result').text(data.error).show();
			}
			else {
				$("#calculating").text("Result is Calculated....Shown Below").show();
				$('#rev').text(data.R).show();
				$('#rat').text(data.name).show();
				$('#result').css("display","block");
				$('#suggestion').css('display','block');
			}

		});

		event.preventDefault();

	});

});
