include_recipe "python"

python_virtutal_dir = [node["app"]["project_dir"], 'env'].join('/')
python_virtualenv "#{python_virtutal_dir}" do
  owner node["app"]["user"]
  group node["app"]["group"]
  action :create
end

bash 'install python dependencies' do
    code <<-EOH
. #{python_virtutal_dir}/bin/activate && pip install -r #{node["app"]["project_dir"]}/requirements.txt
    EOH
end

# install gunicorn
include_recipe "gunicorn"

gunicorn_path = "#{node["app"]["project_dir"]}/gunicon.py"
gunicorn_config gunicorn_path do
  action :create
  listen node[:gunicorn][:listen]
  worker_processes node[:gunicorn][:worker_processes]
  owner node[:app][:user]
  group node[:app][:group]
  worker_class node[:gunicorn][:worker_class]
end

# supervisor
include_recipe "supervisor"
supervisor_service "vietd" do
  action :enable
  autostart true
  autorestart true
  user node[:app][:user]
  directory node[:app][:project_dir]
  command "#{python_virtutal_dir}/bin/gunicorn -c #{gunicorn_path} app:app"
  process_name "vietd"
end