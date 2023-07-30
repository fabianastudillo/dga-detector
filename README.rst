===============
BNDF + DGA Detector on Docker
===============

Install process
===============
.. code-block:: bash

  git clone -b Docker https://github.com/fabianastudillo/dga-detector.git
  unrar x ./dga-detector/dgam-uc/models/KNN-Maldom.rar -d ./dga-detector/dgam-uc/models/
  unrar x ./dga-detector/dgam-uc/models/RF-MG.part01.rar -d ./dga-detector/dgam-uc/models/
  cd dga-detector/
  docker-compose up -d

Useful commands
================
Most docker-compose commands will have the following form ``docker-compose COMMAND [container-name]``
Those commands must be run from the SELKS/docker/ directory
If  no container-name is provided, it will be applied to all SELKS containers

Stopping containers
-------------------
.. code-block:: bash

  docker-compose stop [container-name]

Starting containers
-------------------
.. code-block:: bash

  docker-compose start [container-name]

Restarting containers
-------------------
.. code-block:: bash

  docker-compose restart [container-name]

Removing containers along with their data
-------------------
.. code-block:: bash

  docker-compose down -v

Recreating containers
-------------------
.. code-block:: bash

  docker-compose up [container-name] --force-recreate

Updating containers
-------------------
.. code-block:: bash

  docker-compose pull [container-name]
  docker-compose up [container-name] --force-recreate
  
Enterring a running containers
------------------------------
.. code-block:: bash

  docker exec -it [container-name] /bin/bash
  
Get logs from a container
-------------------------
.. code-block:: bash

  docker logs [container-name]
  
logs can also be found in bndf/docker/containers-data

Some problems
=====
The main problem when logstash not receive data is the kind of port udp/tcp 
