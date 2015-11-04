routes_in=(
  ('/','/init/default/index'),
  ('/dashboard','/init/dashboard/index'),
  ('/search','/init/search/index'),
  ('/stream', '/init/twitterbot/index'),
  ('/discover', '/init/recommended/index'),
  ('/about', '/init/about/index'),
  ('/login', '/init/default/login'),
  ('/logout', '/init/default/logout'),
  ('/help', '/init/help/index'),
)
routes_out=(
  ('/init/default/index','/'),
  ('/init/dashboard/index','/dashboard'),
  ('/init/search/index','/search'),
  ('/init/twitterbot/index','/stream'),
  ('/init/recommended/index','/discover'),
  ('/init/about/index','/about'),
  ('/init/default/login','/login'),
  ('/init/default/logout','/logout'),
  ('/init/help/index', '/help'),
)
