#!/bin/bash

# Create DB
docker exec -it mongors1n1 bash -c 'echo "use UGC_data" | mongosh'

# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"UGC_data\")" | mongosh'

# creating collections
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"UGC_data.views\")" | mongosh'

# sharding collections
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"UGC_data.views\", {\"user_id\": \"hashed\"})" | mongosh'

# indexing collections
docker exec -it mongos1 bash -c 'echo "db.likes.createIndex( { \"user_id\": 1 } )" | mongosh'
