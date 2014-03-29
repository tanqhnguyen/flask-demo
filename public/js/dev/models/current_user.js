define([
  'models/user'
], function(User){
  return new User(window.appData.user);
});