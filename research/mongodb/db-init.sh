#!/bin/bash

# Create DB
docker exec -it mongors1n1 bash -c 'echo "use RecomDB" | mongosh'

# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"RecomDB\")" | mongosh'

# creating collections
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"RecomDB.profiles\")" | mongosh'

# sharding collections
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"RecomDB.profiles\", {\"user_id\": \"hashed\"})" | mongosh'

# indexing collections
docker exec -it mongos1 bash -c 'echo "db.profiles.createIndex( { \"user_id\": 1 } )" | mongosh'
