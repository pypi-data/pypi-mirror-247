import sys
import time

from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from tools.debug_logger import DebugLogger as logger
from ver.helpers import svc
from ver.helpers.cmd_runner import CmdRunner
from ver.helpers.logger_mock import Logger


# --------------------
class Helper:

    # --------------------
    def __init__(self):
        self.gui_process = None

        self.button1_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        self.label1_path = ['window1', 'page1_frame', 'button_frame', 'label1']
        self.menu_clear_path = [2]
        self.file_exit_path = [1, 2]

    # --------------------
    def init(self):
        svc.logger = Logger()
        svc.th = GuiApiHarness()
        svc.th.init()

    # --------------------
    def term(self):
        svc.th.term()

    # --------------------
    def init_each_test(self, ptobj):
        logger.line('')
        svc.pytself = ptobj

    # --------------------
    def term_each_test(self):
        svc.helper.kill_process()
        svc.pytself.assertFalse(self.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {svc.logger.lines}')

    # --------------------
    def start_process(self, args=''):
        svc.logger.info(f'start_process: {args}')
        self.gui_process = CmdRunner()
        cmd = ''
        if sys.platform == 'win32':
            cmd = 'bash '
        cmd += f'ver/do_gui.sh {args}'
        self.gui_process.start_task_bg('gui', cmd, working_dir='.')
        # show it off for a bit
        time.sleep(1)

    # --------------------
    def kill_process(self):
        svc.logger.info('kill_process')
        self.gui_process.finish()

    # --------------------
    def clean_shutdown(self):
        # do a clean exit of the GUI using File | Exit
        self.click_file_exit_menuitem()
        time.sleep(0.500)
        svc.th.term()

    # --------------------
    @property
    def label1_text(self):
        item = svc.th.search(self.label1_path)
        return item['value']

    # --------------------
    def click_button1(self):
        svc.th.click_left(self.button1_path)

    # --------------------
    def click_clear_menuitem(self):
        svc.th.menu_click(self.menu_clear_path)

    # --------------------
    def click_file_exit_menuitem(self):
        svc.th.menu_click(self.file_exit_path)
