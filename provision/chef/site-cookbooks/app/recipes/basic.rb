include_recipe "ulimit"

packages = "sqlite3 gettext libpq-dev python-dev"
packages.split(" ").each do |p|
  package p
end

# setup profile
template "/home/#{node[:app][:user]}/.profile" do
  source "profile.erb"
  owner node[:app][:user]
  group node[:app][:group]
  mode 00644
end

user_ulimit "www-data" do
  filehandle_limit 65535
  filehandle_soft_limit 65535
  filehandle_hard_limit 65535
end

user_ulimit node[:app][:user] do
  filehandle_limit 65535
  filehandle_soft_limit 65535
  filehandle_hard_limit 65535
end