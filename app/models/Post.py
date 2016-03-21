from system.core.model import Model

class Post(Model):
	def __init__(self):
		super(Post, self).__init__()

	def get_user_wall(self, user_id):
		get_messages_query = "SELECT messages.id, messages.content, messages.created_at, messages.user_id, CONCAT(users.first_name, ' ', users.last_name) as name FROM messages JOIN users ON messages.user_id = users.id WHERE messages.posted_to_id = %s ORDER BY created_at DESC"
		user_wall = self.db.query_db(get_messages_query, [user_id])
		comments = self.get_comments(user_id)
		return {'messages': user_wall, 'comments': comments}

	def get_comments(self, wall_id):
		get_comment_query = "SELECT users.id, comments.message_id, comments.content, comments.created_at, CONCAT(users.first_name, ' ', users.last_name) as name FROM comments JOIN users ON comments.user_id = users.id WHERE wall_id = %s"
		return self.db.query_db(get_comment_query, [wall_id])


	def create_message(self, info):
		post_message_query = "INSERT INTO messages (content, user_id, posted_to_id, created_at) VALUES (%s, %s, %s, NOW())"
		content = [info['content'], info['posters_id'], info['posted_to_id']]
		return self.db.query_db(post_message_query, content)

	def create_comment(self, info):
		post_comment_query = "INSERT INTO comments (content, user_id, message_id, wall_id, created_at) VALUES (%s, %s, %s, %s, NOW())"
		content = [info['content'], info['posters_id'], info['message_id'], info['posted_to_id']]
		return self.db.query_db(post_comment_query, content)
