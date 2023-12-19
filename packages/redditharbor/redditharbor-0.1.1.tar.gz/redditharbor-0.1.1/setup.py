from distutils.core import setup

setup(
  name = 'redditharbor',
  packages = ['redditharbor'],   
  version = '0.1.1',      
  license='MIT',        
  description = 'A tool designed to effortlessly collect and store Reddit data in a Supabase database.',   
  author = 'Nick S.H Oh',                   #
  author_email = 'nick.sh.oh@socialscience.ai',      
  url = 'https://github.com/socius-org/RedditHarbor/',  
  download_url = 'https://github.com/socius-org/RedditHarbor/archive/refs/tags/0.1.1.tar.gz', 
  keywords = ['Reddit', 'Supabase', 'Crawler'],
  install_requires=[
          'praw == 7.7.1',
          'supabase == 1.0.3', 
          'rich == 13.4.2',
          'python-dotenv == 1.0.0'
      ],
  include_package_data=True
)