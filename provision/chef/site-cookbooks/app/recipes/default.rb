#
# Cookbook Name:: app
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
#

include_recipe "apt"
include_recipe "build-essential"
include_recipe "app::basic"

include_recipe "app::python"
include_recipe "app::nginx"
include_recipe "app::redis"