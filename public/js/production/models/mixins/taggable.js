define(["underscore.custom"],function(e){return{generateTagArray:function(){var t=this.get("tags");return e.isArray(t)?t:t.map(function(e){return e.get("name")})},setTags:function(t,n){e.isArray(n)||(n=[n]),n=e.map(n,function(e){return{name:e}}),this.get("tags").reset(n)}}});