# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Place.zip_code'
        db.alter_column(u'places_place', 'zip_code', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'Place.zip_code'
        db.alter_column(u'places_place', 'zip_code', self.gf('django.db.models.fields.FloatField')())

    models = {
        u'places.place': {
            'Meta': {'object_name': 'Place'},
            'county': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "'central'", 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['places']