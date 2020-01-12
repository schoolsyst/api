import re
import os
import json
from restore import *
from termcolor import cprint


#
# Utility to change a func's __repr__
# 

import functools
class reprwrapper(object):
    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)
    def __call__(self, *args, **kw):
        return self._func(*args, **kw)
    def __repr__(self):
        return self._repr(self._func)

def withrepr(reprfun):
    def _wrap(func):
        return reprwrapper(reprfun, func)
    return _wrap

#
# 

class Migrator:
  def __init__(self, model, filename, mutate=True, verbose=True):
    if verbose:
      cprint(f'\nModel {model}\n' + '=' * int(len(f'Model {model}')/2), 'yellow', attrs=['bold'])

    self.mutate = mutate
    self.verbose = verbose

    self.full_model = model
    self.app_label, self.model = model.split('.')
    self.filename = filename

    self.orig_raw = None

  def __enter__(self, *args, **kwargs): 
    self.entries = self.load_datadump()
    return self
  def __exit__(self, *args, **kwargs):
    self.write_datadump(None, True, indent=2)

  
  def load_datadump(self):
    with open(self.filename+'.bak', 'r') as file:
      raw = file.read()
    self.orig_raw = raw
    
    parsed = json.loads(raw)
    cleansed = self.strip_models(parsed, ['sessions.session', 'admin.logentry'])

    if self.verbose:
      cprint(f"Loaded {self.filename}.", attrs=['bold'])
    return cleansed

  def write_datadump(self, filename=None, backup=False, **json_dump_options):
    json_dump_options = json_dump_options or {}
    filename = filename or self.filename

    parsed = self.entries
    raw = json.dumps(parsed, **json_dump_options)
    with open(filename, 'w') as file:
      file.write(raw)
    
    if backup:
      self.write_backup()
    
    if self.verbose:
      cprint(f'Written changes to {filename}', attrs=['bold'])
    return raw

  def write_backup(self, filename=None):
    filename = filename or self.filename+'.bak'
    with open(filename, 'w') as file:
      file.write(self.orig_raw)
      if self.verbose:
        cprint(f'Written backup as {filename}', attrs=['bold'])

  def rename_model(self, new_name):
    entries = self.entries
    counter = 0
    app_label, model = new_name.split('.')

    for (i, entry) in enumerate(self.entries):
      # Modify contenttypes
      if entry['model'] == 'contenttypes.contenttype':
        a, m = self.get_entry_fields(entry, as_tuple=True)
        if a == app_label and m == model:
          entries[i]['fields']['app_label'] = app_label
          entries[i]['fields']['model'] = model

      # Modify the model entries itselves
      if entry['model'] == self.full_model:
          entries[i]['model'] = new_name

      # Increment counter
      counter += 1
    
    self.full_model = new_name
    print(f'[ {counter:4} ]', end=' ')
    self.model = model
    self.app_label = app_label

    if self.verbose:
      cprint(f'Renamed model to {new_name}', 'magenta')
    if self.mutate:
      self.entries = entries
    return entries

  def rename_field(self, old_name, new_name):
    entries = self.entries
    counter = 0
    for (i, entry) in enumerate(self.entries):
      if entry['model'] == self.full_model:
        if old_name in self.get_entry_fields(entry).keys():
          value = entry['fields'][old_name]
          del entries[i]['fields'][old_name]
          entries[i]['fields'][self.handle_callable(new_name, entry, old_name)] = value

      # Increment counter
      counter += 1

    if self.verbose and counter:
      print(f'[ {counter:4} ]', end=' ')
      cprint(f'Renamed field {old_name} to {new_name}', 'cyan')
    if self.mutate:
      self.entries = entries
    return entries

  def add_field(self, name, value=None):
    entries = self.entries
    counter = 0
    for (i, entry) in enumerate(self.entries):
      if entry['model'] == self.full_model:
        entries[i]['fields'][name] = self.handle_callable(value, entry, None)

      # Increment counter
      counter += 1
    
    if self.verbose and counter:
      print(f'[ {counter:4} ]', end=' ')
      cprint(f'Added field {name} with value {value.__repr__()}', 'green')
    if self.mutate:
      self.entries = entries
    return entries

  def delete_field(self, name, condition = lambda value, fields: True):
    entries = self.entries
    counter = 0
    for (i, entry) in enumerate(self.entries):
      if entry['model'] == self.full_model:
        if name in self.get_entry_fields(entry).keys():
          if condition(entry['fields'][name], entry['fields']):
            del entries[i]['fields'][name]
            # Increment counter
            counter += 1
    
    if self.verbose and counter:
      print(f'[ {counter:4} ]', end=' ')
      cprint(f'Deleted field {name}', 'red')
    if self.mutate:
      self.entries = entries
    return entries
 
  def set_field(self, field, value):
    entries = self.entries
    counter = 0
    for (i, entry) in enumerate(self.entries):
      if entry['model'] == self.full_model:
        if field in self.get_entry_fields(entry).keys():
          entry['fields'][field] = self.handle_callable(value, entry, field)

      # Increment counter
      counter += 1
    
    if self.verbose and counter:
      print(f'[ {counter:4} ]', end=' ')
      cprint(f'Set field {field} to {value}', 'blue')
    if self.mutate:
      self.entries = entries
    return entries

  def get_field(self, predicate, field_name=None):
    for (i, entry) in enumerate(self.entries):
      if predicate(entry):
        return entry['fields'].get(field_name, None) if field_name else entry

  def get_entry_fields(self, entry, as_tuple=False):
    fields = entry.get('fields', {})
    return tuple(fields.values()) if as_tuple else fields
  
  def handle_callable(self, maybe_callable, entry, field=None):
    fields = entry['fields']
    if field is None: 
      value = None
    else:
      value = fields.get(field, None)

    if callable(maybe_callable):
      return maybe_callable(value, fields)
    else:
      return maybe_callable

  
  def strip_models(self, json_content, models_to_strip):
    filtered_entries = json_content
    for i, entry in enumerate(json_content):
      if entry['model'] in models_to_strip:
        del filtered_entries[i]
    
    return filtered_entries

