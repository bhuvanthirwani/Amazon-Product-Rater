var processed_percentage=0;
var animate;
const myProgressBar = document.querySelector(".progress");
var isprocessing=false;
function updateProgressBar(progressBar, value,z)
{	
	//isprocessing=false;
	value = Math.round(value);
	if(value==0){
		$("#calculating").text("Processing....");
	}
	progressBar.querySelector(".progress__fill").style.width = `${value}%`;
	if(processed_percentage<=100)
	{
		progressBar.querySelector(".progress__text").textContent = `${value}%`;
		processed_percentage=processed_percentage+1;
	}
	else{
		if(isprocessing==false){
			isprocessing=true;
			var m="Result is Calculated....Shown Below";
			if($("#calculating").text().localeCompare(m)!=0)
			{$("#calculating").text("Calculating Results....").show();}
		}
	}
	animate = setTimeout(function() {updateProgressBar(myProgressBar, processed_percentage,z); },z);
}




$("#button1").on("click",function(){
	$('#calculating').text("Processing....")
	$('.display2').css("display","none");
	$('.display3').css("display","none");
	$("#infoinfo").text("");
	$('#change1').text("");
	$("#Reviews").text("");
	$('#suggestion').css('display','none');
	$('#form2').css("display","none");
	if(($("#display1").css("display")=="none"))
	{
		$("#display1").slideDown(1000);
	}
	else
	{	
		$('.display2').css('background-image', 'url("")');
		$("#imageinfo").css("display","none");
		$("#result").css("display","none");
		clearTimeout(animate);
		$(".progress__fill").css("width","0%");
		$(".progress__text").val("0%");
		processed_percentage=0;
		$("#display1").slideUp(100);
		$("#display1").slideDown(1000);
		$("#processing").slideUp(100);
		$(".progress").slideUp(100);
	}
	
})

$("#button2").on("click",function(){
	isprocessing=false;
	$('#suggestion').css('display','none');
	processed_percentage=0;
	var R=document.getElementById("input2").value;
	if(R%10==0){
		x=R/10;
	}  
	else{
		x=Math.floor(R/10)+1;
	}
	z=(x/100)*1000;
	z=z*2.5;
	if(($("#processing").css("display")=="none"))
	{
		$("#processing").slideDown(1000);
		$(".progress").slideDown(1000,function(){
			updateProgressBar(myProgressBar, processed_percentage, z);
		});
	}
	else
	{	
		clearTimeout(animate);
		$(".progress__fill").css("width","0%");
		$(".progress__text").val("0%");
		processed_percentage=0;
		$("#processing").slideUp(100);
		$("#processing").slideDown(1000);
		$(".progress").slideUp(100);
		$(".progress").slideDown(1000);
		updateProgressBar(myProgressBar, processed_percentage,z);
	}
	$("#result").css("display","none");
})
