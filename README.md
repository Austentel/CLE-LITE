# CLE Lite — Git for LLMs™
**U.S. Patent Pending #63/909,873 (filed Nov 1, 2025)

![Patent Pending](https://img.shields.io/badge/Patent-Pending-blue)
![Stars](https://img.shields.io/github/stars/Austentel/cle-lite?style=social)

**Branching AI chat memory** using `parent_id` events.  
Edit a message → new branch, zero data loss.  
Replay any path → LLM only loads the active branch.

## The `ChatEvent` schema (public, patent-protected)
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

## Reddis Demo
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

## Install and Run
pip install redis
redis-server &
python -c "from your_script import add; [add(input()) for _ in range(3)]"

## Watch the Magic!
redis-cli lrange chat:demo 0 -1 | python -m json.tool


    
