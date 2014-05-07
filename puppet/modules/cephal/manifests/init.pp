class cephal {
  include cephal::users
  include cephal::packages

  # Add a nice message to the login prompt.
  file { '/etc/motd.tail' :
    source => 'puppet:///modules/cephal/etc/motd.tail',
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
  }

  # Set up static IP on wired ethernet device.
  file { '/etc/network/interfaces':
    source => 'puppet:///modules/cephal/etc/network/interfaces',
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
  }

  # Replicate wireless hotspot profile.
  file { '/etc/NetworkManager/system-connections/Hotspot':
    source  => 'puppet:///modules/cephal/etc/NetworkManager/system-connections/Hotspot',
    owner   => 'root',
    group   => 'root',
    mode    => '0600',
    require => Package['network-manager']
  }
  ~>
  # Start up wireless hotstop.
  exec { 'start-wireless-hotspot':
    path    => [ '/usr/bin', '/usr/sbin' ],
    command => 'nmcli con up id Hotspot'
  }
  
  # Clone the SRC software.
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
  
  # Create symlinks to Roboclaw USB devices.
  # Roboclaw for drivetrain.
  file { '/dev/roboclaw_drive':
    ensure => 'link',
    target => '/dev/serial/by-path/pci-0000:00:14.0-usb-0:4:1.0',
  }
  # Roboclaw for rake mechanism.
  file { '/dev/roboclaw_rake':
    ensure => 'link',
    target => '/dev/serial/by-path/pci-0000:04:00.0-usb-0:1:1.0',
  }
  # Roboclaw for bagging mechanism.
  file { '/dev/roboclaw_bag':
    ensure => 'link',
    target => '/dev/serial/by-path/pci-0000:04:00.0-usb-0:2:1.0',
  }
}
