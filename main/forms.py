''' Kind reminders, (please review before editing!)
    - Forms are for validating input, NOT business logic.
    - Only include model specific logic in forms if it is required for input.
      Example: user should be able to select only the groups it is member of.
    '''

from django import forms

from bashoneliners.main.models import OneLiner, HackerProfile, User, WishListQuestion

''' constants '''

#


''' forms '''

class CommonOneLinerForm(forms.ModelForm):
    user = None
    action = forms.CharField()

    def __init__(self, user, *args, **kwargs):
	self.user = user
	super(CommonOneLinerForm, self).__init__(*args, **kwargs)

    class Meta:
	model = OneLiner

	widgets = {
		'line': forms.Textarea(attrs={'cols': 80, 'rows': 3, }),
		'summary': forms.TextInput(attrs={'size': 100, }),
		'explanation': forms.Textarea(attrs={'cols': 80, 'rows': 10, }),
		'limitations': forms.Textarea(attrs={'cols': 80, 'rows': 3, }),
		}

	fields = (
		'line',
		'summary',
		'explanation',
		'limitations',
		'is_published',
		)


class PostOneLinerForm(CommonOneLinerForm):
    title = 'Post a one-liner'
    actions = ('Post one-liner',)

    def save(self):
	self.instance.user = self.user
	return super(PostOneLinerForm, self).save()


class EditOneLinerForm(CommonOneLinerForm):
    title = 'Edit one-liner'
    action_save = 'Save one-liner'
    action_delete = 'Delete one-liner'
    actions = (action_save, action_delete,)
    edit = True
    is_save = False
    is_delete = False

    def clean_action(self):
	action = self.cleaned_data['action']
	if action == self.action_save:
	    self.is_save = True
	elif action == self.action_delete:
	    self.is_delete = True
	return action

    def clean(self):
	if self.instance.user != self.user:
	    raise forms.ValidationError('User %s is not the owner of this OneLiner' % self.user)

	return self.cleaned_data


class SearchOneLinerForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 60}))


class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
	super(EditUserForm, self).__init__(*args, **kwargs)
	self.fields['password'].required = False

    def save(self):
	user = super(EditUserForm, self).save(commit=False)
	new_password = self.cleaned_data['password']
	if new_password is not None:
	    user.set_password(new_password)
	user.save()
	return user

    class Meta:
	model = User

	fields = (
		'username',
		'password',
		)


class EditHackerProfileForm(forms.ModelForm):
    class Meta:
	model = HackerProfile

	widgets = {
		'twitter_name': forms.TextInput(attrs={'size': 40, }),
		'blog_url': forms.TextInput(attrs={'size': 80, }),
		'homepage_url': forms.TextInput(attrs={'size': 80, }),
		}

	exclude = (
		'user',
		)


class CommonWishListQuestionForm(forms.ModelForm):
    user = None
    action = forms.CharField()

    def __init__(self, user, *args, **kwargs):
	self.user = user
	super(CommonWishListQuestionForm, self).__init__(*args, **kwargs)

    class Meta:
	model = WishListQuestion

	widgets = {
		'question': forms.Textarea(attrs={'cols': 80, 'rows': 5, }),
		}

	fields = (
		'question',
		'is_published',
		'is_answered',
		)


class PostWishListQuestionForm(CommonWishListQuestionForm):
    title = 'Post a question'
    actions = ('Post question',)

    def save(self):
	self.instance.user = self.user
	return super(PostWishListQuestionForm, self).save()


class EditWishListQuestionForm(CommonWishListQuestionForm):
    title = 'Edit question'
    action_save = 'Save question'
    action_delete = 'Delete question'
    actions = (action_save, action_delete,)
    edit = True
    is_save = False
    is_delete = False

    def clean_action(self):
	action = self.cleaned_data['action']
	if action == self.action_save:
	    self.is_save = True
	elif action == self.action_delete:
	    self.is_delete = True
	return action

    def clean(self):
	if self.instance.user != self.user:
	    raise forms.ValidationError('User %s is not the owner of this Question' % self.user)

	return self.cleaned_data


# eof
