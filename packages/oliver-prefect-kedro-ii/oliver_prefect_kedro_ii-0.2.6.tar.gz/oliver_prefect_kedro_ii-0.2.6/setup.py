from distutils.core import setup
setup(
  name = 'oliver_prefect_kedro_ii',         
  packages = ['oliver_prefect_kedro_ii'], 
  version = '0.2.6', 
  license='MIT',     
  description = 'Prefect and Kedro package for Oliverto deployments',   
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'OTH JG',                
  author_email = 'jgerstein@olivetreeholdings.com',      
  url = 'https://github.com/oth-jonathan-gerstein/oliver_prefect_kedro_ii',   
  download_url = 'https://github.com/oth-jonathan-gerstein/oliver_prefect_kedro_ii/archive/refs/tags/v_0_2_6.tar.gz',    # I explain this later on
  keywords = ['KEDRO', 'PREFECT', 'ETL', 'OLIVERTO'],   
  install_requires=[            
          'kedro',
          'click',
          'pendulum',
          'pluggy',
          'prefect',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
