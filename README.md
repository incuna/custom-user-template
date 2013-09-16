# Incuna Custom User Template

This is not intended for use as a pip-installable app as custom User models
always need to be customised. Instead, copy the `users` directory 
into your project, add `users` to your `INSTALLED_APPS`, and hack away!

*Note:* This is written for python 3, so if you're planning on using this with
python 2 you'll need to change the `__str__` method on the User to be a
`__unicode__` method.

*Also note:* This code is a hodge-podge of code found in blog posts long lost,
but we would happily acknowledge the original sources if asked.
