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