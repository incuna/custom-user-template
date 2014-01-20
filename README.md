# Incuna Custom User Template

This is not intended for use as a pip-installable app as custom User models
always need to be customised. Instead, copy the `users` directory 
into your project, add `users` to your `INSTALLED_APPS`, add 
`AUTH_USER_MODEL = 'users.User'`, and hack away!
To use the tests `pip install incuna-test-utils`.
To use the views include the urls 
`url(r'^profile/', include('users.urls', namespace='users', app_name='users'))`

There is more information in the [Django docs](https://docs.djangoproject.com/en/1.6/topics/auth/customizing/#auth-custom-user).

*Note:* This is written for python 3, so if you're planning on using this with
python 2 you'll need to change the `__str__` method on the User to be a
`__unicode__` method.

*Also note:* This code is a hodge-podge of code found in blog posts long lost,
but we would happily acknowledge the original sources if asked.
