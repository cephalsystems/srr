class cephal::packages {

  # Required aptitude packages
  $apt_packages = [ # Development packages
                    'git',
                    'puppet',
                    'ssh',
                    'lm-sensors',
                    'cmake',
                    'build-essential', 
                    'ipython',
                    # Point Grey dependencies
                    'libraw1394-11',
                    'libgtk2.0-0',
                    'libgtkmm-2.4-dev',
                    'libglademm-2.4-dev',
                    'libgtkglextmm-x11-1.2-dev',
                    'libusb-1.0-0',
                    # ROS packages
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
