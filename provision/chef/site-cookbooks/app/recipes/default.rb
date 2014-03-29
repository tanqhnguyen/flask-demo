#
# Cookbook Name:: app
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
#
packages = "sqlite3 gettext libpq-dev python-dev"
packages.split(" ").each do |p|
  package p
end

include_recipe "apt"
include_recipe "build-essential"

include_recipe "app::python"
include_recipe "app::nginx"
include_recipe "app::postgresql"
include_recipe "app::sphinx"
include_recipe "app::redis"

include_recipe "app::nodejs"

# setup profile
template "/home/#{node[:app][:user]}/.profile" do
  source "profile.erb"
  owner node[:app][:user]
  group node[:app][:group]
  mode 00644
end