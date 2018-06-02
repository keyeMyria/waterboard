# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from django import forms

from .models import Attribute, AttributeGroup, AttributeOption


class GroupForm(forms.Form):
    def __init__(self, attribute_group, webuser, *args, **kwargs):
        self.group_label = attribute_group.label
        self.group_key = attribute_group.key

        super(GroupForm, self).__init__(*args, **kwargs)

        if not webuser.is_staff:
            grants = {key: values for key, values in webuser.grant_set.all().values_list('key', 'values')}
        else:
            grants = {}

        attributes = (
            Attribute.objects
            .filter(attribute_group=attribute_group)
            .order_by('attribute_group__position', 'position')
        )

        for attr in attributes:
            if attr.result_type == 'Integer':
                self.fields[attr.key] = forms.IntegerField(required=attr.required)

            elif attr.result_type == 'Decimal':
                self.fields[attr.key] = forms.DecimalField(decimal_places=8, required=attr.required)

            elif attr.result_type == 'Text':
                self.fields[attr.key] = forms.CharField(max_length=512, required=attr.required)

            elif attr.result_type == 'DropDown':

                if attr.key in grants:
                    attributeoptions = (
                        AttributeOption.objects
                        .filter(attribute_id=attr.id, option__in=grants[attr.key])
                        .order_by('position')
                    )
                else:
                    attributeoptions = AttributeOption.objects.filter(attribute_id=attr.id).order_by('position')

                criteria_information = []
                for attropt in attributeoptions:
                    criteria_information.append(
                        '<b>%s</b></br>%s<br>' % (attropt.option, attropt.description.replace('"', '\''))
                    )

                self.fields[attr.key] = forms.TypedChoiceField(
                    choices=[(attropt.value, attropt.option) for attropt in attributeoptions],
                    label='<b>%s</b> <span class="question-mark" help="%s">?<span>' % (
                        attr.key, '<br>'.join(criteria_information)
                    ),
                    coerce=int,
                    required=attr.required
                )

            elif attr.result_type == 'MultipleChoice':
                attributeoptions = AttributeOption.objects.filter(attribute_id=attr.id).order_by('position')

                self.fields[attr.key] = forms.MultipleChoiceField(
                    choices=[(attropt.value, attropt.option) for attropt in attributeoptions],
                    required=attr.required
                )


class AttributeForm(forms.Form):
    _feature_uuid = forms.CharField(max_length=100, widget=forms.HiddenInput())

    def __init__(self, webuser, *args, **kwargs):
        super(AttributeForm, self).__init__(*args, **kwargs)
        group_data = self.group_attributes(kwargs)

        self.groups = []

        for attribute_group in AttributeGroup.objects.order_by('position').all():
            form_kwargs = dict(initial=self.initial, attribute_group=attribute_group, webuser=webuser)

            if group_data:
                form_kwargs.update(data=group_data.get(attribute_group.key, {}))

            group_form = GroupForm(**form_kwargs)

            self.groups.append(group_form)

    @staticmethod
    def group_attributes(kwargs):
        group_data = {}

        if 'data' in kwargs:
            attribute_keys = [
                compound_key for compound_key in kwargs['data'].keys() if not (compound_key.startswith('_'))
            ]

            for compound_key in attribute_keys:
                group_label, attribute_key = compound_key.split('/')

                if group_label not in group_data:
                    group_data[group_label] = {}

                group_data[group_label].update({attribute_key: kwargs['data'][compound_key]})

        return group_data

    def full_clean(self):
        # clean main form
        super(AttributeForm, self).full_clean()

        # also clean all group forms
        for group in self.groups:
            group.full_clean()

    def is_valid(self):

        # main form (_feature_uuid, ...)
        main_form = [self.is_bound and not self.errors]
        # group forms
        group_forms = [form.is_bound and not form.errors for form in self.groups]

        # check if all forms are valid
        return all(itertools.chain(main_form, group_forms))


class CreateFeatureForm(forms.Form):

    def __init__(self, webuser, *args, **kwargs):
        super(CreateFeatureForm, self).__init__(*args, **kwargs)
        group_data = self.group_attributes(kwargs)

        self.groups = []

        for attribute_group in AttributeGroup.objects.order_by('position').all():
            form_kwargs = dict(initial=self.initial, attribute_group=attribute_group, webuser=webuser)

            if group_data:
                form_kwargs.update(data=group_data.get(attribute_group.key, {}))

            group_form = GroupForm(**form_kwargs)

            self.groups.append(group_form)

    @staticmethod
    def group_attributes(kwargs):
        group_data = {}

        if 'data' in kwargs:

            attributes = Attribute.objects.select_related('attribute_group').order_by('attribute_group__position').all()

            for attribute in attributes:

                group_label = attribute.attribute_group.key

                if group_label not in group_data:
                    group_data[group_label] = {}

                group_data[group_label].update({attribute.key: kwargs['data'][attribute.key]})

        return group_data

    def full_clean(self):
        # clean main form
        super(CreateFeatureForm, self).full_clean()

        # also clean all group forms
        for group in self.groups:
            group.full_clean()

    def is_valid(self):

        # main form (_feature_uuid, ...)
        main_form = [self.is_bound and not self.errors]
        # group forms
        group_forms = [form.is_bound and not form.errors for form in self.groups]

        # check if all forms are valid
        return all(itertools.chain(main_form, group_forms))
