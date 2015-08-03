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
                    }
                };
                
                for (var field in fields) {
                    if (self.user_data.stats[field] !== undefined){
                        data = fields[field];
                        data['value'] = self.user_data.stats[field];
                        el = self._buildTemplateHtml(data['templateId'],data)
                        self.warper.append(el)
                    }
                }


                fields = {
                    'photos':{
                        'icon':'fa fa-thumbs-o-up',
                        'title':'Total Likes',
                        'templateId':'#entry-likes-list-photos',
                    },
                }
                for (var field in fields) {
                    if (self.user_data[field] !== undefined){
                        data = fields[field];
                        data['value'] = self.user_data[field];
                        el = self._buildTemplateHtml(data['templateId'],data)
                        self.warper.append(el)
                    }
                }

                
                
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
    Handlebars.registerHelper('each', function(context, options) {
        var ret = "";

        for(var i=0, j=context.length; i<j; i++) {
            ret = ret + options.fn(context[i]);
        }

        return ret;
    });
})(jQuery);
