# admin testing
def is_admin(user):
    """returns true if requested user is superuser/admin
    otherwise false"""
    return user.is_superuser
