packages = "g++ make"
packages.split(" ").each do |p|
  package p
end

configure_flags = {
  '--prefix' => node[:nodejs][:prefix]
}

configure = []

configure_flags.each { |k,v|
  configure << k
  configure << v
}

url = node[:nodejs][:url] % [node[:nodejs][:version], node[:nodejs][:version]]

Chef::Log.info "#{node[:nodejs][:version]} ===> #{url}"

cache_path  = Chef::Config[:file_cache_path]
nodejs_tar = File.join(cache_path, url.split("/").last)
nodejs_dir = "node-v#{node[:nodejs][:version]}"

remote_file nodejs_tar do
  source url
  action :create_if_missing
end

execute "Extract Nodejs source" do
  cwd cache_path
  command "tar xvzf #{nodejs_tar}"
  not_if { ::File.exist?(File.join(cache_path, nodejs_dir)) }
end

bash "Install Nodejs" do
  cwd File.join(Chef::Config[:file_cache_path], nodejs_dir)
  user node[:nodejs][:user]
  group node[:nodejs][:group]
  code <<-EOH
    ./configure #{configure.join(" ")} &&
    make &&
    make install
  EOH
  not_if {
    nodejs_bin = ::File.join(node[:nodejs][:prefix], 'bin', 'node')
    nodejs_present = ::File.exists?(nodejs_bin)
    nodejs_version_correct = nodejs_present

    if nodejs_present
      nodejs_version = `#{nodejs_bin} -v`
      nodejs_version = nodejs_version.split("\n")[0]
      nodejs_version_correct = nodejs_version == "v#{node[:nodejs][:version]}"      
    end

    nodejs_present && nodejs_version_correct
  }
end