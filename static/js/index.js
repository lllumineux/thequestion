clickedCategories = [];
chosenOBJ = 0;

function addCurrentCategory(obj){
	if (clickedCategories.indexOf(obj.innerHTML) >= 0) {
		obj.classList.remove('chosen-category');
		clickedCategories.pop(obj.innerHTML);
	}
	else {
		obj.classList.add('chosen-category');
		clickedCategories.push(obj.innerHTML);
	};
};

function searchStart(){
	nums = [...Array($('.survey-preview').length).keys()];
	nameFilter = $('.survey-name-search')[0].value;

	for (num in nums){
		$('.survey-preview')[num].style.display = 'flex';
		if (nameFilter != ''){
			if ($('.survey-preview')[num].children[0].innerHTML.toLowerCase().indexOf(nameFilter.toLowerCase()) < 0) {
				$('.survey-preview')[num].style.display = 'none';
			};
		};
		if (clickedCategories.length > 0){
			if (clickedCategories.indexOf($('.survey-preview')[num].children[1].innerHTML) < 0) {
				$('.survey-preview')[num].style.display = 'none';
			};
		};
	};
};

$('.survey-name-search').keyup(function(event){
    if(event.keyCode == 13){
        $('.category-search-submit').click();
    };
});

function choseCategory(obj){
	if (obj == chosenOBJ){
		obj.classList.remove('chosen-category');
		chosenOBJ = 0;
	}
	else {
		if (chosenOBJ != 0) {
			chosenOBJ.classList.remove('chosen-category');
		};
		obj.classList.add('chosen-category');
		chosenOBJ = obj;
	};

	$('.survey-category')[0].value = obj.innerHTML;
};

function copyLink(){
	var copytext = document.createElement('input')
	copytext.value = window.location.href
	document.body.appendChild(copytext)
	copytext.select()
	document.execCommand('copy')
	document.body.removeChild(copytext)
}