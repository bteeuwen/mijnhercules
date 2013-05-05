# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'matches_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'matches', ['Location'])

        # Adding model 'Match'
        db.create_table(u'matches_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nrid', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('teamhome', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_teamhome', to=orm['members.Team'])),
            ('teamaway', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_teamaway', to=orm['members.Team'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['matches.Location'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('substitutesneeded_home', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('substitutesneeded_away', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal(u'matches', ['Match'])

        # Adding M2M table for field substituteoptions_home on 'Match'
        db.create_table(u'matches_match_substituteoptions_home', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'matches.match'], null=False)),
            ('player', models.ForeignKey(orm[u'members.player'], null=False))
        ))
        db.create_unique(u'matches_match_substituteoptions_home', ['match_id', 'player_id'])

        # Adding M2M table for field substitutes_home on 'Match'
        db.create_table(u'matches_match_substitutes_home', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'matches.match'], null=False)),
            ('player', models.ForeignKey(orm[u'members.player'], null=False))
        ))
        db.create_unique(u'matches_match_substitutes_home', ['match_id', 'player_id'])

        # Adding M2M table for field playerspresent_home on 'Match'
        db.create_table(u'matches_match_playerspresent_home', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'matches.match'], null=False)),
            ('player', models.ForeignKey(orm[u'members.player'], null=False))
        ))
        db.create_unique(u'matches_match_playerspresent_home', ['match_id', 'player_id'])

        # Adding M2M table for field substituteoptions_away on 'Match'
        db.create_table(u'matches_match_substituteoptions_away', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'matches.match'], null=False)),
            ('player', models.ForeignKey(orm[u'members.player'], null=False))
        ))
        db.create_unique(u'matches_match_substituteoptions_away', ['match_id', 'player_id'])

        # Adding M2M table for field substitutes_away on 'Match'
        db.create_table(u'matches_match_substitutes_away', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'matches.match'], null=False)),
            ('player', models.ForeignKey(orm[u'members.player'], null=False))
        ))
        db.create_unique(u'matches_match_substitutes_away', ['match_id', 'player_id'])

        # Adding M2M table for field playerspresent_away on 'Match'
        db.create_table(u'matches_match_playerspresent_away', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm[u'matches.match'], null=False)),
            ('player', models.ForeignKey(orm[u'members.player'], null=False))
        ))
        db.create_unique(u'matches_match_playerspresent_away', ['match_id', 'player_id'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'matches_location')

        # Deleting model 'Match'
        db.delete_table(u'matches_match')

        # Removing M2M table for field substituteoptions_home on 'Match'
        db.delete_table('matches_match_substituteoptions_home')

        # Removing M2M table for field substitutes_home on 'Match'
        db.delete_table('matches_match_substitutes_home')

        # Removing M2M table for field playerspresent_home on 'Match'
        db.delete_table('matches_match_playerspresent_home')

        # Removing M2M table for field substituteoptions_away on 'Match'
        db.delete_table('matches_match_substituteoptions_away')

        # Removing M2M table for field substitutes_away on 'Match'
        db.delete_table('matches_match_substitutes_away')

        # Removing M2M table for field playerspresent_away on 'Match'
        db.delete_table('matches_match_playerspresent_away')


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
        u'matches.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'matches.match': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Match'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['matches.Location']"}),
            'nrid': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'playerspresent_away': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'match_playerspresentaway'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['members.Player']"}),
            'playerspresent_home': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'match_playerspresenthome'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['members.Player']"}),
            'substituteoptions_away': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'match_substituteoptions_away'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['members.Player']"}),
            'substituteoptions_home': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'match_substituteoptions_home'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['members.Player']"}),
            'substitutes_away': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'match_substitutes_away'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['members.Player']"}),
            'substitutes_home': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'match_substitutes_home'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['members.Player']"}),
            'substitutesneeded_away': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'substitutesneeded_home': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'teamaway': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_teamaway'", 'to': u"orm['members.Team']"}),
            'teamhome': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_teamhome'", 'to': u"orm['members.Team']"})
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

    complete_apps = ['matches']