# CLE Lite — Git for LLMs™
**U.S. Patent Pending #63/909,873 (filed Nov 1, 2025)

![Patent Pending](https://img.shields.io/badge/Patent-Pending-blue)
![Stars](https://img.shields.io/github/stars/Austentel/cle-lite?style=social)

**Branching AI chat memory** using `parent_id` events.  
Edit a message → new branch, zero data loss.  
Replay any path → LLM only loads the active branch.

## The `ChatEvent` schema (public, patent-protected)
```protobuf
message ChatEvent {
  string event_id    = 1;  // ULID
  string parent_id   = 2;  // ← Git-style branching
  string session_id  = 3;
  string user_id     = 4;
  int64  ts_nanos    = 5;
  enum Role { USER=0; AI=1; TOOL=2; }
  Role   role        = 6;
  bytes  payload     = 7;
}

import redis, json
r = redis.Redis()
def add(msg, parent=None):
    evt = {"event_id":"01J...","parent_id":parent,**msg}
    r.lpush("chat", json.dumps(evt))


flowchart TD
    A[User] --> B[CLE Writer]
    B --> C[Kafka]
    C --> D[Flink]
    D --> E[Redis]
    F[LLM] --> E
    subgraph Branch
        R[A] --> U[B: Hi]
        U --> AI[C: Hello]
        R --> E[D: Hey]
        E --> AI2[E: Hi there]
    end
