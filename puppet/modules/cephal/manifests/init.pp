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
  
  vcsrepo { $repo_path:
    ensure => present,
    owner => 'cephal',
    group => 'cephal',
    revision => 'master',
    provider => git,
    source => $repo_uri,
  }
}
