include_recipe "nginx"

# setup the correct nginx site
template "#{node['nginx']['dir']}/sites-enabled/default" do
  source "nginx/default-site.erb"
  owner "root"
  group "root"
  mode 00644
  notifies :reload, 'service[nginx]'
end