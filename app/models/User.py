from system.core.model import Model
import re

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def validate_registration(self, info):
		print "model validate_registration"
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		errors = []

		first_name = info['first_name']
		last_name = info['last_name']
		email = info['email']
		pass_check = [info['password'], info['pass_confirm']]

		if not first_name:
			errors.append('First name cannot be blank')
		elif len(first_name) < 2:
			errors.append('First name must be at least 2 characters')
		elif not first_name.isalpha():
			errors.append('First name cannot contain non-letter characters')

		if not last_name:
			errors.append('Last name cannot be blank')
		elif len(last_name) < 2:
			errors.append('Last name must be at least 2 characters')
		elif not last_name.isalpha():
			errors.append('Last name cannot contain non-letter characters')

		if not email:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(email):
			errors.append('Must enter a valid email')

		print errors
		password_result = self.validate_password(pass_check)
		if not password_result['status']:
			errors.append(password_result['error'])

		user_exist = self.get_user_by_email(email)
		if user_exist:
			errors.append("Email is already registered")

		print errors
		if errors:
			return {'status': False, 'errors': errors}
		else:
			user = self.add_user(info)
			return {'status': True, 'user': user}

	def add_user(self, info):
		first_name = info['first_name']
		last_name = info['last_name']
		email = info['email']
		password = info['password']

		pass_encrypt = self.bcrypt.generate_password_hash(password)
		add_query = "INSERT INTO users (first_name, last_name, email, pw_hash, user_level, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
		content = [first_name, last_name, email, pass_encrypt, info['user_level']]
		self.db.query_db(add_query, content)
		get_new_user = "SELECT id, user_level FROM users ORDER BY id DESC LIMIT 1"
		user = self.db.query_db(get_new_user)
		return user[0]

	def validate_password(self, info):
		print "model validate_password"
		password = info[0]
		pass_confirm = info[1]
		error = ''

		if not password:
			error = "Password cannot be blank"
		elif len(password) < 8:
			error = "Password must be at least 8 characters"
		elif not password == pass_confirm:
			error = 'Password must match confirmation'

		if error:
			print "password fail"
			return {'status': False, 'error': error}
		else:
			print "password pass"
			return {'status': True}


	def validate_login(self, info):
		print "model validate_login"
		email = info['email']
		password = info['password']

		query = "SELECT * FROM users WHERE email = %s LIMIT 1"
		user_info = self.db.query_db(query, [email])
		if user_info:
			if self.bcrypt.check_password_hash(user_info[0]['pw_hash'], password):
				return user_info[0]
		return False

	def get_all_users(self):
		print "model get_all_users"
		get_all_query = "SELECT CONCAT(first_name, ' ', last_name) as name, id, email, created_at, user_level FROM users"
		return self.db.query_db(get_all_query)

	def get_user(self, id):
		print "model get_user"
		get_user_query = "SELECT id, first_name, last_name, description, DATE_FORMAT(created_at, '%M, %D, %Y') AS created_at, email, pw_hash, user_level FROM users WHERE id = %s"
		return self.db.query_db(get_user_query, [id])

	def get_user_by_email(self, email):
		print "model get_user_by_email"
		get_user_query = "SELECT id, first_name, last_name, description, DATE_FORMAT(created_at, '%M, %D, %Y') AS created_at, email, pw_hash, user_level FROM users WHERE email = %s"
		return self.db.query_db(get_user_query, [email])