### The `COINESPY` library provides a Python interface for interacting with the Bosch Sensortec's Engineering Boards.

### The library offers the following range of functionalities:

- Control VDD and VDDIO of sensor
- Configure SPI and I2C bus parameters
- Read and write into registers of sensors from Bosch Sensortec via SPI and I2C
- Read and write digital pins of the Application Board.

### Example for reading data

+ #### Requirements

    HW: [Application Board 3.X](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-0)

    SW: Windows/Linux/MacOS (Recommended using 64-bit system)

<br>

+ #### Example 1: Get coinespy version, coines-api version and HW version using coinespy:

```python
	import coinespy as cpy
	from coinespy import ErrorCodes
	
	COM_INTF = cpy.CommInterface.USB
	
	if __name__ == "__main__":
		board = cpy.CoinesBoard()
		print('coinespy version - %s' % cpy.__version__)
		board.open_comm_interface(COM_INTF)
		if board.error_code != ErrorCodes.COINES_SUCCESS:
			print(f'Could not connect to board: {board.error_code}')
		else:
			b_info = board.get_board_info()
			print(f"coines lib version: {board.lib_version}")
			print(
				f'BoardInfo: HW/SW ID: {hex(b_info.HardwareId)}/{hex(b_info.SoftwareId)}')
			board.close_comm_interface()
```

<br>

+ #### Example 2: [BMI085 Interrupt streaming using coinespy](https://github.com/boschsensortec/COINES/blob/main/examples/python/bmi08x/bmi085_interrupt_streaming.py)
