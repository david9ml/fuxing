/*
 * yanchao727@gmail.com
 * 15/06/2012
 *
 */

;(function($, undef) {

    $(function(){
                $('#menu_01').addClass('active');
				$('#slider').slidertron({
					viewerSelector: '.viewer',
					reelSelector: '.viewer .reel',
					slidesSelector: '.viewer .reel .slide',
					advanceDelay: 3000,
					speed: 'slow'
				});
	});
})(jQuery);
