class RoiAnswer:

    def roi(self):
        n=3
        rois = {
            "1": [n*x for x in [176, 181, 298, 35]],
            "2": [n*x for x in [477, 181, 298, 35]],
            "3": [n*x for x in [176, 215, 298, 35]],
            "4": [n*x for x in [477, 215, 298, 35]],
            "5": [n*x for x in [176, 253, 298, 35]],
            "6": [n*x for x in [477, 253, 298, 35]],
            "7": [n*x for x in [176, 287, 298, 35]],
            "8": [n*x for x in [477, 287, 298, 35]],
            "9": [n*x for x in [176, 325, 298, 35]],
            "10": [n*x for x in [477, 325, 298, 35]],
            "11": [n*x for x in [176, 359, 298, 35]],
            "12": [n*x for x in [477, 359, 298, 35]],
            "13": [n*x for x in [176, 397, 298, 35]],
            "14": [n*x for x in [477, 397, 298, 35]],
            "15": [n*x for x in [176, 431, 298, 35]],
            "16": [n*x for x in [477, 431, 298, 35]],
        }
        return rois

    rois_answer_voltage = ["Wiring", "Min. Measured Secondary Voltage [V]", "VT Primary L-L Voltage [V]", 
                        "VT Secondary L-L Voltage [V]", "Primary Reference Voltage [V]", "Sliding Reference Voltage",
                        "Rotating Sequence"
                        ]
    rois_answer_current = ["CT Primary Current [A]", "CT Secondary Current [A]", "Reference Current [A]", "Min. Measured Current [mA]",
                        "TDD Reference Selection", "TDD Nominal Current [A]"]