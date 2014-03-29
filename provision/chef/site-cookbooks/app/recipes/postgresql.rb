require 'json'

include_recipe "postgresql::client"
include_recipe "postgresql::server"

db_config_file = [node['app']['project_dir'], 'config', 'local.json'].join('/')

file = File.read(db_config_file)
config = JSON.parse(file, :symbolize_names => true)
db_config = config[:postgres]

pg_user db_config[:username] do
  privileges :superuser => false, :createdb => false, :login => true
  password db_config[:password]
end

pg_database db_config[:database] do
  owner db_config[:username]
  encoding "utf8"
  template "template0"
  locale "en_US.UTF8"
end