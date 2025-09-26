// waste_tracker.jac
// Import libraries for date formatting
import:py from datetime;
import:py from jaseci.jsorc.live_actions;

// --------------------------
// Data model for the graph
// --------------------------

// User object
object user:
    has str name;

// Waste item object with geo-location
object waste_item:
    has str name;
    has float latitude;
    has float longitude;
    has datetime reported_at;

// Edge to connect a user to a waste item
edge reported_by;


// ----------------------------
// Walker to report new waste
// ----------------------------
walker report_waste(
    str user_name,
    str item_name,
    float lat,
    float lon
):
    has node<user> current_user;
    has node<waste_item> new_item;

    // Find user or create a new one
    current_user = spawn here walker::find_user(user_name);

    // Spawn a new waste item in the graph
    new_item = spawn here<waste_item>(
        name = item_name,
        latitude = lat,
        longitude = lon,
        reported_at = now
    );

    // Connect the user to the new waste item
    current_user +[reported_by]+> new_item;

    std.out = "✅ Waste reported by " + user_name + ": " + item_name;

// Helper walker to find or create a user
walker find_user(str name):
    has node<user> user_node;
    // Try to find the user first
    with entry {
        visitor = root;
        for i in visitor.nodes {
            if (i.kind == "user" and i.context["name"] == name) {
                user_node = i;
                break;
            }
        }
    }
    // If user not found, create a new one
    if (user_node == null):
        user_node = spawn here<user>(name=name);

    return user_node;


// ----------------------------------
// Walker to retrieve all waste logs
// ----------------------------------
walker list_waste_reports:
    has list results = [];

    // Traverse and collect all waste_item objects
    with entry {
        for item in -->.nodes {
            if (item.kind == "waste_item") {
                has list reporters = item o.. <--(reported_by);
                has str reporter_name = "Unknown";
                if (reporters.length > 0):
                    reporter_name = reporters[0].context["name"];

                // Format the timestamp
                has str formatted_date = date.format(item.context["reported_at"], "%Y-%m-%d %H:%M:%S");

                results.append({
                    "item": item.context["name"],
                    "reported_by": reporter_name,
                    "location": {
                        "latitude": item.context["latitude"],
                        "longitude": item.context["longitude"]
                    },
                    "reported_at": formatted_date
                });
            }
        }
    }

    std.out = results;