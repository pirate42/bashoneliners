from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
        (r'^$', 'oneliner_list'),
        (r'^sourcecode/$', 'sourcecode'),
        (r'^mission/$', 'mission'),
        (r'^feeds/$', 'feeds'),

        (r'^oneliner/$', 'oneliner_list'),
        (r'^oneliner/(?P<pk>\d+)/$', 'oneliner'),
        (r'^oneliner/edit/(?P<pk>\d+)/$', 'oneliner_edit'),
        (r'^oneliner/new/$', 'oneliner_new'),
        (r'^oneliner/new/question/(?P<question_pk>\d+)/$', 'oneliner_answer'),
        (r'^oneliner/new/alternative/(?P<oneliner_pk>\d+)/$', 'oneliner_alternative'),
        (r'^oneliner/comment/(?P<pk>\d+)/$', 'oneliner_comment'),

        (r'^profile/(?P<pk>\d+)/$', 'profile'),
        (r'^profile/$', 'profile'),
        (r'^profile/edit/$', 'profile_edit'),

        (r'^question/$', 'question_list'),
        (r'^question/(?P<pk>\d+)/$', 'question'),
        (r'^question/edit/(?P<pk>\d+)/$', 'question_edit'),
        (r'^question/new/$', 'question_new'),

        (r'^comment/$', 'comment_list'),

        (r'^search/$', 'search'),

        (r'^login/$', 'login'),
        (r'^logout/$', 'logout'),

        (r'^help/markdown/$', 'help_markdown'),
        )

urlpatterns += patterns('main.ajax',
        (r'^ajax/markdown/$', 'markdown'),
        (r'^ajax/question/(?P<question_pk>\d+)/answered_by/oneliner/(?P<oneliner_pk>\d+)/$', 'question_answered'),
        (r'^ajax/search/$', 'search'),
        (r'^ajax/search/tag/$', 'search_by_tag'),
        )

urlpatterns += patterns('main.feeds',
        (r'^feeds/oneliner/$', 'oneliner'),
        (r'^feeds/question/$', 'question'),
        (r'^feeds/comment/$', 'comment'),
        )

# eof
