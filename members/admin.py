from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

from members.models import Player, Team, Pass, MembershipHercules

class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        #'user',
        'content_type',
        'action_flag',
        'action_time'
    ]

    search_fields = [
        'object_repr',
        'change_message',
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'


admin.site.register(LogEntry, LogEntryAdmin)


'''
class PlayersInline(admin.StackedInline):
    model = Player
    extra = 1

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['number']}),
        (' Player information', {'fields': ['first_name']}),
    ]
    inlines = [PlayersInline]

admin.site.register(Team, TeamAdmin)
admin.site.register(Player)
'''


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'suffix', 'last_name', 'mailplayer', 'teamlink', 'userlink', 'knvblink', 'herlink')
    list_filter = ['team_member__level', 'knvbnr__passtatus', 'gender']
    search_fields = ['last_name', 'first_name', 'team_member__number', 'herculesnr__herculesnr', 'knvbnr__knvbnr', 'email']
    list_per_page = 185

    def knvblink(self, obj):
      return ('<a href="/admin/members/pass/%s">%s</a>' % (obj.knvbnr.id, obj.knvbnr.knvbnr))
    knvblink.short_description = 'KNVB ID'
    knvblink.allow_tags = True

    def herlink(self, obj):
      return ('<a href="/admin/members/membershiphercules/%s">%s</a>' % (obj.herculesnr.id, obj.herculesnr.herculesnr))
    herlink.short_description = 'Hercules ID'
    herlink.allow_tags = True

    def teamlink(self, obj):
        try:
            return ('<a href="/admin/members/team/%s">%s</a>' % (obj.team_member.id, obj.team_member.number))
        except:
            pass
    teamlink.short_description = 'Team'
    teamlink.allow_tags = True

    def mailplayer(self, obj):
      return ('<a href="mailto:%s">%s</a>' % (obj.email, obj.email))
    mailplayer.short_description = 'Email'
    mailplayer.allow_tags = True

    def userlink(self, obj):
      return ('<a href="/admin/auth/user/%s">%s</a>' % (obj.user.id, obj.user.username))
    userlink.short_description = 'account'
    userlink.allow_tags = True

    # idee hiermee is om filter op standaard waarde te laten beginnen.
    # http://stackoverflow.com/questions/851636/default-filter-in-django-admin
    # def changelist_view(self, request, extra_context=None):
    #     if not request.GET.has_key('decommissioned__exact'):

    #         q = request.GET.copy()
    #         q['decommissioned__exact'] = 'N'
    #         request.GET = q
    #         request.META[Player__role == 'Aanvoerder'] = request.GET.urlencode()
    #     return super(PlayerAdmin,self).changelist_view(request, extra_context=extra_context)


class PassAdmin(admin.ModelAdmin):
    search_fields = ['knvbnr']
    list_filter = ['passtatus']

class MembershipHerculesAdmin(admin.ModelAdmin):
    search_fields = ['herculesnr']
    #list_filter = ['passtatus']


admin.site.register(MembershipHercules, MembershipHerculesAdmin)
admin.site.register(Team)
admin.site.register(Pass, PassAdmin)
admin.site.register(Player, PlayerAdmin)