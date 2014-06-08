class cephal::packages {

  # Required aptitude packages.
  $apt_packages = [ # Hardware support packages
                    'lm-sensors',
                    'bcmwl-kernel-source',
                    'network-manager',
                    # Development packages
                    'git',
                    'puppet',
                    'python-pip',
                    'ssh',
                    'cmake',
                    'build-essential', 
                    'ipython',
                    'yaml-mode',
                    'python-mode',
                    # Point Grey dependencies
                    'libraw1394-11',
                    'libgtk2.0-0',
                    'libgtkmm-2.4-dev',
                    'libglademm-2.4-dev',
                    'libgtkglextmm-x11-1.2-dev',
                    'libusb-1.0-0',
                    # SRC build dependencies
                    'python-dev',
                    'python-opencv',
                    # Pip dependencies
                    'libxml2-dev',
                    'libxslt1-dev',
                    'python-lxml',
                    # ROS packages
                    'ros-indigo-desktop',
                    ]

  # Required PIP packages.
  $pip_packages = [ # Linting and formatting tools
                    'pep8',
                    'autopep8',
                    # SRC build dependencies
                    'utm',
                    'pykml',
                    'flask',
                    'shapely',
                    ]

  # Install the required pip packages.
  package { $pip_packages:
    ensure   => 'present',
    provider => 'pip',
    require  => [ Package['python-pip'],
                  # PyKML dependencies
                  Package['libxml2-dev'],
                  Package['libxslt1-dev'],
                  Package['python-lxml'] ]
  }
  
  # Require the aptitude puppet module.
  class { 'apt': 
    always_apt_update => true,
  }

  # Add ROS repository before anything else.
  apt::key { 'ros':
    key        => 'B01FA116',
    key_source => 'http://packages.ros.org/ros.key',
  }
  ->
  apt::source { 'ros':
    location          => 'http://packages.ros.org/ros/ubuntu',
    release           => 'saucy',
    repos             => 'main',
    required_packages => 'debian-keyring debian-archive-keyring',
  }
  ~>
  exec { 'sudo rosdep init && rosdep update' :
    path        => [ '/usr/bin' ],
    refreshonly => true,
  }

  # Do not install recommended packages by default.
  file { "/root/.aptitude/config":
    ensure  => present,
    content => 'APT::Install-Recommends "0";',
  }
  ->
  # Trigger installation of necessary packages.
  package { $apt_packages:
    ensure   => present,
    provider => 'aptitude',
    require  => Apt::Source[ 'ros' ],
  }

  # Start network-manager service with modified permissions.
  file { '/etc/dbus-1/system.d/org.freedesktop.NetworkManager.conf':
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    source  => 'puppet:///modules/cephal/etc/dbus-1/system.d/org.freedesktop.NetworkManager.conf',
    require => Package['network-manager'],
  }
  -> 
  service { 'network-manager':
    enable  => true,
    ensure  => 'running',
  }
}