FILE = 'datadump.json'
@withrepr(lambda f: f'[ invert_bool ]')
def invert_bool(value, fields):
  return not value

def slug_from(using_field):
  from slugify import slugify
  @withrepr(lambda f: f"[ slug_from {using_field.__repr__()} ]")
  def _make_slug(value, fields):
    return slugify(fields[using_field])
  return _make_slug

def use(func, apply_as="function", *args, **kwargs):
  @withrepr(lambda f: f"[ {'.' if apply_as == 'method' else ''}{func.__name__} ]")
  def transformer(value, fields):
    if apply_as == 'function':
      return func(value, *args, **kwargs)
    elif apply_as == 'method':
      return value.func(*args, **kwargs)
  return transformer

@withrepr(lambda f: f"[ uppercase ]")
def uppercase(value, fields):
  if type(value) is not str:
    return value
  return value.upper()

@withrepr(lambda f: f"[ lowercase ]")
def lowercase(value, fields):
  if type(value) is not str:
    return value
  return value.lowercase()

from datetime import datetime
iso_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def default(default_value, needs_a_default = lambda value, fields: value is None):
  @withrepr(lambda f: f"[ default {default_value.__repr__()} ]")
  def transformer(value, fields):
    if needs_a_default(value, fields):
      return default_value
    else:
      return value
  return transformer

with Migrator('common.defaultsetting', FILE) as m:
  m.rename_field('required', 'optional')
  m.set_field('optional', invert_bool)
  m.rename_field('kind', 'type')
  m.rename_field('namespace', 'category')
  m.rename_model('common.settingdefinition')

with Migrator('common.subject', FILE) as m:
  m.delete_field('abbreviation')
  m.delete_field('physical_weight')
  m.rename_field('grade_weight', 'weight')
  m.rename_field('grade_goal', 'goal')
  m.set_field('slug', slug_from('name'))
  m.set_field('weight', default(1))
  
with Migrator('learn.note', FILE) as m:
  m.rename_field('filetype', 'format')
  m.set_field('format', uppercase)
  m.rename_field('last_modifier', 'modified')
  m.rename_field('created', 'added')
  m.add_field('opened', iso_now)

with Migrator('learn.grade', FILE) as m:
  m.delete_field('test')
  m.rename_field('actual', 'obtained')
  m.rename_field('maximum', 'unit')

with Migrator('schedule.exercise', FILE) as m:
  m.delete_field('event')
  m.rename_field('completed', 'progress')
  m.set_field('progress', lambda v,f: float(v))
  m.rename_field('created', 'added')
  m.add_field('completed', iso_now)
  m.rename_field('notes', 'details')
  m.add_field('type', 'EXERCISE')
  m.rename_model('homework.homework')

with Migrator('learn.test', FILE) as m:
  m.add_field('progress', 0.0)
  m.rename_field('created', 'added')
  m.add_field('completed', iso_now)
  m.delete_field('notes')
  m.add_field('type', 'TEST')
  m.rename_model('homework.homework')

