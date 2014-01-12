class cephal {
  include cephal::users
  include cephal::packages

  # Add a nice message to the login prompt
  file { '/etc/motd.tail' :
    source => 'puppet:///modules/cephal/etc/motd.tail',
    owner => "root",
    group => "root",
    mode => "644",
  }

  # Clone the SRC software
  $repo_path = '/opt/cephal'
  $repo_uri = 'git@github.com:psigen/src.git'

  file { '/etc/ssh/ssh_known_hosts':
    ensure => 'present',
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
  }
  ->  
  sshkey { 'github.com':
    ensure => 'present',
    type   => 'ssh-rsa',
    key    => 'AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==',
  }
  ->
  vcsrepo { $repo_path:
    ensure => present,
    owner => 'cephal',
    group => 'cephal',
    revision => 'master',
    provider => git,
    source => $repo_uri,
  }
}
