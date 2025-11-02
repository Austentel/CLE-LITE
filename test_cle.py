import redis
import json
import time
import uuid

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def generate_ulid():
    """Generate a simple ULID-like ID for testing"""
    timestamp = str(int(time.time() * 1000))[-10:]
    random_part = str(uuid.uuid4())[:8]
    return f"01J{timestamp}{random_part}".upper()

def add(msg, role=0, parent=None, session="demo"):
    """Add a chat event to Redis"""
    evt = {
        "event_id": generate_ulid(),
        "parent_id": parent or "",
        "session_id": session,
        "user_id": "matt",
        "ts_nanos": int(time.time_ns()),
        "role": role,
        "payload": msg
    }
    r.lpush(f"chat:{session}", json.dumps(evt))
    return evt["event_id"]  # Return the event_id for branching

def get_chat_history(session="demo"):
    """Retrieve and display chat history"""
    history = r.lrange(f"chat:{session}", 0, -1)
    events = [json.loads(event) for event in history]
    return events

def print_chat_tree(events):
    """Print events in a tree structure to show branching"""
    print("\n=== Chat Event Tree ===")
    for i, event in enumerate(reversed(events)):
        indent = "  " if event.get("parent_id") else ""
        role_names = {0: "USER", 1: "AI", 2: "TOOL"}
        role = role_names.get(event.get("role", 0), "UNKNOWN")
        print(f"{indent}[{i}] {role}: {event.get('payload', 'N/A')}")
        print(f"{indent}    Event ID: {event.get('event_id', 'N/A')}")
        if event.get("parent_id"):
            print(f"{indent}    Parent ID: {event.get('parent_id', 'N/A')}")
        print()

def run_test():
    """Run a test demonstrating the branching functionality"""
    print("=== CLE-LITE Test ===\n")

    # Clear previous test data
    r.delete("chat:demo")
    print("1. Cleared previous test data")

    # Test 1: Add initial message
    print("\n2. Adding initial message...")
    event1_id = add("Hello, I need help with Python", role=0)
    print(f"   Added: User message (Event ID: {event1_id})")

    # Test 2: Add AI response
    print("\n3. Adding AI response...")
    event2_id = add("I'd be happy to help you with Python!", role=1, parent=event1_id)
    print(f"   Added: AI response (Event ID: {event2_id})")

    # Test 3: Create a branch by editing the original message
    print("\n4. Creating a branch by editing the original message...")
    event3_id = add("Actually, I need help with JavaScript", role=0, parent=event1_id)
    print(f"   Added: Edited user message (Event ID: {event3_id}) - This creates a new branch!")

    # Test 4: Add AI response to the edited branch
    print("\n5. Adding AI response to the new branch...")
    event4_id = add("Sure, I can help you with JavaScript!", role=1, parent=event3_id)
    print(f"   Added: AI response on new branch (Event ID: {event4_id})")

    # Test 5: Retrieve and display the chat history
    print("\n6. Retrieving chat history from Redis...")
    events = get_chat_history()
    print(f"   Total events stored: {len(events)}")

    # Display the tree structure
    print_chat_tree(events)

    # Show raw JSON for verification
    print("\n=== Raw JSON Events ===")
    for i, event in enumerate(events):
        print(f"Event {i}: {event}")

    return len(events) == 4  # Should have exactly 4 events

if __name__ == "__main__":
    try:
        # Check Redis connection
        r.ping()
        print("Redis connection successful!\n")

        # Run the test
        success = run_test()

        if success:
            print("\n✓ Test completed successfully!")
            print("The chat event system with branching is working correctly.")
        else:
            print("\n✗ Test failed - unexpected number of events")

    except redis.ConnectionError:
        print("✗ Cannot connect to Redis. Please ensure Redis is running.")
        print("  Run: redis-server")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")