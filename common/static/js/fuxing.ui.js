/*
 *
 *yanchao727@gmail.com
 *
 *2013/2/7
*/
var fuxing = fuxing || {};

fuxing.ui = {

    runSlider : function(){

            $('#slider').slidertron({
                viewerSelector: '.viewer',
                reelSelector: '.viewer .reel',
                slidesSelector: '.viewer .reel .slide',
                advanceDelay:4300,
                speed: 'slow'
            });
    }


}
