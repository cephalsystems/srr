class cephal::development {
  include cephal::packages
  
  $apt_packages = [ 'emacs',
                    'puppet-el',
                    'puppet-lint',
                    'meld',
                    'terminator',
                    'htop' ]
  
  package { $apt_packages:
    ensure => 'present',
    provider => 'apt',
    require => Exec["apt-get update"],
  }

  file { '/home/cephal/.emacs.d/cephal.el':
    source => 'puppet:///modules/cephal/home/.emacs.d/cephal.el',
    ensure => 'present',
    owner => 'cephal',
    group => 'cephal',
    require => Package['emacs'],
  }

  file { '/home/cephal/.bashrc_cephal':
    source => 'puppet:///modules/cephal/home/.bashrc_cephal',
    ensure => 'present',
    owner => 'cephal',
    group => 'cephal',
  }
  ->
  file_line { 'source .bashrc_cephal':
    path => '/home/cephal/.bashrc',
    line => 'source ~/.bashrc_cephal',
    ensure => 'present',
  }
}
