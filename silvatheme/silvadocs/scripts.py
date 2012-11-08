
from silva.system.utils.script import NEED_SILVA_SESSION
from silva.core.services.interfaces import IMemberService

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
        if not IMemberService.providedBy(root.service_members):
            root.manage_delObjects(['service_members'])
            if extensionRegistry.get_extension('silva.pas.base') is not None:
                from silva.pas.base.subscribers import configure_service

                factory = root.manage_addProduct['silva.pas.base']
                factory.manage_addMemberService()
                configure_service(root, None)
                logger.info('member service updated.')
            else:
                factory = root.manage_addProduct['Silva']
                factory.manage_addSimpleMemberService()
                logger.info('member service created.')
        else:
            logger.info('member service already present. nothing do to.')
