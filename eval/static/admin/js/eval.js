/**
 * Created by reedd on 6/14/17.
 */
// Fancier version https://gist.github.com/985283

/* collapse filter lists in admin listview */
;(function($){ $(document).ready(function(){
    $('#changelist-filter').children('h3').each(function(){
        var $title = $(this);
        $title.click(function(){
            $title.next().slideToggle();
        });
    });
  });
})(django.jQuery);