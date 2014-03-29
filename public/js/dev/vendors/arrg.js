(function (root, factory) {
  if (typeof exports === 'object') {
    module.exports = factory();
  } else if (typeof define === 'function' && define.amd) {
    define([], factory);
  }
}(this, function () {

  var arrg = function(args, argNames, defaultArgs) {
    "use strict";
  
    // borrow some stuff from underscore
    var ArrayProto = Array.prototype;
    var nativeForEach = ArrayProto.forEach;
    var nativeIsArray = ArrayProto.isArray;
    var slice = ArrayProto.slice;
    var _each = function(obj, iterator, context) {
      if (obj == null) return;
      if (nativeForEach && obj.forEach === nativeForEach) {
        obj.forEach(iterator, context);
      } else if (obj.length === +obj.length) {
        for (var i = 0, l = obj.length; i < l; i++) {
          if (iterator.call(context, obj[i], i, obj) === breaker) return;
        }
      } else {
        for (var key in obj) {
          if (_.has(obj, key)) {
            if (iterator.call(context, obj[key], key, obj) === breaker) return;
          }
        }
      }
    };
  
    var _defaults = function(obj) {
      _each(slice.call(arguments, 1), function(source) {
        if (source) {
          for (var prop in source) {
            if (obj[prop] == null) obj[prop] = source[prop];
          }
        }
      });
      return obj;
    };
  
    var _isArray = nativeIsArray || function(obj) {
      return toString.call(obj) == '[object Array]';
    };
  
    var _isObject = function(obj) {
      return obj === Object(obj);
    };
  
    // now start the real thing
    args = slice.apply(args);
    var realArgs = {};
    var returnArgs = {};
    defaultArgs = defaultArgs || {};
  
    if (args.length == 1) {
      var arg = args[0];
  
      if (_isArray(arg)) {
        // turn the first and only array param into usable stuff
        realArgs = [arg];
      } else if (arg.jquery) {
        // keep jquery param as it is
        realArgs = [arg];
      } else if (_isObject(arg)) {
        // if the first and only param is an object return
        return _defaults(arg, defaultArgs);      
      } else {
        // everything else
        realArgs = [arg];
      }
  
    } else if (args.length === 0) {
      // defaults
      return defaultArgs;
    }
  
    _each(args, function(arg, index){
      returnArgs[argNames[index]] = arg;
    }); 
  
    return _defaults(returnArgs, defaultArgs);
  };
  return arrg;

}));