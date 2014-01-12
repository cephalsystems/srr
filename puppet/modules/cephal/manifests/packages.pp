class cephal::packages {

  # Required aptitude packages
  $apt_packages = [ 'git',
                    'puppet',
                    'ssh',
                    'lm-sensors',
                    'cmake',
                    'build-essential', 
                    'ros-hydro-desktop-full', ]

  # Require the aptitude puppet module
  class { 'apt': 
    always_apt_update => true,
  }

  # Add ROS repository before anything else
  apt::key { 'ros':
    key        => 'B01FA116',
    key_source => 'http://packages.ros.org/ros.key',
  }
  ->
  apt::source { 'ros':
    location          => 'http://packages.ros.org/ros/ubuntu',
    release           => 'raring',
    repos             => 'main',
    required_packages => 'debian-keyring debian-archive-keyring',
  }
  ~>
  exec { 'sudo rosdep init && rosdep update' :
    path        => ["/usr/bin"],
    refreshonly => true
  }
  
  # Trigger installation of necessary packages
  package { $apt_packages:
    ensure => latest,
    provider => 'apt',
    require => Apt::Source[ 'ros' ],
  }
}
