conda-create:
  conda env create -f pyspark_env.yml

conda-update:
  conda env update -f pyspark_env.yml

conda-remove:
  conda env remove -n pyspark_env
