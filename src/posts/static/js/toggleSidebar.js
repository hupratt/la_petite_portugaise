	showHideSidebar = () => {
		$('body').append('<div class="overlay-sidebar trans-0-4"></div>');
		var ovlSideBar = $('.overlay-sidebar');
		var btnShowSidebar = $('.lines-button');
		var sidebar = $('.sidebar');

		$(btnShowSidebar).on('click', function () {
			$(sidebar).addClass('show-sidebar');
			$(ovlSideBar).addClass('show-overlay-sidebar');
		})

		$(ovlSideBar).on('click', function () {
			$(sidebar).removeClass('show-sidebar');
			$(ovlSideBar).removeClass('show-overlay-sidebar');
			$(btnShowSidebar).removeClass('close');
		})
		$(document).on('click', ".lines-button", function () {
			$(btnShowSidebar).addClass('close');
		});
	}