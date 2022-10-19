#!/bin/bash

# Create DB
docker exec -it mongors1n1 bash -c 'echo "use recommendations" | mongosh'

# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"recommendations\")" | mongosh'

# creating collections
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"recommendations.profiles\")" | mongosh'

# sharding collections
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"recommendations.profiles\", {\"user_id\": \"hashed\"})" | mongosh'

# indexing collections
docker exec -it mongos1 bash -c 'echo "db.profiles.createIndex( { \"user_id\": 1 } )" | mongosh'
