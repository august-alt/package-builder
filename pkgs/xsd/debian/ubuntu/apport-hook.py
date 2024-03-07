'''apport package hook for xsdcxx

Author: Jörg Frings-Fürst <ubuntu@jff-webhosting.net>
'''

from apport.hookutils import *

def add_info(report):
    attach_dmesg(report)
    attach_hardware(report)
    attach_related_packages(report, packages)
    
