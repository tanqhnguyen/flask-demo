include_recipe "nodejs"

# install nodejs dependencies
execute "npm install -d" do
  cwd "#{node['app']['project_dir']}/public/build"
  user node[:nodejs][:user]
  group node[:nodejs][:group]
  command "#{node[:nodejs][:prefix]}/bin/npm install -d"
end

# install some global libraries for nodejs
execute "npm install -g" do
  user node[:nodejs][:user]
  group node[:nodejs][:group]
  command "#{node[:nodejs][:prefix]}/bin/npm install -g grunt-cli"
end