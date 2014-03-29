# default[:build_essential][:compiletime] = true
# default[:apt][:compiletime] = true

# default[:python][:install_method] = 'package'
# default[:python][:prefix_dir] = '/usr'
# default[:python][:binary] = '/usr/bin/python'
# default[:python][:url] = 'http://www.python.org/ftp/python'
# default[:python][:version] = '2.7.5'
# default[:python][:checksum] = '3b477554864e616a041ee4d7cef9849751770bc7c39adaf78a94ea145c488059'
# default[:python][:configure_options] = %W{--prefix=/usr}
# default[:python][:setuptools_script_url] = 'https://bitbucket.org/pypa/setuptools/raw/0.8/ez_setup.py'
# default[:python][:pip_script_url] = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'

# default[:postgresql][:apt_distribution] = 'precise'
# default[:postgresql][:version] = '9.3'

# default[:sphinx][:version] = '2.1.6'
# default[:sphinx][:use_postgres] = true

default[:app][:project_dir] = '/home/vietd/vietd'
default[:app][:user] = 'vietd'
default[:app][:group] = 'vietd'