### **Eviction Policies of In-Memory Databases**

Eviction policies define how in-memory databases handle situations when the memory limit is reached. These policies determine which data is removed to make space for new data. Redis, being a widely used in-memory database, provides several eviction policies configurable based on the use case.

---

### **Eviction Policies in Redis**

Redis supports the following eviction policies:

1. **noeviction** *(default)*:
   - Returns an error when memory is full and new data is written.
   - Suitable for scenarios where evictions must be explicitly managed.

2. **allkeys-lru**:
   - Removes the least recently used (LRU) keys across all keys to free memory.

3. **volatile-lru**:
   - Removes the least recently used keys, but only from keys with a TTL.

4. **allkeys-random**:
   - Evicts a random key across all keys.

5. **volatile-random**:
   - Evicts a random key, but only from keys with a TTL.

6. **volatile-ttl**:
   - Evicts keys with the nearest expiration time.

7. **allkeys-lfu** *(Redis 4.0+)*:
   - Evicts the least frequently used (LFU) keys across all keys.

8. **volatile-lfu** *(Redis 4.0+)*:
   - Evicts the least frequently used keys, but only from keys with a TTL.

---

### **How to Set Eviction Policy in Redis**

To configure the eviction policy in Redis, use the `maxmemory-policy` configuration.

1. **In `redis.conf`**:
   ```conf
   maxmemory 100mb
   maxmemory-policy allkeys-lru
   ```

2. **Using CLI**:
   ```bash
   redis-cli CONFIG SET maxmemory 100mb
   redis-cli CONFIG SET maxmemory-policy allkeys-lru
   ```

---

### **Example: Using Redis with Eviction Policy**

#### **Setup:**
- Configure Redis to use `allkeys-lru` with a memory limit of 1 MB.
- Insert keys into Redis and observe evictions.

#### **Python Code Example**:
```python
import redis

# Connect to Redis
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Set memory limit and eviction policy
client.config_set("maxmemory", "1mb")  # Set max memory to 1 MB
client.config_set("maxmemory-policy", "allkeys-lru")  # Use allkeys-lru eviction policy

# Insert data
for i in range(1, 10000):  # Large number to exceed memory limit
    client.set(f"key{i}", f"value{i}")
    if i % 100 == 0:
        print(f"Inserted key{i}")

# Verify evictions
print("Current keys in Redis:")
keys = client.keys()
print(keys[:10])  # Show first 10 keys to verify which keys remain
```

---

### **Expected Output**
1. The program inserts many keys into Redis.
2. When the memory limit of 1 MB is reached, Redis evicts the least recently used keys to make room for new ones.
3. The output displays only a subset of the most recently used keys.

---

### **Monitoring Evictions**

Use Redis CLI to monitor evictions in real-time:

```bash
redis-cli monitor
```

Or check stats:

```bash
redis-cli info memory
```

Key fields to observe:
- `evicted_keys`: Number of keys evicted due to memory pressure.

---

### **Example Output from CLI**
```bash
# After running the Python script
127.0.0.1:6379> INFO memory
# Memory stats
used_memory:1048576
used_memory_peak:2097152
evicted_keys:1500
maxmemory:1048576
maxmemory_policy:allkeys-lru
```

---

### **Conclusion**

Redis provides flexible eviction policies tailored for different use cases. Using `allkeys-lru` ensures that the cache stays performant by retaining frequently accessed data while evicting less-used data. Choose the eviction policy that aligns with your application's access patterns and requirements.
