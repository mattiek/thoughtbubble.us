# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ThoughtbubbleUser'
        db.create_table(u'thoughtbubble_thoughtbubbleuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=25, db_index=True)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=254)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thoughtbubble', ['ThoughtbubbleUser'])

        # Adding M2M table for field groups on 'ThoughtbubbleUser'
        m2m_table_name = db.shorten_name(u'thoughtbubble_thoughtbubbleuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thoughtbubbleuser', models.ForeignKey(orm[u'thoughtbubble.thoughtbubbleuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thoughtbubbleuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'ThoughtbubbleUser'
        m2m_table_name = db.shorten_name(u'thoughtbubble_thoughtbubbleuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thoughtbubbleuser', models.ForeignKey(orm[u'thoughtbubble.thoughtbubbleuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thoughtbubbleuser_id', 'permission_id'])

        # Adding model 'ThoughtbubbleUserProfile'
        db.create_table(u'thoughtbubble_thoughtbubbleuserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thoughtbubble.ThoughtbubbleUser'])),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'thoughtbubble', ['ThoughtbubbleUserProfile'])


    def backwards(self, orm):
        # Deleting model 'ThoughtbubbleUser'
        db.delete_table(u'thoughtbubble_thoughtbubbleuser')

        # Removing M2M table for field groups on 'ThoughtbubbleUser'
        db.delete_table(db.shorten_name(u'thoughtbubble_thoughtbubbleuser_groups'))

        # Removing M2M table for field user_permissions on 'ThoughtbubbleUser'
        db.delete_table(db.shorten_name(u'thoughtbubble_thoughtbubbleuser_user_permissions'))

        # Deleting model 'ThoughtbubbleUserProfile'
        db.delete_table(u'thoughtbubble_thoughtbubbleuserprofile')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thoughtbubble.thoughtbubbleuser': {
            'Meta': {'object_name': 'ThoughtbubbleUser'},
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '254'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '25', 'db_index': 'True'})
        },
        u'thoughtbubble.thoughtbubbleuserprofile': {
            'Meta': {'object_name': 'ThoughtbubbleUserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thoughtbubble.ThoughtbubbleUser']"})
        }
    }

    complete_apps = ['thoughtbubble']