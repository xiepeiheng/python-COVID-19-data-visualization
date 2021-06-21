//主页导航栏
$(function() {
  $('.page-header').each(function () {
    var $window = $(window);
    var $header = $(this);
    var headerOffsetTop = $header.offset().top;

    $window.on('scroll', function () {
      if ($window.scrollTop() > headerOffsetTop) {
        $header.addClass('sticky');
      } else {
        $header.removeClass('sticky');
      }
    });
  });
});
//侧边栏
$(function() {
  var $aside = $('.page-main');
  var $asidButton = $aside.find('button').on('click', function () {
    $aside.toggleClass('open');
    if ($aside.hasClass('open')) {
      $aside.stop(true).animate({
        left: '-70px'
      }, 300, 'swing');
      $asidButton.find('img').attr('src', 'img/btn_close.png');
    } else {
      $aside.stop(true).animate({
        left: '-350px'
      }, 300, 'swing');
      $asidButton.find('img').attr('src', 'img/btn_open.png');
    };
  });
});
//画廊
$(function(){
	$('.type3').on('click',function(){
		$('#type0 img').attr('src', this.href);
		return false;
	});
});
//提交成功
$(function(){
	$('#bg').hide();
	
	$('#click').on('click',function(){
		$('#bg').fadeIn(300);
	})
	
	$('#ok').on('click',function(){
		$('#bg').fadeOut(300);
	})
})