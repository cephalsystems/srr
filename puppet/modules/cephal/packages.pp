class cephal::packages {
  # Require the aptitude puppet module
  class { apt: }

  # Install necessary aptitude packages
  $apt_packages = [ 'git',
                    'puppet',
                    'ssh',
                    'lm-sensors',
                    'lcdproc',
                    'cmake',
                    'build-essential', ]
  
  # Trigger installation of necessary packages
  package { $apt_packages:
    ensure => latest,
    provider => 'apt',
    require => [ Exec["apt-get update"],
                 Apt::Ppa[ "ppa:chris-lea/node.js" ],
                 Apt::Ppa[ "ppa:chris-lea/redis-server" ], ]
  }

  # Run apt-get update only when /etc/apt/ changes
  # https://blog.kumina.nl/2010/11/puppet-tipstricks-running-apt-get-update-only-when-needed/
  exec { "apt-get update":
    command => "/usr/bin/apt-get update",
    onlyif => "/bin/sh -c '[ ! -f /var/cache/apt/pkgcache.bin ] || /usr/bin/find /etc/apt/* -cnewer /var/cache/apt/pkgcache.bin | /bin/grep . > /dev/null'",
  }
}
