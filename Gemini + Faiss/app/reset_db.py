from pymongo import MongoClient

# ✅ Connect to MongoDB
client = MongoClient("mongodb+srv://yashshahmindsyncx:iWyf4cfsw55dFujv@chatbotcluster.xsgutpz.mongodb.net/?retryWrites=true&w=majority&appName=ChatbotCluster")

db = client["chatbot"]
sessions = db["chat_sessions"]

# ✅ Delete all existing sessions
result = sessions.delete_many({})
print(f"🗑️ Deleted {result.deleted_count} sessions.")

# # ✅ Create a new session
# from datetime import datetime

# new_session = {
#     "created_at": datetime.utcnow(),
#     "messages": [],
#     "session_name": "New Chat"
# }
# inserted = sessions.insert_one(new_session)
# print(f"✅ New session created with ID: {inserted.inserted_id}")
