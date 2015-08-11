(function($) {
    var listener = function() {
        this.warper = jQuery('#continer');
        this.link = jQuery('#count');
        this._login_el = jQuery('#login');
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
        _initilaSharingEvents :function() {
            jQuery('.sharing_button').click(function(e) {
                var el = jQuery(this);
                var url = el.attr('data-url-share');
                if (typeof url != 'undefined') {
                    FB.ui({
                          method: 'feed',
                          description: 'asdsadsa',
                          caption:'asasdasd',
                          href: url,
                    }, function(response){
                        
                    });
                }
            })
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
            if (typeof data.stats != 'undefined') {
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
            (function before () {
                self._login_el.fadeOut(1000,function() {
                    self.warper.html(jQuery('<i class="text-center fa fa-refresh  fa-5x fa-spin"></i>'))
                })
                self.warper.fadeIn(1000);
            })();        
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
        _buildTemplateHtml :function(id,data) {
            template = Handlebars.compile(jQuery(id).html());
            return template(data)
        },
        
        buildHtml:function() {
            var self = this;
            this.link.fadeOut(1000,function() {
                fields = {
                    'total':{
                        'icon':'fa fa-thumbs-o-up',
                        'title':'Total Likes',
                        'templateId':'#entry-likes-number',
                    },
                    'photos':{
                        'icon':'fa fa fa-camera',
                        'title':'Total Likes On Photos',
                        'templateId':'#entry-likes-number'
                    },
                    'posts':{
                        'icon':'fa fa-font',
                        'title':'Total Likes On Posts',
                        'templateId':'#entry-likes-number'
                    },
                    'videos':{
                        'icon':'fa fa-video-camera',
                        'title':'Total Likes On Videos',
                        'templateId':'#entry-likes-number'
                    },
                    'top_likers': {
                        'icon':'fa fa-video-camera',
                        'title':'Total Likes On Videos',
                        'templateId':'#entry-likes-list',
                    },
                    'sorted_photos':{
                        'icon':'fa fa-thumbs-o-up',
                        'title':'Total Likes',
                        'templateId':'#entry-likes-list-photos',
                    },
                    'sorted_videos':{
                        'icon':'fa fa-thumbs-o-up',
                        'title':'Total Likes',
                        'templateId':'#entry-likes-list-videos',
                    },
                    'sorted_posts':{
                        'icon':'fa fa-thumbs-o-up',
                        'title':'Total Likes',
                        'templateId':'#entry-likes-list-posts',
                    },
                };
                
                for (var field in fields) {
                    if (self.user_data.stats[field] !== undefined){
                        data = fields[field];
                        data['user_data'] = self.user_data;
                        data['value'] = self.user_data.stats[field];
                        console.log(data)
                        el = self._buildTemplateHtml(data['templateId'], data)
                        self.warper.append(el)
                    }
                }
                
                self._initilaSharingEvents();                
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
    Handlebars.registerHelper('each', function(context, profile) {
        options = arguments[arguments.length - 1];
        var ret = "";

        for(var i=0, j=context.length; i<j; i++) {
            context[i].profile = profile ;
            //context[i].created_time = new Date(context[i].created_time)
            ret = ret + options.fn(context[i]);
        }

        return ret;
    });
    Handlebars.registerHelper('posts', function(context) {
        options = arguments[arguments.length - 1];
        var ret = "";   
        for(var i=0, j=context.length; i<j; i++) {
            
            var arr = {
                'post_id' : context[i].post_id.split('_')[1],
                'user_id' : context[i].post_id.split('_')[0]
            }
            
            ret = ret + options.fn(arr);
        }
        setTimeout(function() {
            FB.XFBML.parse();
        },10);
        return ret;
    });


})(jQuery);
