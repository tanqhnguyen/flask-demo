# install sphinx
require 'json'

db_config_file = [node['app']['project_dir'], 'config', 'local.json'].join('/')

file = File.read(db_config_file)
config = JSON.parse(file, :symbolize_names => true)
db_config = config[:postgres]

if node[:sphinx][:user] != 'root' and node[:sphinx][:group] != 'root'
  group node[:sphinx][:group] do
    action :create
  end

  user node[:sphinx][:user] do
    gid node[:sphinx][:group]
    system true
  end
end

include_recipe "sphinx"
config_file = "#{node[:sphinx][:source][:install_path]}/sphinx.conf"
template config_file do
  source "sphinx/sphinx.conf.erb"
  owner node[:sphinx][:user]
  group node[:sphinx][:group]
  mode 00644
  variables({
    :db_config => db_config
  })
end

sphinx_dirs = []

log_dir = node[:sphinx][:searchd][:log].split('/')
log_dir.pop()
sphinx_dirs << log_dir.join("/")

# data dir

sphinx_dirs << '/var/data'

# pid dir
pid_dir = node[:sphinx][:searchd][:pid_file].split('/')
pid_dir.pop()
pid_dir = pid_dir.join('/')
sphinx_dirs << pid_dir

sphinx_dirs.each do |dir|
  directory dir do
    action :create
    group node[:sphinx][:group]
    user node[:sphinx][:user]
  end
end

# init script
template "/etc/init.d/sphinxsearch" do
  source "sphinx/sphinx.init.erb"
  owner "root"
  group "root"
  mode 00755
  variables({
    :log_dir => log_dir.join("/"),
    :config_file => config_file
  })
end

service "sphinxsearch" do
  supports :status => true, :restart => true, :reload => true
  action :enable
end

cron "sphinxsearch_indexer" do
  action :create
  minute "0"
  user node[:sphinx][:user]
  command "#{node[:sphinx][:source][:install_path]}/bin/indexer --all --rotate --config #{config_file}"
end