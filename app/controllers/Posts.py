from system.core.controller import *

class Posts(Controller):
	def __init__(self, action):
		super(Posts, self).__init__(action)
		self.load_model('Post')

	def index(self):
		pass

	def post_message(self):
		info = {
			'posters_id': request.form['poster_id'],
			'posted_to_id': request.form['wall_owner'],
			'content': request.form['post']
		}
		self.models['Post'].create_message(info)
		return redirect('/show/'+str(request.form['wall_owner']))

	def post_comment(self):
		info = {
			'posters_id': request.form['poster_id'],
			'posted_to_id': request.form['wall_owner'],
			'message_id': request.form['message_id'],
			'content': request.form['comment']
		}
		self.models['Post'].create_comment(info)
		return redirect('/show/'+str(request.form['wall_owner']))