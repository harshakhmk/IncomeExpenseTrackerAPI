Custom defined user  clashes with Default User model permissions and its associated group's permissions
(Solved by setting AUTH_USER_MODEL to custom defined model in settings file)

RuntimeError: You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to 127.0.0.1:8000/auth/register/ (note the trailing slash), or set APPEND_SLASH=False in your Django settings.

django-jwt-extension able to simply give access, refresh tokens

we r using smtp.gmail as email host

Silly issue, Getting error when calling a class function without using self while calling it in other function

Cannot assign "<django.contrib.auth.models.AnonymousUser object at 0x000001EBA166DE50>": "Expense.user" must be a "User" instance.
Solved by def get_queryset method in that class