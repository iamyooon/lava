# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-18 14:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0022_alter_imagechartfilter'),
        ('lava_scheduler_app', '0029_remove_testjob__results_bundle'),
        ('lava_results_app', '0014_xaxis_maxlength_increase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='buglink',
            name='test_result',
        ),
        migrations.RemoveField(
            model_name='buglink',
            name='test_runs',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='bundle_stream',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='bundlestream',
            name='group',
        ),
        migrations.RemoveField(
            model_name='bundlestream',
            name='user',
        ),
        migrations.RemoveField(
            model_name='image',
            name='filter',
        ),
        migrations.RemoveField(
            model_name='imagechartfilter',
            name='filter',
        ),
        migrations.RemoveField(
            model_name='imagechartfilter',
            name='image_chart',
        ),
        migrations.AlterUniqueTogether(
            name='imagecharttest',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagecharttest',
            name='image_chart_filter',
        ),
        migrations.RemoveField(
            model_name='imagecharttest',
            name='test',
        ),
        migrations.RemoveField(
            model_name='imagecharttestattribute',
            name='image_chart_test',
        ),
        migrations.AlterUniqueTogether(
            name='imagecharttestattributeuser',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagecharttestattributeuser',
            name='image_chart_test_attribute',
        ),
        migrations.RemoveField(
            model_name='imagecharttestattributeuser',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='imagecharttestcase',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagecharttestcase',
            name='image_chart_filter',
        ),
        migrations.RemoveField(
            model_name='imagecharttestcase',
            name='test_case',
        ),
        migrations.RemoveField(
            model_name='imagecharttestcaseattribute',
            name='image_chart_test_case',
        ),
        migrations.AlterUniqueTogether(
            name='imagecharttestcaseuser',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagecharttestcaseuser',
            name='image_chart_test_case',
        ),
        migrations.RemoveField(
            model_name='imagecharttestcaseuser',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='imagecharttestuser',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagecharttestuser',
            name='image_chart_test',
        ),
        migrations.RemoveField(
            model_name='imagecharttestuser',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='imagechartuser',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagechartuser',
            name='image_chart',
        ),
        migrations.RemoveField(
            model_name='imagechartuser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='imagereport',
            name='group',
        ),
        migrations.RemoveField(
            model_name='imagereport',
            name='image_report_group',
        ),
        migrations.RemoveField(
            model_name='imagereport',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='imagereportchart',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imagereportchart',
            name='image_report',
        ),
        migrations.RemoveField(
            model_name='imageset',
            name='images',
        ),
        migrations.AlterUniqueTogether(
            name='namedattribute',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='namedattribute',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='pmqabundlestream',
            name='bundle_stream',
        ),
        migrations.DeleteModel(
            name='SoftwarePackageScratch',
        ),
        migrations.AlterUniqueTogether(
            name='testcase',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='testcase',
            name='test',
        ),
        migrations.DeleteModel(
            name='TestDefinition',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='test_case',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='test_run',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='bundle',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='devices',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='packages',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='sources',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='test',
        ),
        migrations.DeleteModel(
            name='SoftwarePackage',
        ),
        migrations.AlterUniqueTogether(
            name='testrunfilter',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='testrunfilter',
            name='bundle_streams',
        ),
        migrations.RemoveField(
            model_name='testrunfilter',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='testrunfilter',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='testrunfilterattribute',
            name='filter',
        ),
        migrations.AlterUniqueTogether(
            name='testrunfiltersubscription',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='testrunfiltersubscription',
            name='filter',
        ),
        migrations.RemoveField(
            model_name='testrunfiltersubscription',
            name='user',
        ),
        migrations.RemoveField(
            model_name='testrunfiltertest',
            name='filter',
        ),
        migrations.RemoveField(
            model_name='testrunfiltertest',
            name='test',
        ),
        migrations.RemoveField(
            model_name='testrunfiltertestcase',
            name='test',
        ),
        migrations.RemoveField(
            model_name='testrunfiltertestcase',
            name='test_case',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.DeleteModel(
            name='BugLink',
        ),
        migrations.DeleteModel(
            name='Bundle',
        ),
        migrations.DeleteModel(
            name='BundleDeserializationError',
        ),
        migrations.DeleteModel(
            name='BundleStream',
        ),
        migrations.DeleteModel(
            name='HardwareDevice',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='ImageChartFilter',
        ),
        migrations.DeleteModel(
            name='ImageChartTest',
        ),
        migrations.DeleteModel(
            name='ImageChartTestAttribute',
        ),
        migrations.DeleteModel(
            name='ImageChartTestAttributeUser',
        ),
        migrations.DeleteModel(
            name='ImageChartTestCase',
        ),
        migrations.DeleteModel(
            name='ImageChartTestCaseAttribute',
        ),
        migrations.DeleteModel(
            name='ImageChartTestCaseUser',
        ),
        migrations.DeleteModel(
            name='ImageChartTestUser',
        ),
        migrations.DeleteModel(
            name='ImageChartUser',
        ),
        migrations.DeleteModel(
            name='ImageReport',
        ),
        migrations.DeleteModel(
            name='ImageReportChart',
        ),
        migrations.DeleteModel(
            name='ImageReportGroup',
        ),
        migrations.DeleteModel(
            name='ImageSet',
        ),
        migrations.DeleteModel(
            name='NamedAttribute',
        ),
        migrations.DeleteModel(
            name='PMQABundleStream',
        ),
        migrations.DeleteModel(
            name='SoftwareSource',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='TestCase',
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
        migrations.DeleteModel(
            name='TestRun',
        ),
        migrations.DeleteModel(
            name='TestRunDenormalization',
        ),
        migrations.DeleteModel(
            name='TestRunFilter',
        ),
        migrations.DeleteModel(
            name='TestRunFilterAttribute',
        ),
        migrations.DeleteModel(
            name='TestRunFilterSubscription',
        ),
        migrations.DeleteModel(
            name='TestRunFilterTest',
        ),
        migrations.DeleteModel(
            name='TestRunFilterTestCase',
        ),
    ]