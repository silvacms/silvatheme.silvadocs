
from silva.system.utils.script import NEED_SILVA_SESSION
from silva.pas.base.interfaces import IPASService

from Products.Silva.ExtensionRegistry import extensionRegistry

import logging

logger = logging.getLogger('silva.fix_pas')


class FixPASCommand(object):
    """ Reinstall silva.pas.base member service if needed
    """
    flags = NEED_SILVA_SESSION

    def get_options(self, factory):
        parser = factory(
            'fix_pas',
            help="reinstall silva.pas.base member service if needed")
        parser.add_argument(
            "paths", nargs="+",
            help="path to Silva sites to work on")
        parser.set_defaults(plugin=self)

    def run(self, root, options):
        if not IPASService.providedBy(root.service_members):
            root.manage_delObjects(['service_members'])
            if extensionRegistry.get_extension('silva.pas.base') is not None:
                from silva.pas.base.subscribers import configure_service

                factory = root.manage_addProduct['silva.pas.base']
                factory.manage_addMemberService()
                configure_service(root, None)
                logger.info('member service updated.')
            else:
                logger.error('silva.pas.base not installed.')
        else:
            logger.info('member service already present. nothing do to.')


from five import grok
from silva.core.views import views as silvaviews
from silva.core.interfaces import IRoot

class Run(silvaviews.View):
    grok.name('update_service_member')
    grok.require('zope2.ViewManagementScreens')
    grok.context(IRoot)

    def update(self):
        FixPASCommand().run(self.context, None)

    def render(self):
        return '<p>updated.</p>'
