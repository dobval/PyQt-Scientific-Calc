"""
Author: Dobromir Valentinov
Fac. No: 201223004
Description: A scientific python GUI calculator, using PyQt
Last modified: 07/04/2024
"""

# Encoding: utf-8
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import math
import operator

from MainWindow import Ui_MainWindow

# Calculator state variables
READY = 0  # Ready to start a new operation. Default state
INPUT = 1  # In the middle of an operation, accepting input
INV = False
# Main Window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Setup numbers
        for i in range(10):
            getattr(self, f'pushButton{i}').pressed.connect(lambda v=i: self.input_number(v))

        # Setup arithmetic operations
        self.pushButtonAdd.pressed.connect(lambda: self.operation(operator.add))
        self.pushButtonSubstract.pressed.connect(lambda: self.operation(operator.sub))
        self.pushButtonMultiply.pressed.connect(lambda: self.operation(operator.mul))
        self.pushButtonDivide.pressed.connect(lambda: self.operation(operator.truediv))  # operator.div for Python2.7
        ''' The lambda lines are equivalent to the example:
            def add():
                self.operation(operator.add)'''
        self.pushButtonEquals.pressed.connect(self.equals)

        # Setup non-scientific operations
        self.pushButtonSign.pressed.connect(self.operation_sign)
        self.pushButtonSqrt.pressed.connect(self.operation_sqrt)
        self.pushButtonPercent.pressed.connect(self.operation_pc)
        self.pushButtonReciprocal.pressed.connect(self.reciprocal)

        # Setup memory operations
        self.pushButtonMC.pressed.connect(self.memory_clear)
        self.pushButtonMR.pressed.connect(self.memory_recall)
        self.pushButtonMS.pressed.connect(self.memory_store)
        self.pushButtonMAdd.pressed.connect(self.memory_add)
        self.pushButtonMMinus.pressed.connect(self.memory_substract)
        self.pushButtonClear.pressed.connect(self.clear)
        self.pushButtonCE.pressed.connect(self.clear_entry)

        self.memory = 0  # Memory variable
        self.clear()

        # Setup decimal point
        self.pushButtonDecPoint.pressed.connect(self.decimal_point)

        # Setup "scientific" operations
        self.pushButtonInt.pressed.connect(self.integer_part)
        self.pushButtonFactorial.pressed.connect(self.factorial)
        self.pushButtonRootY.pressed.connect(self.root_y)
        self.pushButtonRoot3.pressed.connect(self.cube_root)
        self.pushButton10Power.pressed.connect(self.power_of_ten)

        self.pushButtonPI.pressed.connect(self.pi)
        self.pushButtonPower2.pressed.connect(self.power2)
        self.pushButtonPowerY.pressed.connect(self.power_y)
        self.pushButtonPower3.pressed.connect(self.power3)
        self.pushButtonLog.pressed.connect(self.log)

        self.pushButtonLn.pressed.connect(self.ln)
        self.pushButtonSin.pressed.connect(self.sin)
        self.pushButtonCos.pressed.connect(self.cos)
        self.pushButtonTan.pressed.connect(self.tan)
        self.pushButtonMod.pressed.connect(self.mod)

        self.pushButtonInv.pressed.connect(self.inv)
        self.pushButtonSinH.clicked.connect(self.sinh)
        self.pushButtonCosH.clicked.connect(self.cosh)
        self.pushButtonTanH.clicked.connect(self.tanh)
        self.pushButtonExp.pressed.connect(self.exp)

        self.show()

    # Mapping the keyboard numpad to buttons
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9]:
            key_num = event.key() - Qt.Key_0
            self.input_number(key_num)
        elif event.key() == Qt.Key_Plus:
            self.operation(operator.add)
        elif event.key() == Qt.Key_Minus:
            self.operation(operator.sub)
        elif event.key() == Qt.Key_Asterisk:
            self.operation(operator.mul)
        elif event.key() == Qt.Key_Slash:
            self.operation(operator.truediv)
        elif event.key() == Qt.Key_Period:
            self.input_number('.')
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.equals()

    def display(self):
        self.lcdNumber.display(self.stack[-1])

    def memory_clear(self):
        self.memory = 0

    def memory_recall(self):
        self.state = INPUT
        self.stack[-1] = self.memory
        self.display()

    def memory_store(self):
        self.memory = self.lcdNumber.value()

    def memory_add(self):
        self.memory += self.lcdNumber.value()

    def memory_substract(self):
        self.memory -= self.lcdNumber.value()

    def clear_entry(self):
        if self.state == INPUT:
            self.state = READY
            self.stack[-1] = 0
        self.display()

    def clear(self):
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def operation_sign(self):
        self.state = INPUT
        self.stack[-1] = -self.stack[-1]
        self.display()

    def operation_sqrt(self):
        self.state = INPUT
        self.stack[-1] = math.sqrt(self.stack[-1])
        self.display()

    def operation_pc(self):
        self.state = INPUT
        self.stack[-1] *= 0.01
        self.display()

    def reciprocal(self):
        self.state = INPUT
        self.stack[-1] = 1 / self.stack[-1]
        self.display()

    # More "scientific" operations
    def integer_part(self):
        self.state = INPUT
        self.stack[-1] = int(self.stack[-1])
        self.display()

    def factorial(self):
        self.state = INPUT
        try:
            # Converts to string for calculation (without string didn't work)
            result = str(math.factorial(self.stack[-1]))
            self.stack[-1] = float(result)
        except OverflowError:
            # Result too large, error message
            result = "Result too large"
        self.lcdNumber.display(result)
        self.display()

    def root_y(self):
        if self.current_op:  # Completes the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = self.root_operation

    def root_operation(self, x, y):  # Used with root_y function
        return math.pow(x, 1/y)

    def cube_root(self):
        self.state = INPUT
        self.stack[-1] = self.stack[-1] ** (1/3)
        self.display()

    def power_of_ten(self):
        self.state = INPUT
        self.stack[-1] = 10 ** self.stack[-1]
        self.display()

    def pi(self):
        self.state = INPUT
        self.stack[-1] = math.pi
        self.display()

    def power2(self):
        self.state = INPUT
        self.stack[-1] = math.pow(self.stack[-1], 2)
        self.display()

    def power_y(self):
        if self.current_op:  # Completes the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = math.pow

    def power3(self):
        self.state = INPUT
        self.stack[-1] = math.pow(self.stack[-1], 3)
        self.display()

    def log(self):
        self.state = INPUT
        self.stack[-1] = math.log10(self.stack[-1])
        self.display()

    def ln(self):
        self.state = INPUT
        self.stack[-1] = math.log(self.stack[-1])
        self.display()

    def sin(self):
        global INV
        self.state = INPUT
        if INV:
            if self.radioButtonDeg.isChecked():
                try:
                    self.stack[-1] = math.degrees(math.asin(self.stack[-1]))
                except ValueError:
                    self.stack[-1] = 0
                    self.lcdNumber.display('Err')
                    return
            else:
                try:
                    self.stack[-1] = math.asin(self.stack[-1])
                except ValueError:
                    self.stack[-1] = 0
                    self.lcdNumber.display('Err')
                    return
        else:
            if self.radioButtonDeg.isChecked():
                self.stack[-1] = math.sin(math.radians(self.stack[-1]))
            else:
                self.stack[-1] = math.sin(self.stack[-1])
        self.display()

    def cos(self):
        global INV
        self.state = INPUT
        if INV:
            if self.radioButtonDeg.isChecked():
                try:
                    self.stack[-1] = math.degrees(math.acos(self.stack[-1]))
                except ValueError:
                    self.stack[-1] = 0
                    self.lcdNumber.display('Err')
                    return
            else:
                try:
                    self.stack[-1] = math.acos(self.stack[-1])
                except ValueError:
                    self.stack[-1] = 0
                    self.lcdNumber.display('Err')
                    return
        else:
            if self.radioButtonDeg.isChecked():
                self.stack[-1] = math.cos(math.radians(self.stack[-1]))
            else:
                self.stack[-1] = math.cos(self.stack[-1])
        self.display()

    def tan(self):
        global INV
        self.state = INPUT
        if INV:
            if self.radioButtonDeg.isChecked():
                try:
                    self.stack[-1] = math.degrees(math.atan(self.stack[-1]))
                except ValueError:
                    self.stack[-1] = 0
                    self.lcdNumber.display('Err')
                    return
            else:
                try:
                    self.stack[-1] = math.atan(self.stack[-1])
                except ValueError:
                    self.stack[-1] = 0
                    self.lcdNumber.display('Err')
                    return
        else:
            if self.radioButtonDeg.isChecked():
                self.stack[-1] = math.tan(math.radians(self.stack[-1]))
            else:
                self.stack[-1] = math.tan(self.stack[-1])
        self.display()

    def inv(self):
        global INV
        INV = not INV
        if INV:
            self.pushButtonSin.setText("sin⁻¹")
            self.pushButtonCos.setText("cos⁻¹")
            self.pushButtonTan.setText("tan⁻¹")
        else:
            self.pushButtonSin.setText("sin")
            self.pushButtonCos.setText("cos")
            self.pushButtonTan.setText("tan")

    def sinh(self):
        try:
            self.stack[-1] = math.sinh(self.stack[-1])
            self.display()
        except OverflowError:
            self.lcdNumber.display('Err')

    def cosh(self):
        try:
            self.stack[-1] = math.cosh(self.stack[-1])
            self.display()
        except OverflowError:
            self.lcdNumber.display('Err')

    def tanh(self):
        try:
            self.stack[-1] = math.tanh(self.stack[-1])
            self.display()
        except OverflowError:
            self.lcdNumber.display('Err')

    def mod(self):
        if self.current_op:  # Completes the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = operator.mod

    def exp(self): # Returns 'E' raised to the power of X
        try:
            self.state = INPUT
            self.stack[-1] = math.exp(self.stack[-1])
            self.display()
        except OverflowError:
            self.lcdNumber.display('Err')
            self.stack[-1] = 0

    # Core functions
    def decimal_point(self):
        if self.state == READY:
                self.state = INPUT
                self.stack[-1] = '0.'
        # Checks if the current number already has a decimal point
        elif '.' not in str(self.stack[-1]):
            self.stack[-1] = f'{self.stack[-1]}.'
        self.display()

    def input_number(self, v):
        if isinstance(v, str):  # Checks if the input is a string ('.')
            if self.state == READY:
                self.state = INPUT
                self.stack[-1] = f'0{v}' # No numbers entered, joins with 0
            else:
                # Joins the decimal point to the existing number
                self.stack[-1] = f'{self.stack[-1]}{v}'
        else:
            if self.state == READY:
                self.state = INPUT
                #self.stack[-1] = v
            else:
                # Checks if the last input is a decimal point
                if isinstance(self.stack[-1], float) or isinstance(self.stack[-1], str) or v == 0:
                    # Converts the number to a string and joins
                    self.stack[-1] = f'{self.stack[-1]}{v}'
                else:
                    # If not, simple multiplication and addition
                    self.stack[-1] = self.stack[-1] * 10 + v

        # Converts the display to float if the last input
        # is not a decimal point, not 0 (can lead to 0.101 skipping to 0.11)
        if isinstance(self.stack[-1], str) and not self.stack[-1].endswith('.') and not v == 0:
            self.stack[-1] = float(self.stack[-1])

        self.display()


    def operation(self, op):
        if self.current_op:  # Completes the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def equals(self):
        ''' Support to allow '=' to repeat previous operation
            if no further input has been added.'''
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Err')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = READY
                self.display()


# Main function
def main():
    app = QApplication([])
    app.setApplicationName("Calculator (PyQt)")

    window = MainWindow()
    app.exec_()


# Should be used in scripts, avoided in libraries/modules
if __name__ == "__main__":
    main()
