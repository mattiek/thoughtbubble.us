# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IdeaType'
        db.create_table(u'idea_ideatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'idea', ['IdeaType'])

        # Adding model 'IdeaImage'
        db.create_table(u'idea_ideaimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'idea', ['IdeaImage'])

        # Adding model 'IdeaLink'
        db.create_table(u'idea_idealink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'idea', ['IdeaLink'])

        # Adding model 'Idea'
        db.create_table(u'idea_idea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('what_kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['idea.IdeaType'])),
            ('what_for', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('where', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['neighborhood.Neighborhood'])),
        ))
        db.send_create_signal(u'idea', ['Idea'])

        # Adding M2M table for field images on 'Idea'
        m2m_table_name = db.shorten_name(u'idea_idea_images')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'idea.idea'], null=False)),
            ('ideaimage', models.ForeignKey(orm[u'idea.ideaimage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'ideaimage_id'])

        # Adding M2M table for field links on 'Idea'
        m2m_table_name = db.shorten_name(u'idea_idea_links')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm[u'idea.idea'], null=False)),
            ('idealink', models.ForeignKey(orm[u'idea.idealink'], null=False))
        ))
        db.create_unique(m2m_table_name, ['idea_id', 'idealink_id'])


    def backwards(self, orm):
        # Deleting model 'IdeaType'
        db.delete_table(u'idea_ideatype')

        # Deleting model 'IdeaImage'
        db.delete_table(u'idea_ideaimage')

        # Deleting model 'IdeaLink'
        db.delete_table(u'idea_idealink')

        # Deleting model 'Idea'
        db.delete_table(u'idea_idea')

        # Removing M2M table for field images on 'Idea'
        db.delete_table(db.shorten_name(u'idea_idea_images'))

        # Removing M2M table for field links on 'Idea'
        db.delete_table(db.shorten_name(u'idea_idea_links'))


    models = {
        u'idea.idea': {
            'Meta': {'object_name': 'Idea'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['idea.IdeaImage']", 'symmetrical': 'False'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['idea.IdeaLink']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'what_for': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'what_kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['idea.IdeaType']"}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['neighborhood.Neighborhood']"})
        },
        u'idea.ideaimage': {
            'Meta': {'object_name': 'IdeaImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'idea.idealink': {
            'Meta': {'object_name': 'IdeaLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        }
    }

    complete_apps = ['idea']