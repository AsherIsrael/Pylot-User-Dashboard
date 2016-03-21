from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')
		self.load_model('Post')

	def index(self):
		return self.load_view('users/index.html')

	def display_login(self):
		return self.load_view('/users/login.html')

	def display_register(self):
		return self.load_view('users/register.html')

	def dashboard(self):
		users = self.models['User'].get_all_users()
		return self.load_view('users/dashboard.html', users=users)

	def create_user(self):
		info = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'pass_confirm': request.form['pass_confirm'],
			'user_level': 1
		}
		users = self.models['User'].check_database()
		if not users:
			info['user_level'] = 9
		validated = self.models['User'].validate_registration(info)
		if not validated['status']:
			for error in validated['errors']:
				flash(error)
			return redirect('/register')
		new_user = self.models['User'].add_user(validated['info'])
		if session:
			if session['authorization'] == 9:
				return redirect('/dashboard')
		else:
			session['user_id'] = new_user['id']
			session['authorization'] = new_user['user_level']
			return redirect('/dashboard')

	def edit(self):
		user = self.models['User'].get_user(session['user_id'])
		return self.load_view('/users/edit_user.html', user=user)

	def admin_edit(self, id):
		if session['authorization'] == 9:
			user = self.models['User'].get_user(id)
			return self.load_view('/users/edit_user.html', user=user)
		return redirect('/dashboard')

	def edit_controller(self):
		info = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'pass_confirm': request.form['pass_confirm'],
			'user_level': request.form['set_level'],
			'user_id': request.form['user_id'],
			'description': request.form['description']
		}

		path = request.form['edit_type']
		if path == "edit_password":
			return self.change_password(info)
		elif path == "edit_user_info":
			return self.change_email_name(info)
		elif path == "edit_description":
			return self.change_description(info)
		return redirect('/dashboard')

	def change_email_name(self, info):
		user_id = info['user_id']
		result = self.models['User'].validate_email_name(info)
		if not result['status']:
			for error in result['errors']:
				flash(error)
			if session['authorization'] == 9:
				return redirect('/edit/'+ str(user_id))
			else:
				return redirect('/edit')
		else:
			user = self.models['User'].get_user(user_id)
			user['first_name'] = info['first_name']
			user['last_name'] = info['last_name']
			user['email'] = info['email']
			self.models['User'].update_user(user)
			return redirect('/show/'+ str(user_id))

	def change_password(self, info):
		user_id = info['user_id']
		result = self.models['User'].validate_password(info)
		if not result['status']:
			error = [result['error']][0]
			flash(error)
			if session['authorization'] == 9:
				return redirect('/edit/'+ str(user_id))
			else:
				return redirect('/edit')
		else:
			user = self.models['User'].get_user(user_id)
			user['pw_hash'] = result['pass_encrypt']
			self.models['User'].update_user(user)
			return redirect('/show/'+ str(user_id))

	def change_description(self, info):
		user = self.models['User'].get_user(info['user_id'])
		user['description'] = info['description']
		self.models['User'].update_user(user)
		return redirect('/show/'+str(info['user_id']))

	def show(self,id):
		user = self.models['User'].get_user(id)
		posts = self.models['Post'].get_user_wall(id)
		return self.load_view('/users/user_page.html', user=user, messages=posts['messages'], comments=posts['comments'])

	def logoff(self):
		session.clear()
		return redirect('/')

	def login(self):
		info = {
			'email': request.form['email'],
			'password': request.form['password']
		}

		result = self.models['User'].validate_login(info)

		if result:
			session['user_id'] = result['id']
			session['authorization'] = result['user_level']
			return redirect('/dashboard')

		return redirect('/')

	def destroy(self, id):
		self.models['User'].remove_user(id)
		if session['user_id'] == id:
			return redirect('/logoff')
		return redirect('/dashboard')