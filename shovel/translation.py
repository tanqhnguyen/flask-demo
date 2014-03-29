from babel.messages import frontend as babel
from distutils.dist import Distribution
from shovel import task
import os
import config

#import config

dist = Distribution(dict(
        name='DevZoneVN',
        version='0.1'
    ))
messages_pot = os.path.join('translations', 'messages.pot')

@task
def extract():
    cmd = babel.extract_messages(dist)
    cmd.output_file = messages_pot
    cmd.mapping_file = os.path.join('babel.cfg')
    cmd.keywords = "lazy_gettext"
    cmd.input_dirs = 'simple_page,social_auth,public'

    cmd.finalize_options()
    cmd.run()

@task
def init():
    for locale in config.LANGUAGES.keys():
        cmd = babel.init_catalog(dist)
        cmd.input_file = messages_pot
        cmd.output_dir = 'translations'
        cmd.locale = locale

        cmd.finalize_options()
        cmd.run()

@task
def update():
    cmd = babel.update_catalog(dist)
    cmd.input_file = messages_pot
    cmd.output_dir = 'translations'

    cmd.finalize_options()
    cmd.run()

@task
def compile():
    cmd = babel.compile_catalog(dist)
    cmd.directory = 'translations'

    cmd.finalize_options()
    cmd.run()

@task
def setup():
    extract()
    init()
    compile()

@task
def generate():
    update()