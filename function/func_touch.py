import time
import time

from function.func_connection import ConnectionManager
from config.config_touch import ConfigTouch as ect

class TouchManager:

    connect_manager = ConnectionManager()
    hex_value = int("A5A5", 16)

    def __init__(self):
        pass

    def touch_write(self, address, value, delay=0.6):
        attempt = 0
        while attempt < 2:
            self.connect_manager.touch_client.write_register(address, value)
            read_value = self.connect_manager.touch_client.read_holding_registers(address)
            time.sleep(delay)
            if read_value == value:
                print("\nTouched")
                return
            else:
                attempt += 1

    def uitest_mode_start(self):
        if self.connect_manager.touch_client:
            self.touch_write(ect.touch_addr_ui_test_mode.value, 1)
        else:
            print("client Error")

    def screenshot(self):
        if self.connect_manager.touch_client:
            self.touch_write(ect.touch_addr_screen_capture.value, self.hex_value)
        else:
            print("client Error")

    def touch_password(self):
        if self.connect_manager.touch_client:
            number0_x = 485
            number0_y = 290
            enter_x = 340
            enter_y = 350
            for i in range(4):
                self.touch_write(ect.touch_addr_pos_x.value, number0_x)
                self.touch_write(ect.touch_addr_pos_y.value, number0_y)
                self.touch_write(ect.touch_addr_touch_mode.value, 1)
                self.touch_write(ect.touch_addr_touch_mode.value, 0)
            self.touch_write(ect.touch_addr_pos_x.value, enter_x)
            self.touch_write(ect.touch_addr_pos_y.value, enter_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)

    def touch_menu(self, menu_key):
        if self.connect_manager.touch_client:
            data_view_x, data_view_y = menu_key
            self.touch_write(ect.touch_addr_pos_x.value, data_view_x)
            self.touch_write(ect.touch_addr_pos_y.value, data_view_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Menu Touch Error")

    def btn_popup_touch(self, btn_popup_key):
        if self.connect_manager.touch_client:
            btn_x, btn_y = self.config_touch[btn_popup_key]
            self.touch_write(ect.touch_addr_pos_x.value, btn_x)
            self.touch_write(ect.touch_addr_pos_y.value, btn_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.config_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.config_touch["btn_popup_enter"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Popup Touch Error")

    def number_1_touch(self, number_key):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(
                ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_2_touch(self, number_key1, number_key2):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_3_touch(self, number_key1, number_key2, number_key3):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_c, number_d = self.coords_touch[number_key3]
            self.touch_write(ect.touch_addr_pos_x.value, number_c)
            self.touch_write(ect.touch_addr_pos_y.value, number_d)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def btn_apply_touch(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_apply"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_apply"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Apply Touch Error")

    def btn_front_setup(self):
        if self.connect_manager.touch_client:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 2)
        else:
            print("Front setup button is clicked Error")

    def btn_front_meter(self):
        if self.connect_manager.touch_client:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 64)
        else:
            print("Front meter button is clicked Error")

    def btn_front_home(self):
        if self.connect_manager.touch_client:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 1)
        else:
            print("Front home button is clicked Error")
