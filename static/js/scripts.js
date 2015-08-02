(function($) {
    var listener = function() {
        this.warper = jQuery('#login');
        this.link = jQuery('#count');
        this._userId = jQuery('#fb_id').val();
        this._template = jQuery('#box-template').clone(true);
        this._init();

    }
    listener.prototype = {
        _init:function() {
            this._ajaxFinished = true;
            this.token = $('input[name=csrfmiddlewaretoken]').val();
            this.affects_before();
            this.listener();
        },
        listener:function() {
            var self = this;

            this._intervalId = setInterval(function() {
                    self.onListen();
                }, 3000);
        },
        onListen :function() {
            var self = this;
            if (this._ajaxFinished) {
                time = new Date().getTime() / 1000;
                jQuery.ajax({
                        method:'post',
                        url:'/stats/'+self._userId,
                        data: {
                                'time':time,
                                'csrfmiddlewaretoken':this.token
                            },
                        dataType:'JSON',
                        success:function(data) {
                            console.log('success');
                            self.onListenerSuccess(data);
                        },

                        beforeSend:function() {
                            self._ajaxFinished = false;
                        },

                        error:function(a,b,c) {
                            self._ajaxFinished = true;
                            console.log(a+b+c);
                        }

                });
            }
        },
        onListenerSuccess :function(data) {
            if (data) {
                clearInterval(this._intervalId);
                this.user_data = data;
                this.affects_after();
            } else {
                this._ajaxFinished = true;
            }
        },
        affects_before:function() {
            var self = this;
            this.warper.queue('before_result');
            function before () {
                self.warper.fadeOut(1000,function() {
                    self.warper.html(jQuery('<i class="text-center fa fa-refresh  fa-5x fa-spin"></i>'))
                })
                self.warper.fadeIn(1000);
            }
            before();
            
        },  
        affects_after:function() {
            var self = this;
            this.warper.queue('after_result');
            this.warper.animate({'height':'90%'},1000);
            this.warper.fadeOut(1000,function() {
                jQuery(this).html('')
                self.buildHtml()
                jQuery(this).fadeIn(1000);
            });
        },
        buildHtml:function() {
            var self = this;
            this.link.fadeOut(1000,function() {
                fields = {
                    'LIKE_COUNT':{
                        'icon':'fa fa-thumbs-o-up',
                        'title':'Total Likes'
                    },
                    'PHOTOS_COUNT':{
                        'icon':'fa fa fa-camera',
                        'title':'Total Likes On Photos'
                    },
                    'POSTS_COUNT':{
                        'icon':'fa fa-font',
                        'title':'Total Likes On Posts'
                    },
                    'VIDEOS_COUNT':{
                        'icon':'fa fa-video-camera',
                        'title':'Total Likes On Videos'
                    }
                };
                
                for (var x in fields) {
                    if (self.user_data[x] !== undefined){
                        data = fields[x];
                        a = self._template.clone();
                        a.removeClass('hidden');
                        a.find('.panel-header').html(
                            data.title)
                        a.find('.center-panel').append(
                            jQuery('<h2><i class="'+data.icon+'">'+self.user_data[x]+'</i></h2>')
                        )
                        a.find('.bottom-panel').append(
                            jQuery('')
                        )
                        a.attr('class','');
                        self.warper.append(a)
                    }
                }

                fields_tops = {
                    'top_likers':{
                        'title':'Top Likers'
                    },
                    'top_posts':{
                        'title':'Top Post'
                    },
                    'top_videos':{
                        'title':'Top Video'
                    },
                    'top_photos':{
                        'title':'Top Photo'
                    }
                    
                }
                
                for (var x in fields_tops) {

                    if (self.user_data[x] !== undefined){
                        extra_info = fields_tops[x]
                        data = self.user_data[x];
                        a = self._template.clone();
                        a.removeClass('hidden');
                        a.find('.panel-header').html(
                            extra_info.title
                            )
                        a.find('.center-panel').append(
                            jQuery(data.html)
                        )
                        a.find('.bottom-panel').append(
                            jQuery('')
                        )
                        a.attr('class','');
                        self.warper.append(a)
                    }
                }
                //FB.XFBML.parse(); 
            });


        }
    }

    jQuery(document).ready(function() {
        //events bind;
        jQuery('#count').click(function(e) {
            e.preventDefault();
            jQuery(this).attr('disabled');
            (new listener());
            return false;
        });
    });
  
    $.fn.animateNumber=function(number, _callback)
    {

        this.each(function() {
            var self = this;
            $(this).html('0');
            var timer = setInterval(function() {
                current_num = parseInt($(self).html());
                $(self).html(current_num + 1)
                if (current_num == number) {
                    console.log(typeof _callback)
                    if (typeof _callback === "function")
                        _callback();
                    clearInterval(timer);
                }
            }, 1)

        })
        return this;
    }
})(jQuery);
