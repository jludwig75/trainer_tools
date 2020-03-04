import os


class StartScript:
    def install(self):
        while True:
            print('Start-up modes')
            print(' 1 - Controll fan speed by heart rate')
            print(' 2 - Control lights by power')
            print(' 3 - Both')
            print('Select mode: ', end='')
            option = input()
            try:
                option = int(option)
            except:
                print('%s is not a valid option' % option)
                continue
            if option < 1 or option > 3:
                print('%u is not a valid option' % option)
                continue
            break
        assert option >= 1 and option <= 3
        if os.path.exists('start_script'):
            os.unlink('start_script')
        if option == 1:
            os.symlink('hr_controlled_fan.py', 'start_script')
        elif option == 2:
            os.symlink('power_controlled_lights.py', 'start_script')
        elif option == 3:
            os.symlink('control_fan_and_lights.py', 'start_script')
