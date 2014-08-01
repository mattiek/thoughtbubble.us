# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OrganizationImage.active'
        db.add_column(u'organization_organizationimage', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OrganizationImage.active'
        db.delete_column(u'organization_organizationimage', 'active')


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
        u'organization.organization': {
            'Meta': {'ordering': "['order']", 'object_name': 'Organization'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'organization_curator'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['organization.OrganizationCurator']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['thoughtbubble.ThoughtbubbleUser']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['partner.Partner']", 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['places.Place']", 'null': 'True', 'blank': 'True'}),
            'sherlock_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('place',)", 'max_length': '50', 'populate_from': "'title'"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'organization.organizationcurator': {
            'Meta': {'object_name': 'OrganizationCurator'},
            'curator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thoughtbubble.ThoughtbubbleUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.OrganizationCuratorRole']", 'null': 'True', 'blank': 'True'})
        },
        u'organization.organizationcuratorrole': {
            'Meta': {'object_name': 'OrganizationCuratorRole'},
            'authority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'organization.organizationimage': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'OrganizationImage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"})
        },
        u'organization.organizationnews': {
            'Meta': {'object_name': 'OrganizationNews'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']"})
        },
        u'partner.partner': {
            'Meta': {'object_name': 'Partner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'places.county': {
            'Meta': {'ordering': "['name']", 'object_name': 'County'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'places.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'county_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['places.County']", 'null': 'True'}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "('state',)", 'max_length': '50', 'populate_from': "'name'"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {})
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

    complete_apps = ['organization']