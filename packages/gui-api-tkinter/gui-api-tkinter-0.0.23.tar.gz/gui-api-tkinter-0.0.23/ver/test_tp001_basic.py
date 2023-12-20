import unittest

from pytest_ver import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp001(unittest.TestCase):

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()
        svc.helper = Helper()
        svc.helper.init()

    # -------------------
    def setUp(self):
        svc.helper.init_each_test(self)

    # -------------------
    def tearDown(self):
        svc.helper.term_each_test()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        svc.helper.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp001(self):
        pth.proto.protocol('tp-001', 'basic server tests')
        pth.proto.add_objective('check server connect and disconnect')
        pth.proto.add_objective('check get_screen gets screen content of GUI')
        pth.proto.add_objective('check click successfully clicks a button')
        pth.proto.add_objective('check menu items can be invoked')
        pth.proto.add_objective('check callback function can be invoked')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{svc.th.version}')

        pth.proto.step('start gui')
        svc.helper.start_process()
        pth.ver.verify_true(svc.helper.gui_process.is_alive())
        pth.ver.verify_false(svc.th.is_connected(), reqids=['SRS-001', 'SRS-030'])

        pth.proto.step('connect harness to GUI App server')
        svc.th.connect()
        pth.ver.verify_true(svc.th.is_connected(), reqids=['SRS-001', 'SRS-004'])

        pth.proto.step('get page content')
        svc.th.get_screen()
        pth.ver.verify_gt(len(svc.th.content), 0, reqids=['SRS-020', 'SRS-032', 'SRS-021'])

        pth.proto.step('check initial state of the label')
        pth.ver.verify_equal(svc.helper.label1_text, 'state: 0', reqids=['SRS-050', 'SRS-022', 'SRS-023'])

        pth.proto.step('click a button')
        svc.helper.click_button1()
        svc.th.get_screen()
        pth.ver.verify_equal(svc.helper.label1_text, 'state: 1', reqids=['SRS-050', 'SRS-051'])

        pth.proto.step('click "Clear" menu item')
        svc.helper.click_clear_menuitem()
        svc.th.get_screen()
        pth.ver.verify_equal(svc.helper.label1_text, 'state: 0', reqids=['SRS-060', 'SRS-062', 'SRS-061'])

        pth.proto.step('send "cmd01" command')
        cmd = {
            'cmd': 'cmd01',
            'param1': 'some parameter1',
            'param2': 'some parameter2',
        }
        rsp = svc.th.send_recv(cmd)
        pth.ver.verify_equal(rsp['value'], 'ack', reqids=['SRS-010', 'SRS-032'])

        pth.proto.step('disconnect from GUI API server')
        svc.helper.clean_shutdown()
        pth.ver.verify_false(svc.th.is_connected(), reqids=['SRS-003', 'SRS-031'])
