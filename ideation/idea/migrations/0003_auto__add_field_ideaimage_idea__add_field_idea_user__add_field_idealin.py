# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IdeaImage.idea'
        db.add_column(u'idea_ideaimage', 'idea',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['idea.Idea']),
                      keep_default=False)

        # Adding field 'Idea.user'
        db.add_column(u'idea_idea', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thoughtbubble.ThoughtbubbleUser'], null=True),
                      keep_default=False)

        # Removing M2M table for field links on 'Idea'
        db.delete_table(db.shorten_name(u'idea_idea_links'))

        # Removing M2M table for field images on 'Idea'
        db.delete_table(db.shorten_name(u'idea_idea_images'))

        # Removing M2M table for field support on 'Idea'
        db.delete_table(db.shorten_name(u'idea_idea_support'))

        # Adding field 'IdeaLink.idea'
        db.add_column(u'idea_idealink', 'idea',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['idea.Idea']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'IdeaImage.idea'
        db.delete_column(u'idea_ideaimage', 'idea_id')

        # Deleting field 'Idea.user'
        db.delete_column(u'idea_idea', 'user_id')

        # Adding M2M table for field links on 'Idea'
        m2m_table_name = db.shorten_name(u'idea_idea_links')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'idea.idea'], null=False)),
            ('idealink', models.ForeignKey(orm[u'idea.idealink'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'idealink_id'])

        # Adding M2M table for field images on 'Idea'
        m2m_table_name = db.shorten_name(u'idea_idea_images')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'idea.idea'], null=False)),
            ('ideaimage', models.ForeignKey(orm[u'idea.ideaimage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'ideaimage_id'])

        # Adding M2M table for field support on 'Idea'
        m2m_table_name = db.shorten_name(u'idea_idea_support')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'idea.idea'], null=False)),
            ('support', models.ForeignKey(orm[u'supportering.support'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'support_id'])

        # Deleting field 'IdeaLink.idea'
        db.delete_column(u'idea_idealink', 'idea_id')


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
        u'idea.idea': {
            'Meta': {'object_name': 'Idea'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thoughtbubble.ThoughtbubbleUser']", 'null': 'True'}),
            'what_for': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'what_kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['idea.IdeaType']"}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['neighborhood.Neighborhood']"})
        },
        u'idea.ideaimage': {
            'Meta': {'object_name': 'IdeaImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['idea.Idea']"}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'idea.idealink': {
            'Meta': {'object_name': 'IdeaLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['idea.Idea']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'idea.ideatype': {
            'Meta': {'object_name': 'IdeaType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'neighborhood.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'regionid': ('django.db.models.fields.FloatField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
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
        }
    }

    complete_apps = ['idea']