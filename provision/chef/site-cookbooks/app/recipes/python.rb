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