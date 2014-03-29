base_path = Dir.pwd

cookbook_path [
  [base_path, "cookbooks"].join("/"),
  [base_path, "site-cookbooks"].join("/") 
]
node_path [base_path, "nodes"].join("/")
role_path [base_path, "roles"].join("/")
data_bag_path [base_path, "data_bags"].join("/")
log_level :info
verbose_logging true