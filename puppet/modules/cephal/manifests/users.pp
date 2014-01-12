class cephal::users {
  user { 'cephal':
    home => '/home/cephal',
    shell => '/bin/bash',
    uid => '1000',
    gid => '1000',
    comment => 'Cephal Systems,,,',
    groups => [ 'cephal', 'adm', 'cdrom', 'sudo',
                'dip', 'plugdev', 'lpadmin', 'sambashare' ],
    ensure => 'present',
    managehome => true,
    password => '$6$M4O5bCCj$GJMeeP6GVXHlnIbWxgw6TAvOxOtXtjn5XqK1kipDkIL7XWpQzYaD8.vS5lE5mbf4xu0F8eJdxiznqmfa5eMKA0',
  }
}
