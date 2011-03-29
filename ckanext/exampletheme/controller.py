import sys
from ckan.lib.base import request
from ckan.lib.base import c, g, h
from ckan.lib.base import model
from ckan.lib.base import render
from ckan.lib.base import _

from ckan.controllers.user import UserController


class CustomUserController(UserController):
    """This controller is an example to show how you might extend or
    override core CKAN behaviour from an extension package.

    It duplicates functionality in the core CKAN UserController's
    register function, but extends it to make an email address
    mandatory.
    """
    def custom_register(self):
        if request.method == 'POST':
            # custom validation that requires an email address
            error = False
            c.email = request.params.getone('email')
            c.login = request.params.getone('login')
            if not model.User.check_name_available(c.login):
                error = True
                h.flash_error(_("That username is not available."))
            if not c.email:
                error = True
                h.flash_error(_("You must supply an email address."))
            try:
                self._get_form_password()
            except ValueError, ve:
                h.flash_error(ve)
                error = True
            if error:
                return render('user/register.html')
        # now delegate to core CKAN register method
        return self.register()
