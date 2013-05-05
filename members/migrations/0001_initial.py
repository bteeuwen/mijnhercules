# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'members_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('level', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('switchingdays', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('captain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Player'], null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Team'])

        # Adding model 'MembershipHercules'
        db.create_table(u'members_membershiphercules', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('herculesnr', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True, null=True, blank=True)),
            ('subscription', self.gf('django.db.models.fields.CharField')(default='Wachtlijst', max_length=24)),
            ('injured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('enrolled', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('membersince', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('soccer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['MembershipHercules'])

        # Adding model 'Pass'
        db.create_table(u'members_pass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('knvbnr', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True, null=True, blank=True)),
            ('pasverloop', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('passtatus', self.gf('django.db.models.fields.CharField')(default='Foto', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Pass'])

        # Adding model 'Player'
        db.create_table(u'members_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('knvbnr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['members.Pass'], unique=True, null=True, blank=True)),
            ('herculesnr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['members.MembershipHercules'], unique=True, null=True, blank=True)),
            ('team_member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Team'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('cellphone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('regularphone', self.gf('django.db.models.fields.CharField')(max_length=14, null=True, blank=True)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=51)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True)),
            ('streetnr', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('streetnrplus', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(default='Speler', max_length=20, null=True, blank=True)),
            ('substitutewilling', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Player'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table(u'members_team')

        # Deleting model 'MembershipHercules'
        db.delete_table(u'members_membershiphercules')

        # Deleting model 'Pass'
        db.delete_table(u'members_pass')

        # Deleting model 'Player'
        db.delete_table(u'members_player')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'members.membershiphercules': {
            'Meta': {'ordering': "['herculesnr']", 'object_name': 'MembershipHercules'},
            'enrolled': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'herculesnr': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'injured': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'membersince': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'soccer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'subscription': ('django.db.models.fields.CharField', [], {'default': "'Wachtlijst'", 'max_length': '24'})
        },
        u'members.pass': {
            'Meta': {'ordering': "['knvbnr']", 'object_name': 'Pass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knvbnr': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'passtatus': ('django.db.models.fields.CharField', [], {'default': "'Foto'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pasverloop': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'members.player': {
            'Meta': {'object_name': 'Player'},
            'age': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cellphone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '51'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'herculesnr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['members.MembershipHercules']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knvbnr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['members.Pass']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'regularphone': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'Speler'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'streetnr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'streetnrplus': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'substitutewilling': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'team_member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Team']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'members.team': {
            'Meta': {'ordering': "['number']", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Player']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'switchingdays': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['members']